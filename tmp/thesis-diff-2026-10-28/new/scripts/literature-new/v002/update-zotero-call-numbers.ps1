# Writes the digest numbers [n] (01_Literature/Methods-Digest/registry.json) into Zotero's
# Call Number field. Run it from the repository root: .\scripts\literature-new\v002\update-zotero-call-numbers.ps1
# Zotero must be closed; the script refuses to run otherwise and backs up the database first.
if (Get-Process zotero -ErrorAction SilentlyContinue) {
    Write-Host 'Zotero is running. Close it completely (also in the system tray) and run this again.'
    exit 1
}
python "$PSScriptRoot\set_call_numbers.py" "$HOME\Zotero\zotero.sqlite"
