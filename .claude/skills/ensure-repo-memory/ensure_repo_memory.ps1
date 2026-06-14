# ensure_repo_memory.ps1
# -----------------------------------------------------------------------------
# Idempotently redirect THIS repo's Claude auto-memory into the version-controlled
# <repo-root>/.claude/memory folder, by setting `autoMemoryDirectory` in the repo's
# .claude/settings.local.json (machine-local, gitignored).
#
# Deterministic and generic: works for any repo that uses the .claude/memory convention.
# Re-running once configured is a cheap no-op. Prints a single STATUS line:
#   OK:    already configured
#   FIXED: path was (re)written -> a relaunch is required to load memory
#   SKIP:  not applicable here (e.g. no .claude folder)
# -----------------------------------------------------------------------------
$ErrorActionPreference = 'Stop'

# 1. Repo root (git if available, else current directory)
$root = $null
try { $root = (git rev-parse --show-toplevel 2>$null) } catch { $root = $null }
if (-not $root) { $root = (Get-Location).Path }
$root = [System.IO.Path]::GetFullPath($root)

$claudeDir    = Join-Path $root '.claude'
$memDir       = [System.IO.Path]::GetFullPath((Join-Path $claudeDir 'memory'))
$settingsPath = Join-Path $claudeDir 'settings.local.json'

if (-not (Test-Path $claudeDir)) {
  Write-Output "SKIP: no .claude folder at $root"
  exit 0
}

# 2. Load (or initialise) settings.local.json, preserving any existing keys
if (Test-Path $settingsPath) {
  try { $cfg = Get-Content $settingsPath -Raw -Encoding UTF8 | ConvertFrom-Json } catch { $cfg = [PSCustomObject]@{} }
} else {
  $cfg = [PSCustomObject]@{ '$schema' = 'https://json.schemastore.org/claude-code-settings.json' }
}

# 3. Compare current value to the expected absolute path (case-insensitive, slash-normalised)
function Norm($p) { if (-not $p) { return '' } return ($p.TrimEnd('\','/').ToLower()) }

$current = $null
if ($cfg.PSObject.Properties.Name -contains 'autoMemoryDirectory') { $current = $cfg.autoMemoryDirectory }

if ((Norm $current) -eq (Norm $memDir)) {
  Write-Output "OK: repo memory already configured -> $memDir"
  exit 0
}

# 4. Fix: ensure the memory folder exists, set the property, write back
if (-not (Test-Path $memDir)) { New-Item -ItemType Directory -Force -Path $memDir | Out-Null }

if ($cfg.PSObject.Properties.Name -contains 'autoMemoryDirectory') {
  $cfg.autoMemoryDirectory = $memDir
} else {
  $cfg | Add-Member -NotePropertyName 'autoMemoryDirectory' -NotePropertyValue $memDir
}

$json = $cfg | ConvertTo-Json -Depth 20
[System.IO.File]::WriteAllText($settingsPath, $json, (New-Object System.Text.UTF8Encoding($false)))
Write-Output "FIXED: set autoMemoryDirectory -> $memDir in settings.local.json. RELAUNCH REQUIRED so memory loads from the repo."
exit 0
