<#
    build.ps1 — compile the LaTeX documents from PowerShell.

    Usage:
        .\build.ps1              # build all three
        .\build.ps1 proposal     # build only the proposal
        .\build.ps1 thesis
        .\build.ps1 slides

    TeXstudio users do not need this — press F5. This exists for a quick
    check that everything still compiles before committing.

    Each document folder carries a `latexmkrc` with the tool chain
    (PDFLaTeX and the required bibliography passes, built in place), so this script and
    LaTeX Workshop only have to say *which file* to build, never *how*.
    latexmk re-runs the passes the auxiliary files ask for, which is why
    there is no hard-coded pass count below.
#>
param(
    [ValidateSet('all', 'proposal', 'thesis', 'slides')]
    [string]$Target = 'all'
)

$ErrorActionPreference = 'Stop'

# Non-zero exits of native tools are reported through $LASTEXITCODE, not as
# terminating errors (PowerShell 7.3+ would otherwise throw on them).
if ($PSVersionTable.PSVersion.Major -ge 7) {
    $PSNativeCommandUseErrorActionPreference = $false
}

# TeX Live is not guaranteed to be on PATH (e.g. in a fresh shell) — add it
# for this session only.
$texbin = 'C:\texlive\2025\bin\windows'
if (Test-Path $texbin) { $env:PATH = "$texbin;$env:PATH" }

if (-not (Get-Command latexmk -ErrorAction SilentlyContinue)) {
    throw "latexmk not found. Install TeX Live, or fix `$texbin in build.ps1."
}

$base = $PSScriptRoot
# name -> @{ dir = <folder>; file = <tex basename> }
$docs = [ordered]@{
    'proposal'       = @{ dir = '03_Thesis/proposal'; file = 'proposal' }
    'thesis'         = @{ dir = '03_Thesis';          file = 'thesis' }
    'slides'         = @{ dir = '06_Presentation';    file = 'slides' }
}

$targets = if ($Target -eq 'all') { @($docs.Keys) } else { @($Target) }
$failed = @()

foreach ($name in $targets) {
    $dir  = Join-Path $base $docs[$name].dir
    $file = $docs[$name].file
    Write-Host "=== $name ===" -ForegroundColor Cyan

    Push-Location $dir
    try {
        & latexmk -silent "$file.tex"
        $exit = $LASTEXITCODE
    } finally {
        Pop-Location
    }

    if ($exit -eq 0 -and (Test-Path (Join-Path $dir "$file.pdf"))) {
        Write-Host "  built $file.pdf" -ForegroundColor Green
    } else {
        Write-Host "  FAILED - see $dir\$file.log" -ForegroundColor Red
        $failed += $name
    }

    # Surface any hard errors from the last pass.
    $log = Join-Path $dir "$file.log"
    if (Test-Path $log) {
        Select-String -Path $log -Pattern '^!' | Select-Object -First 10 |
            ForEach-Object { Write-Host "  $($_.Line)" -ForegroundColor Yellow }
    }
}

if ($failed.Count -gt 0) {
    Write-Host "Failed: $($failed -join ', ')" -ForegroundColor Red
    exit 1
}
