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
    [ValidateSet('all', 'proposal', 'proposal-short', 'thesis', 'slides')]
    [string]$Target = 'all'
)

$ErrorActionPreference = 'Stop'

# TeX Live is not on PATH on this machine — add it for this session only.
$texbin = 'C:\texlive\2025\bin\windows'
if (Test-Path $texbin) { $env:PATH = "$texbin;$env:PATH" }

$base = $PSScriptRoot
# name -> @{ dir = <folder>; file = <tex basename> }
$docs = [ordered]@{
    'proposal'       = @{ dir = '02_Proposal';     file = 'proposal' }
    'proposal-short' = @{ dir = '02_Proposal';     file = 'proposal_short' }
    'thesis'         = @{ dir = '03_Thesis';       file = 'thesis' }
    'slides'         = @{ dir = '06_Presentation'; file = 'slides' }
}

$targets = if ($Target -eq 'all') { @($docs.Keys) } else { @($Target) }

foreach ($name in $targets) {
    $dir  = Join-Path $base $docs[$name].dir
    $file = $docs[$name].file
    Push-Location $dir
    Write-Host "=== $name ===" -ForegroundColor Cyan
    & pdflatex -interaction=nonstopmode "$file.tex" | Out-Null
    & biber $file | Out-Null
    & pdflatex -interaction=nonstopmode "$file.tex" | Out-Null
    & pdflatex -interaction=nonstopmode "$file.tex" | Out-Null

    if (Test-Path "$file.pdf") {
        Write-Host "  built $file.pdf" -ForegroundColor Green
    } else {
        Write-Host "  FAILED - see $dir\$file.log" -ForegroundColor Red
    }

    # Surface any hard errors from the last pass.
    Select-String -Path "$file.log" -Pattern '^!' | Select-Object -First 10 |
        ForEach-Object { Write-Host "  $($_.Line)" -ForegroundColor Yellow }

    Pop-Location
}
