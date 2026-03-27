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


class HarnessFailure(RuntimeError):
    pass


def stream_reader(stream, out_queue: queue.Queue[tuple[str, str]]) -> None:
    try:
        for raw in iter(stream.readline, ''):
            if raw == '':
                break
            out_queue.put(('line', raw.rstrip('\r\n')))
    except Exception as exc:  # pragma: no cover
        out_queue.put(('error', f'{type(exc).__name__}: {exc}'))
    finally:
        out_queue.put(('eof', ''))


def stderr_reader(stream, chunks: list[str]) -> None:
    try:
        for raw in iter(stream.readline, ''):
            if raw == '':
                break
            chunks.append(raw)
    except Exception as exc:  # pragma: no cover
        chunks.append(f'[stderr read failed] {type(exc).__name__}: {exc}\n')


def wait_for_line(proc: subprocess.Popen[str], out_queue: queue.Queue[tuple[str, str]], timeout_seconds: float, label: str, stderr_chunks: list[str]) -> str:
    deadline = time.monotonic() + timeout_seconds
    while True:
        if proc.poll() is not None:
            stderr_text = ''.join(stderr_chunks).strip()
            raise HarnessFailure(
                f"Child exited before {label}. exit_code={proc.returncode} stderr={stderr_text!r}"
            )

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            stderr_text = ''.join(stderr_chunks).strip()
            raise HarnessFailure(
                f"Timeout waiting for {label} after {timeout_seconds:.1f}s; child_exit={proc.poll()} stderr={stderr_text!r}"
            )

        try:
            kind, value = out_queue.get(timeout=min(0.2, remaining))
        except queue.Empty:
            continue

        if kind == 'line':
            return value
        if kind == 'error':
            raise HarnessFailure(f'stdout reader failed while waiting for {label}: {value}')
        if kind == 'eof':
            stderr_text = ''.join(stderr_chunks).strip()
            raise HarnessFailure(f'stdout closed while waiting for {label}; stderr={stderr_text!r}')


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout-seconds', type=float, default=4.0)
    args = parser.parse_args()

    ahk_exe = os.environ.get('AHK_EXE')
    if not ahk_exe:
        raise RuntimeError('AHK_EXE environment variable is required')

    repo_root = Path(__file__).resolve().parent.parent
    child_path = repo_root / 'scripts' / 'tests' / 'stdio' / 'child_echo_v2.ahk'
    artifact_dir = Path(os.environ.get('ARTIFACT_DIR', repo_root / 'artifacts-ipc-fast-v2'))
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
    stdout_thread = threading.Thread(target=stream_reader, args=(proc.stdout, stdout_queue), daemon=True)
    stdout_thread.start()

    stderr_chunks: list[str] = []
    stderr_thread = threading.Thread(target=stderr_reader, args=(proc.stderr, stderr_chunks), daemon=True)
    stderr_thread.start()

    try:
        ready = wait_for_line(proc, stdout_queue, args.timeout_seconds, 'READY', stderr_chunks)
        transcript.append(f'< {ready}')
        if ready != 'READY':
            raise HarnessFailure(f"Expected READY but received {ready!r}")

        checks = [
            ('ping', 'pong', None),
            ('hello CI', 'echo=hello CI', None),
            ('time', None, 'time='),
            ('exit', 'bye', None),
        ]

        for send_text, expected, expected_prefix in checks:
            if proc.stdin is None:
                raise HarnessFailure('stdin pipe is missing')
            proc.stdin.write(send_text + '\n')
            proc.stdin.flush()
            transcript.append(f'> {send_text}')

            line = wait_for_line(proc, stdout_queue, args.timeout_seconds, send_text, stderr_chunks)
            transcript.append(f'< {line}')

            if expected is not None and line != expected:
                raise HarnessFailure(f"For {send_text!r} expected {expected!r} but received {line!r}")
            if expected_prefix is not None and not line.startswith(expected_prefix):
                raise HarnessFailure(f"For {send_text!r} expected prefix {expected_prefix!r} but received {line!r}")

        if proc.stdin is not None:
            proc.stdin.close()

        try:
            proc.wait(timeout=args.timeout_seconds)
        except subprocess.TimeoutExpired:
            raise HarnessFailure(f'Child did not exit within {args.timeout_seconds:.1f}s after exit command')

        stderr_thread.join(timeout=1.0)
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
            'stderr_preview': stderr_text.splitlines()[-10:],
        }
        write_file(summary_path, json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
        with meta_path.open('a', encoding='utf-8') as fh:
            fh.write(f'exit_code={proc.returncode}\n')

        if proc.returncode != 0:
            raise HarnessFailure(f'Child exited with code {proc.returncode}')
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
        stderr_thread.join(timeout=1.0)
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
            'stderr_preview': stderr_text.splitlines()[-10:],
        }
        write_file(summary_path, json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
        with meta_path.open('a', encoding='utf-8') as fh:
            fh.write(f'exit_code={proc.returncode}\n')
        raise


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'[harness-v2] {type(exc).__name__}: {exc}', file=sys.stderr)
        raise
