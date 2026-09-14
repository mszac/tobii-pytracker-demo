$ErrorActionPreference = "Stop"

function Invoke-Git {
    & git @args
    if ($LASTEXITCODE -ne 0) {
        throw "git failed with exit code $LASTEXITCODE: git $($args -join ' ')"
    }
}


$UpstreamUrl = if ($env:TOBII_PYTRACKER_URL) { $env:TOBII_PYTRACKER_URL } else { "https://github.com/sbobek/tobii-pytracker.git" }
$UpstreamRef = $env:TOBII_PYTRACKER_REF
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ExamplesRoot = (Resolve-Path (Join-Path $ScriptDir "..")).Path
$ParentDir = Split-Path -Parent $ExamplesRoot
if ((Split-Path -Leaf $ParentDir) -eq "tobii-pytracker") {
    throw "Examples repo is nested inside upstream; this helper cannot replace its parent safely. Use docs/windows/NATIVE_TESTING.md for a full reset."
}
$WorkspaceRoot = $ParentDir
$UpstreamDir = Join-Path $WorkspaceRoot "tobii-pytracker"

if ([string]::IsNullOrWhiteSpace($WorkspaceRoot) -or $WorkspaceRoot -eq [System.IO.Path]::GetPathRoot($WorkspaceRoot)) {
    throw "Refusing to operate with unsafe workspace root: '$WorkspaceRoot'"
}
if ($UpstreamDir -eq $ExamplesRoot) {
    throw "Upstream path resolves to the examples repository."
}
if ((Split-Path -Leaf $UpstreamDir) -ne "tobii-pytracker") {
    throw "Refusing to remove unexpected directory name: $UpstreamDir"
}

Write-Host "[prepare] examples repo: $ExamplesRoot"
Write-Host "[prepare] workspace:     $WorkspaceRoot"
Write-Host "[prepare] upstream path: $UpstreamDir"

if (Test-Path -LiteralPath $UpstreamDir) {
    Write-Host "[prepare] removing previous upstream clone: $UpstreamDir"
    Remove-Item -LiteralPath $UpstreamDir -Recurse -Force
}

Write-Host "[prepare] cloning original upstream: $UpstreamUrl"
Invoke-Git clone $UpstreamUrl $UpstreamDir

if (-not [string]::IsNullOrWhiteSpace($UpstreamRef)) {
    Write-Host "[prepare] checking out requested upstream ref: $UpstreamRef"
    Invoke-Git -C $UpstreamDir fetch --all --tags --prune
    Invoke-Git -C $UpstreamDir checkout $UpstreamRef
}

Write-Host ""
Write-Host "[prepare] original upstream provenance"
Write-Host -NoNewline "origin: "
Invoke-Git -C $UpstreamDir remote get-url origin
Write-Host -NoNewline "branch: "
& git -C $UpstreamDir branch --show-current
if ($LASTEXITCODE -ne 0) { throw "git branch --show-current failed" }
Write-Host -NoNewline "commit: "
Invoke-Git -C $UpstreamDir rev-parse HEAD
Write-Host "status:"
Invoke-Git -C $UpstreamDir status --short
Write-Host ""
Write-Host "[prepare] done. Do not install tobii-pytracker from the examples repository."
