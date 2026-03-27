from __future__ import annotations

import argparse
import json
import os
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path


def reader_thread(stream, out_queue: queue.Queue[tuple[str, str]]) -> None:
    try:
        for raw in iter(stream.readline, ''):
            if raw == '':
                break
            out_queue.put(('line', raw.rstrip('\r\n')))
    except Exception as exc:  # pragma: no cover
        out_queue.put(('error', f'{type(exc).__name__}: {exc}'))
    finally:
        out_queue.put(('eof', ''))


def wait_for_line(out_queue: queue.Queue[tuple[str, str]], timeout_seconds: float, label: str) -> str:
    deadline = time.monotonic() + timeout_seconds
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(f'Timeout waiting for {label} after {timeout_seconds:.1f}s')
        kind, value = out_queue.get(timeout=remaining)
        if kind == 'line':
            return value
        if kind == 'error':
            raise RuntimeError(f'stdout reader failed while waiting for {label}: {value}')
        if kind == 'eof':
            raise RuntimeError(f'stdout closed while waiting for {label}')


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout-seconds', type=float, default=8.0)
    args = parser.parse_args()

    ahk_exe = os.environ.get('AHK_EXE')
    if not ahk_exe:
        raise RuntimeError('AHK_EXE environment variable is required')

    repo_root = Path(__file__).resolve().parent.parent
    child_path = repo_root / 'scripts' / 'tests' / 'stdio' / 'child_echo.ahk'
    artifact_dir = Path(os.environ.get('ARTIFACT_DIR', repo_root / 'artifacts-ipc-fast'))
    stdout_path = artifact_dir / 'stdout-transcript.txt'
    stderr_path = artifact_dir / 'stderr.txt'
    summary_path = artifact_dir / 'summary.json'
    meta_path = artifact_dir / 'run-metadata.txt'

    transcript: list[str] = []
    started_at = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    meta_lines = [
        f'timestamp_utc={started_at}',
        f'ahk_exe={ahk_exe}',
        f'child_path={child_path}',
        f'timeout_seconds={args.timeout_seconds}',
    ]

    proc = subprocess.Popen(
        [ahk_exe, '/ErrorStdOut', str(child_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=str(child_path.parent),
        bufsize=1,
    )
    meta_lines.append(f'pid={proc.pid}')
    write_file(meta_path, '\n'.join(meta_lines) + '\n')

    stdout_queue: queue.Queue[tuple[str, str]] = queue.Queue()
    stdout_reader = threading.Thread(target=reader_thread, args=(proc.stdout, stdout_queue), daemon=True)
    stdout_reader.start()

    stderr_chunks: list[str] = []

    def drain_stderr() -> None:
        if proc.stderr is None:
            return
        try:
            stderr_chunks.append(proc.stderr.read())
        except Exception as exc:  # pragma: no cover
            stderr_chunks.append(f'[stderr read failed] {type(exc).__name__}: {exc}')

    stderr_reader = threading.Thread(target=drain_stderr, daemon=True)
    stderr_reader.start()

    try:
        ready = wait_for_line(stdout_queue, args.timeout_seconds, 'READY')
        transcript.append(f'< {ready}')
        if ready != 'READY':
            raise AssertionError(f"Expected READY but received '{ready}'")

        checks = [
            ('ping', 'pong', None),
            ('hello CI', 'echo=hello CI', None),
            ('time', None, 'time='),
            ('exit', 'bye', None),
        ]

        for send_text, expected, expected_prefix in checks:
            assert proc.stdin is not None
            proc.stdin.write(send_text + '\n')
            proc.stdin.flush()
            transcript.append(f'> {send_text}')

            line = wait_for_line(stdout_queue, args.timeout_seconds, send_text)
            transcript.append(f'< {line}')

            if expected is not None and line != expected:
                raise AssertionError(f"For '{send_text}' expected '{expected}' but received '{line}'")
            if expected_prefix is not None and not line.startswith(expected_prefix):
                raise AssertionError(f"For '{send_text}' expected prefix '{expected_prefix}' but received '{line}'")

        if proc.stdin is not None:
            proc.stdin.close()

        proc.wait(timeout=args.timeout_seconds)
        stderr_reader.join(timeout=1.0)
        stderr_text = ''.join(stderr_chunks)
        write_file(stderr_path, stderr_text)
        write_file(stdout_path, '\n'.join(transcript) + ('\n' if transcript else ''))

        summary = {
            'passed': proc.returncode == 0,
            'timeout_seconds': args.timeout_seconds,
            'child_exit_code': proc.returncode,
            'transcript_line_count': len(transcript),
            'checks': ['READY', 'ping/pong', 'echo', 'time', 'exit'],
            'transcript_preview': transcript,
        }
        write_file(summary_path, json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
        with meta_path.open('a', encoding='utf-8') as fh:
            fh.write(f'exit_code={proc.returncode}\n')

        if proc.returncode != 0:
            raise RuntimeError(f'Child exited with code {proc.returncode}')
        return 0

    except Exception as exc:
        try:
            proc.kill()
        except Exception:
            pass
        try:
            proc.wait(timeout=1.0)
        except Exception:
            pass
        stderr_reader.join(timeout=1.0)
        stderr_text = ''.join(stderr_chunks)
        write_file(stderr_path, stderr_text)
        write_file(stdout_path, '\n'.join(transcript) + ('\n' if transcript else ''))
        summary = {
            'passed': False,
            'error': str(exc),
            'timeout_seconds': args.timeout_seconds,
            'child_exit_code': proc.returncode,
            'transcript_line_count': len(transcript),
            'transcript_preview': transcript,
        }
        write_file(summary_path, json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
        with meta_path.open('a', encoding='utf-8') as fh:
            fh.write(f'exit_code={proc.returncode}\n')
        raise


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'[harness] {type(exc).__name__}: {exc}', file=sys.stderr)
        raise
