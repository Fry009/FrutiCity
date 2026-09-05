param(
    [ValidateSet('BuildWindows', 'BuildAndroidApk', 'Tests', 'SnapshotOnly')]
    [string]$Action = 'BuildWindows',
    [string]$EditorPath = 'C:\Program Files\Unity\Hub\Editor\6000.6.0f1\Editor\Unity.exe',
    [string]$SnapshotPath = ''
)
$ErrorActionPreference = 'Stop'
$frutiRepository = Split-Path -Parent $PSScriptRoot
$frutiSource = Join-Path $frutiRepository 'FrutiCity'
$frutiValidationRoot = [IO.Path]::GetFullPath((Join-Path $frutiRepository '.validation'))
if ([string]::IsNullOrWhiteSpace($SnapshotPath)) {
    $SnapshotPath = Join-Path $frutiValidationRoot ('unity-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
}
$frutiSnapshot = [IO.Path]::GetFullPath($SnapshotPath)
if (-not $frutiSnapshot.StartsWith($frutiValidationRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'The validation snapshot must be inside the repository .validation folder.'
}
if (-not (Test-Path -LiteralPath $EditorPath -PathType Leaf)) { throw "Unity Editor not found: $EditorPath" }
New-Item -ItemType Directory -Force -Path $frutiSnapshot | Out-Null
foreach ($frutiFolder in @('Assets', 'Packages', 'ProjectSettings')) {
    & robocopy (Join-Path $frutiSource $frutiFolder) (Join-Path $frutiSnapshot $frutiFolder) /E /R:1 /W:1 /NFL /NDL /NJH /NJS /NP
    if ($LASTEXITCODE -ge 8) { throw "Snapshot copy failed: $frutiFolder" }
}
Write-Output "Validation snapshot: $frutiSnapshot"
if ($Action -eq 'SnapshotOnly') { exit 0 }
$frutiArtifactRoot = Join-Path $frutiRepository 'artifacts'
New-Item -ItemType Directory -Force -Path $frutiArtifactRoot | Out-Null
$frutiLog = Join-Path $frutiArtifactRoot ('unity-' + $Action.ToLowerInvariant() + '.log')
$frutiArguments = @('-batchmode', '-nographics', '-projectPath', $frutiSnapshot, '-logFile', $frutiLog)
if ($Action -eq 'Tests') {
    $frutiArguments += @('-runTests', '-testPlatform', 'EditMode', '-testResults', (Join-Path $frutiArtifactRoot 'editmode-results.xml'))
} elseif ($Action -eq 'BuildAndroidApk') {
    $frutiArguments += @('-buildTarget', 'Android', '-quit', '-executeMethod', 'FrutiCity.Editor.ProjectBuilder.BuildAndroidApk')
} else {
    $frutiArguments += @('-buildTarget', 'Win64', '-quit', '-executeMethod', 'FrutiCity.Editor.ProjectBuilder.ValidateAndBuild')
}
$frutiPreviousOutput = $env:FRUTICITY_BUILD_OUTPUT
try {
    $env:FRUTICITY_BUILD_OUTPUT = Join-Path $frutiRepository 'FrutiCity/Builds'
    # Windows paths cannot contain double quotes; quote every argument to preserve spaces.
    $frutiLaunchArguments = $frutiArguments | ForEach-Object { '"' + $_ + '"' }
    # Run the isolated project, never another instance of the user's open project.
    $frutiProcess = Start-Process -FilePath $EditorPath -ArgumentList $frutiLaunchArguments -WindowStyle Hidden -Wait -PassThru
    if ($frutiProcess.ExitCode -ne 0) { throw "Unity exited with $($frutiProcess.ExitCode). See $frutiLog" }
} finally {
    if ($null -eq $frutiPreviousOutput) { Remove-Item Env:FRUTICITY_BUILD_OUTPUT -ErrorAction SilentlyContinue }
    else { $env:FRUTICITY_BUILD_OUTPUT = $frutiPreviousOutput }
}
Write-Output "Unity $Action completed. Log: $frutiLog"
