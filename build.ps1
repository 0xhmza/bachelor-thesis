<#
    build.ps1 — compile the LaTeX documents from PowerShell.

    Usage:
        .\build.ps1              # build all three
        .\build.ps1 proposal     # build only the proposal
        .\build.ps1 thesis
        .\build.ps1 slides

    TeXstudio users do not need this — press F5. This exists for a quick
    check that everything still compiles before committing.
#>
param(
    [ValidateSet('all', 'proposal', 'thesis', 'slides')]
    [string]$Target = 'all'
)

$ErrorActionPreference = 'Stop'

# TeX Live is not on PATH on this machine — add it for this session only.
$texbin = 'C:\texlive\2025\bin\windows'
if (Test-Path $texbin) { $env:PATH = "$texbin;$env:PATH" }

$base = $PSScriptRoot
$docs = @{
    proposal = '02_Proposal'
    thesis   = '03_Thesis'
    slides   = '06_Presentation'
}

$targets = if ($Target -eq 'all') { $docs.Keys } else { @($Target) }

foreach ($name in $targets) {
    $dir = Join-Path $base $docs[$name]
    Push-Location $dir
    Write-Host "=== $name ===" -ForegroundColor Cyan
    & pdflatex -interaction=nonstopmode "$name.tex" | Out-Null
    & biber $name | Out-Null
    & pdflatex -interaction=nonstopmode "$name.tex" | Out-Null
    & pdflatex -interaction=nonstopmode "$name.tex" | Out-Null

    if (Test-Path "$name.pdf") {
        Write-Host "  built $name.pdf" -ForegroundColor Green
    } else {
        Write-Host "  FAILED - see $dir\$name.log" -ForegroundColor Red
    }

    # Surface any hard errors from the last pass.
    Select-String -Path "$name.log" -Pattern '^!' | Select-Object -First 10 |
        ForEach-Object { Write-Host "  $($_.Line)" -ForegroundColor Yellow }

    Pop-Location
}
