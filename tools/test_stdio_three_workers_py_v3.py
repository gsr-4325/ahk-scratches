from __future__ import annotations

import argparse
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path


class HarnessFailure(RuntimeError):
    pass


@dataclass
class WorkerProc:
    worker_id: str
    proc: subprocess.Popen[str]
    stdout_queue: queue.Queue[tuple[str, str]]
    stderr_chunks: list[str]
    stdout_thread: threading.Thread
    stderr_thread: threading.Thread
    child_log_path: Path
    script_copy_path: Path


def stream_reader(stream, out_queue: queue.Queue[tuple[str, str]]) -> None:
    try:
        for raw in iter(stream.readline, ''):
            if raw == '':
                break
            out_queue.put(('line', raw.rstrip('\r\n')))
    except Exception as exc:
        out_queue.put(('error', f'{type(exc).__name__}: {exc}'))
    finally:
        out_queue.put(('eof', ''))


def stderr_reader(stream, chunks: list[str]) -> None:
    try:
        for raw in iter(stream.readline, ''):
            if raw == '':
                break
            chunks.append(raw)
    except Exception as exc:
        chunks.append(f'[stderr read failed] {type(exc).__name__}: {exc}\n')


def wait_for_line(worker: WorkerProc, timeout_seconds: float, label: str) -> str:
    deadline = time.monotonic() + timeout_seconds
    while True:
        if worker.proc.poll() is not None:
            stderr_text = ''.join(worker.stderr_chunks).strip()
            child_log = worker.child_log_path.read_text(encoding='utf-8') if worker.child_log_path.exists() else ''
            raise HarnessFailure(
                f"{worker.worker_id} exited before {label}. exit_code={worker.proc.returncode} stderr={stderr_text!r} child_log={child_log!r}"
            )

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            stderr_text = ''.join(worker.stderr_chunks).strip()
            child_log = worker.child_log_path.read_text(encoding='utf-8') if worker.child_log_path.exists() else ''
            raise HarnessFailure(
                f"Timeout waiting for {label} from {worker.worker_id} after {timeout_seconds:.1f}s; child_exit={worker.proc.poll()} stderr={stderr_text!r} child_log={child_log!r}"
            )

        try:
            kind, value = worker.stdout_queue.get(timeout=min(0.2, remaining))
        except queue.Empty:
            continue

        if kind == 'line':
            return value
        if kind == 'error':
            raise HarnessFailure(f'stdout reader failed for {worker.worker_id} while waiting for {label}: {value}')
        if kind == 'eof':
            stderr_text = ''.join(worker.stderr_chunks).strip()
            child_log = worker.child_log_path.read_text(encoding='utf-8') if worker.child_log_path.exists() else ''
            raise HarnessFailure(
                f'stdout closed for {worker.worker_id} while waiting for {label}; stderr={stderr_text!r} child_log={child_log!r}'
            )


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def start_worker(worker_id: str, ahk_exe: str, child_template_path: Path, runtime_dir: Path) -> WorkerProc:
    runtime_dir.mkdir(parents=True, exist_ok=True)
    script_copy_path = runtime_dir / f'{worker_id}.ahk'
    child_log_path = runtime_dir / f'{worker_id}.log'
    shutil.copyfile(child_template_path, script_copy_path)

    proc = subprocess.Popen(
        [ahk_exe, '/ErrorStdOut', str(script_copy_path), worker_id, str(child_log_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=str(runtime_dir),
        bufsize=1,
    )

    stdout_queue: queue.Queue[tuple[str, str]] = queue.Queue()
    stderr_chunks: list[str] = []
    stdout_thread = threading.Thread(target=stream_reader, args=(proc.stdout, stdout_queue), daemon=True)
    stderr_thread = threading.Thread(target=stderr_reader, args=(proc.stderr, stderr_chunks), daemon=True)
    stdout_thread.start()
    stderr_thread.start()
    return WorkerProc(worker_id, proc, stdout_queue, stderr_chunks, stdout_thread, stderr_thread, child_log_path, script_copy_path)


def send_and_expect(worker: WorkerProc, send_text: str, timeout_seconds: float, expected: str | None = None, expected_prefix: str | None = None) -> str:
    if worker.proc.stdin is None:
        raise HarnessFailure(f'{worker.worker_id} stdin pipe is missing')
    worker.proc.stdin.write(send_text + '\n')
    worker.proc.stdin.flush()
    line = wait_for_line(worker, timeout_seconds, send_text)
    if expected is not None and line != expected:
        raise HarnessFailure(f"For {worker.worker_id} sending {send_text!r} expected {expected!r} but received {line!r}")
    if expected_prefix is not None and not line.startswith(expected_prefix):
        raise HarnessFailure(f"For {worker.worker_id} sending {send_text!r} expected prefix {expected_prefix!r} but received {line!r}")
    return line


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout-seconds', type=float, default=8.0)
    args = parser.parse_args()

    ahk_exe = os.environ.get('AHK_EXE')
    if not ahk_exe:
        raise RuntimeError('AHK_EXE environment variable is required')

    repo_root = Path(__file__).resolve().parent.parent
    child_template_path = repo_root / 'scripts' / 'tests' / 'stdio' / 'child_echo_multiworker_v2.ahk'
    artifact_dir = Path(os.environ.get('ARTIFACT_DIR', repo_root / 'artifacts-ipc-three-workers-v3'))
    runtime_dir = artifact_dir / 'runtime-workers'
    stdout_path = artifact_dir / 'stdout-transcript.txt'
    stderr_path = artifact_dir / 'stderr.txt'
    summary_path = artifact_dir / 'summary.json'
    meta_path = artifact_dir / 'run-metadata.txt'
    child_logs_path = artifact_dir / 'child-logs.txt'

    worker_ids = ['worker-001', 'worker-002', 'worker-003']
    workers: list[WorkerProc] = []
    transcript: list[str] = []
    started_at = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    meta_lines = [
        f'timestamp_utc={started_at}',
        f'ahk_exe={ahk_exe}',
        f'child_template_path={child_template_path}',
        f'timeout_seconds={args.timeout_seconds}',
        f'worker_count={len(worker_ids)}',
    ]

    try:
        for worker_id in worker_ids:
            worker = start_worker(worker_id, ahk_exe, child_template_path, runtime_dir)
            workers.append(worker)
            meta_lines.append(f'{worker.worker_id}.pid={worker.proc.pid}')
            meta_lines.append(f'{worker.worker_id}.script={worker.script_copy_path}')
            meta_lines.append(f'{worker.worker_id}.log={worker.child_log_path}')
            time.sleep(0.15)

        write_file(meta_path, '\n'.join(meta_lines) + '\n')

        for worker in workers:
            ready = wait_for_line(worker, args.timeout_seconds, 'READY')
            transcript.append(f'{worker.worker_id} < {ready}')
            if ready != 'READY':
                raise HarnessFailure(f"Expected READY from {worker.worker_id} but received {ready!r}")

        direct_messages = [
            ('worker-001', 'hello one', 'echo=hello one'),
            ('worker-002', 'hello two', 'echo=hello two'),
            ('worker-003', 'hello three', 'echo=hello three'),
        ]
        worker_by_id = {worker.worker_id: worker for worker in workers}

        for worker_id, send_text, expected in direct_messages:
            worker = worker_by_id[worker_id]
            transcript.append(f'{worker_id} > {send_text}')
            line = send_and_expect(worker, send_text, args.timeout_seconds, expected=expected)
            transcript.append(f'{worker_id} < {line}')

        for worker in workers:
            transcript.append(f'{worker.worker_id} > ping')
            line = send_and_expect(worker, 'ping', args.timeout_seconds, expected='pong')
            transcript.append(f'{worker.worker_id} < {line}')

        for worker in workers:
            transcript.append(f'{worker.worker_id} > time')
            line = send_and_expect(worker, 'time', args.timeout_seconds, expected_prefix='time=')
            transcript.append(f'{worker.worker_id} < {line}')

        exit_codes: dict[str, int | None] = {}
        for worker in workers:
            transcript.append(f'{worker.worker_id} > exit')
            line = send_and_expect(worker, 'exit', args.timeout_seconds, expected='bye')
            transcript.append(f'{worker.worker_id} < {line}')
            if worker.proc.stdin is not None:
                worker.proc.stdin.close()
            try:
                worker.proc.wait(timeout=args.timeout_seconds)
            except subprocess.TimeoutExpired:
                raise HarnessFailure(f'{worker.worker_id} did not exit within {args.timeout_seconds:.1f}s after exit command')
            worker.stderr_thread.join(timeout=1.0)
            exit_codes[worker.worker_id] = worker.proc.returncode
            if worker.proc.returncode != 0:
                raise HarnessFailure(f'{worker.worker_id} exited with code {worker.proc.returncode}')

        stderr_lines: list[str] = []
        child_log_lines: list[str] = []
        for worker in workers:
            if worker.stderr_chunks:
                stderr_lines.append(f'[{worker.worker_id}]')
                stderr_lines.extend(chunk.rstrip('\n') for chunk in worker.stderr_chunks)
            if worker.child_log_path.exists():
                child_log_lines.append(f'[{worker.worker_id}]')
                child_log_lines.extend(worker.child_log_path.read_text(encoding='utf-8').splitlines())

        stderr_text = '\n'.join(stderr_lines)
        child_logs_text = '\n'.join(child_log_lines)
        write_file(stderr_path, stderr_text + ('\n' if stderr_text else ''))
        write_file(child_logs_path, child_logs_text + ('\n' if child_logs_text else ''))
        write_file(stdout_path, '\n'.join(transcript) + ('\n' if transcript else ''))

        summary = {
            'passed': True,
            'timeout_seconds': args.timeout_seconds,
            'worker_count': len(worker_ids),
            'worker_exit_codes': exit_codes,
            'transcript_line_count': len(transcript),
            'checks': [
                'all READY',
                'direct echo to worker-001',
                'direct echo to worker-002',
                'direct echo to worker-003',
                'broadcast ping',
                'per-worker time',
                'clean shutdown',
            ],
            'transcript_preview': transcript,
            'stderr_preview': stderr_lines[-20:],
            'child_logs_preview': child_log_lines[-30:],
        }
        write_file(summary_path, json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
        with meta_path.open('a', encoding='utf-8') as fh:
            for worker_id in worker_ids:
                fh.write(f'{worker_id}.exit_code={exit_codes[worker_id]}\n')
        return 0

    except Exception as exc:
        exit_codes: dict[str, int | None] = {}
        stderr_lines: list[str] = []
        child_log_lines: list[str] = []
        for worker in workers:
            try:
                if worker.proc.stdin is not None and not worker.proc.stdin.closed:
                    worker.proc.stdin.close()
            except Exception:
                pass
            try:
                if worker.proc.poll() is None:
                    worker.proc.kill()
            except Exception:
                pass
            try:
                worker.proc.wait(timeout=1.0)
            except Exception:
                pass
            worker.stderr_thread.join(timeout=1.0)
            exit_codes[worker.worker_id] = worker.proc.returncode
            if worker.stderr_chunks:
                stderr_lines.append(f'[{worker.worker_id}]')
                stderr_lines.extend(chunk.rstrip('\n') for chunk in worker.stderr_chunks)
            if worker.child_log_path.exists():
                child_log_lines.append(f'[{worker.worker_id}]')
                child_log_lines.extend(worker.child_log_path.read_text(encoding='utf-8').splitlines())

        stderr_text = '\n'.join(stderr_lines)
        child_logs_text = '\n'.join(child_log_lines)
        write_file(stderr_path, stderr_text + ('\n' if stderr_text else ''))
        write_file(child_logs_path, child_logs_text + ('\n' if child_logs_text else ''))
        write_file(stdout_path, '\n'.join(transcript) + ('\n' if transcript else ''))
        summary = {
            'passed': False,
            'error': str(exc),
            'timeout_seconds': args.timeout_seconds,
            'worker_count': len(worker_ids),
            'worker_exit_codes': exit_codes,
            'transcript_line_count': len(transcript),
            'transcript_preview': transcript,
            'stderr_preview': stderr_lines[-20:],
            'child_logs_preview': child_log_lines[-30:],
        }
        write_file(summary_path, json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
        with meta_path.open('a', encoding='utf-8') as fh:
            for worker in workers:
                fh.write(f'{worker.worker_id}.exit_code={worker.proc.returncode}\n')
        raise


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'[three-workers-v3] {type(exc).__name__}: {exc}', file=sys.stderr)
        raise
