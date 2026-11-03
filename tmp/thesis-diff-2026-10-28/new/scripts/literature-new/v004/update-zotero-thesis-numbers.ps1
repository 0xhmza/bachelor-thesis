# Writes the thesis reference numbers [n] (from 03_Thesis/thesis.bbl) into Zotero's Rights and Call Number fields.
# Compile the thesis first, then run from the repository root:
#   .\scripts\literature-new\v004\update-zotero-thesis-numbers.ps1
# Zotero must be closed; the script refuses to run otherwise and backs up the database first.
if (Get-Process zotero -ErrorAction SilentlyContinue) {
    Write-Host 'Zotero is running. Close it completely (also in the system tray) and run this again.'
    exit 1
}
python "$PSScriptRoot\set_thesis_numbers.py" "$HOME\Zotero\zotero.sqlite"
