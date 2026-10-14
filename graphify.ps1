param(
    [Parameter(Position=0)][string]$Command = 'query',
    [Parameter(ValueFromRemainingArguments=$true)][string[]]$Arguments
)
$ErrorActionPreference = 'Stop'
$taskPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $taskPython)) {
    throw 'Run python -m venv .venv, then .\.venv\Scripts\python.exe -m pip install -r requirements-graphify.txt'
}
Push-Location $PSScriptRoot
try {
    if ($Command -in @('refresh', 'prepare', 'import-semantic')) {
        & $taskPython (Join-Path $PSScriptRoot 'scripts\thesis_graph.py') $Command @Arguments
    } else {
        # Use this installation, independent of global PATH or interpreter choice.
        & $taskPython -m graphify $Command @Arguments
    }
    $taskExitCode = $LASTEXITCODE
} finally { Pop-Location }
exit $taskExitCode
