param(
    [int]$TimeoutSeconds = 20
)

$ErrorActionPreference = 'Stop'

if (-not $env:AHK_EXE) {
    throw 'AHK_EXE environment variable is required.'
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$childPath = Join-Path $repoRoot 'scripts/tests/stdio/child_echo.ahk'
$artifactDir = if ($env:ARTIFACT_DIR) { $env:ARTIFACT_DIR } else { Join-Path $repoRoot 'artifacts-ipc' }
$stdoutTranscriptPath = Join-Path $artifactDir 'stdout-transcript.txt'
$stderrPath = Join-Path $artifactDir 'stderr.txt'
$summaryPath = Join-Path $artifactDir 'summary.json'
$metaPath = Join-Path $artifactDir 'run-metadata.txt'

New-Item -ItemType Directory -Force -Path $artifactDir | Out-Null

$transcript = New-Object System.Collections.Generic.List[string]

function Add-TranscriptLine {
    param([string]$Line)
    $script:transcript.Add($Line)
}

function Read-LineWithTimeout {
    param(
        [Parameter(Mandatory)] $Reader,
        [Parameter(Mandatory)] [int] $TimeoutMs,
        [Parameter(Mandatory)] [string] $Label
    )

    $task = $Reader.ReadLineAsync()
    if (-not $task.Wait($TimeoutMs)) {
        throw "Timeout waiting for $Label after ${TimeoutMs}ms"
    }

    return $task.Result
}

$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = $env:AHK_EXE
$null = $psi.ArgumentList.Add('/ErrorStdOut')
$null = $psi.ArgumentList.Add($childPath)
$psi.WorkingDirectory = Split-Path -Parent $childPath
$psi.UseShellExecute = $false
$psi.RedirectStandardInput = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.CreateNoWindow = $true
$psi.StandardOutputEncoding = [System.Text.Encoding]::UTF8
$psi.StandardErrorEncoding = [System.Text.Encoding]::UTF8

$process = [System.Diagnostics.Process]::new()
$process.StartInfo = $psi

try {
    if (-not $process.Start()) {
        throw 'Failed to start child process.'
    }

    $stderrTask = $process.StandardError.ReadToEndAsync()

    @(
        "timestamp_utc=$(Get-Date -AsUTC -Format o)",
        "ahk_exe=$($env:AHK_EXE)",
        "child_path=$childPath",
        "timeout_seconds=$TimeoutSeconds",
        "pid=$($process.Id)"
    ) | Set-Content -LiteralPath $metaPath

    $ready = Read-LineWithTimeout -Reader $process.StandardOutput -TimeoutMs ($TimeoutSeconds * 1000) -Label 'READY'
    Add-TranscriptLine "< $ready"
    if ($ready -ne 'READY') {
        throw "Expected READY but received '$ready'"
    }

    $checks = @(
        @{ send = 'ping'; expected = 'pong' },
        @{ send = 'hello CI'; expected = 'echo=hello CI' },
        @{ send = 'time'; expectedPrefix = 'time=' },
        @{ send = 'exit'; expected = 'bye' }
    )

    foreach ($check in $checks) {
        $process.StandardInput.WriteLine($check.send)
        $process.StandardInput.Flush()
        Add-TranscriptLine "> $($check.send)"

        $line = Read-LineWithTimeout -Reader $process.StandardOutput -TimeoutMs ($TimeoutSeconds * 1000) -Label $check.send
        Add-TranscriptLine "< $line"

        if ($check.ContainsKey('expected')) {
            if ($line -ne $check.expected) {
                throw "For '$($check.send)' expected '$($check.expected)' but received '$line'"
            }
        }
        elseif ($check.ContainsKey('expectedPrefix')) {
            if (-not $line.StartsWith($check.expectedPrefix)) {
                throw "For '$($check.send)' expected prefix '$($check.expectedPrefix)' but received '$line'"
            }
        }
    }

    $process.StandardInput.Close()

    if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
        try { $process.Kill($true) } catch {}
        Add-Content -LiteralPath $metaPath 'timed_out=true'
        throw "Child process did not exit within $TimeoutSeconds seconds"
    }

    Add-Content -LiteralPath $metaPath "exit_code=$($process.ExitCode)"

    $stderr = $stderrTask.GetAwaiter().GetResult()
    Set-Content -LiteralPath $stderrPath -Value $stderr
    Set-Content -LiteralPath $stdoutTranscriptPath -Value $transcript

    if ($process.ExitCode -ne 0) {
        throw "Child exited with code $($process.ExitCode)"
    }

    $summary = [ordered]@{
        passed = $true
        timeout_seconds = $TimeoutSeconds
        child_exit_code = $process.ExitCode
        transcript_line_count = $transcript.Count
        checks = @('READY', 'ping/pong', 'echo', 'time', 'exit')
    }

    $summary | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $summaryPath
}
catch {
    $stderr = ''
    try {
        if ($stderrTask) {
            $stderr = $stderrTask.GetAwaiter().GetResult()
        }
    }
    catch {}

    Set-Content -LiteralPath $stderrPath -Value $stderr
    Set-Content -LiteralPath $stdoutTranscriptPath -Value $transcript

    $summary = [ordered]@{
        passed = $false
        error = $_.Exception.Message
        timeout_seconds = $TimeoutSeconds
        transcript_line_count = $transcript.Count
    }

    if ($process -and $process.HasExited) {
        $summary.child_exit_code = $process.ExitCode
        Add-Content -LiteralPath $metaPath "exit_code=$($process.ExitCode)"
    }

    $summary | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $summaryPath
    throw
}
finally {
    if ($process) {
        try {
            if (-not $process.HasExited) {
                $process.Kill($true)
            }
        }
        catch {}

        $process.Dispose()
    }
}
