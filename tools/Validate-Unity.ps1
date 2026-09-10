param(
    [ValidateSet('BuildWindows', 'BuildAndroidApk', 'Tests', 'SnapshotOnly')]
    [string]$Action = 'BuildWindows',
    [string]$EditorPath = 'C:\Program Files\Unity\Hub\Editor\6000.6.0f1\Editor\Unity.exe',
    [string]$SnapshotPath = '',
    # Reutiliza el snapshot automatico mas reciente en vez de crear uno nuevo. Es el modo por
    # defecto porque una carpeta nueva obliga a Unity a reimportar los ~6500 assets de los
    # paquetes desde cero: veinticinco minutos por validacion, la mayoria en importar iconos
    # del Memory Profiler. Reutilizando, la Library sigue caliente y la vuelta baja a minutos.
    # Con -FreshSnapshot se fuerza la copia limpia, que es lo que hay que hacer cuando se
    # sospecha de la propia cache de importacion.
    [switch]$FreshSnapshot
)
$ErrorActionPreference = 'Stop'
$frutiRepository = Split-Path -Parent $PSScriptRoot
$frutiSource = Join-Path $frutiRepository 'FrutiCity'
$frutiValidationRoot = [IO.Path]::GetFullPath((Join-Path $frutiRepository '.validation'))
if ([string]::IsNullOrWhiteSpace($SnapshotPath)) {
    $frutiWarm = $null
    if (-not $FreshSnapshot -and (Test-Path -LiteralPath $frutiValidationRoot)) {
        $frutiWarm = Get-ChildItem -LiteralPath $frutiValidationRoot -Directory |
            Where-Object { $_.Name -match '^unity-\d{8}-\d{6}$' -and (Test-Path -LiteralPath (Join-Path $_.FullName 'Library')) } |
            Sort-Object Name -Descending | Select-Object -First 1
    }
    if ($frutiWarm) { $SnapshotPath = $frutiWarm.FullName }
    else { $SnapshotPath = Join-Path $frutiValidationRoot ('unity-' + (Get-Date -Format 'yyyyMMdd-HHmmss')) }
}
$frutiSnapshot = [IO.Path]::GetFullPath($SnapshotPath)
if (-not $frutiSnapshot.StartsWith($frutiValidationRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'The validation snapshot must be inside the repository .validation folder.'
}
if (-not (Test-Path -LiteralPath $EditorPath -PathType Leaf)) { throw "Unity Editor not found: $EditorPath" }
# Cada ejecucion deja una copia completa del proyecto, Library incluida. Treinta y cinco de
# ellas llenaron el disco y el build murio con ENOSPC resolviendo paquetes, sin un solo
# "error CS" en el log. Solo se podan las carpetas con nombre automatico: las que alguien
# ha bautizado a mano (fruticity2-phase1, unity-mobile-mono) se quedan.
if (Test-Path -LiteralPath $frutiValidationRoot) {
    Get-ChildItem -LiteralPath $frutiValidationRoot -Directory |
        Where-Object { $_.Name -match '^unity-\d{8}-\d{6}$' -and $_.FullName -ne $frutiSnapshot } |
        Sort-Object Name -Descending |
        ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
}
New-Item -ItemType Directory -Force -Path $frutiSnapshot | Out-Null
foreach ($frutiFolder in @('Assets', 'Packages', 'ProjectSettings')) {
    # /MIR y no /E: al reutilizar el snapshot, un script borrado en el proyecto sobreviviria
    # en la copia y Unity compilaria la clase dos veces. Solo espeja esas tres carpetas;
    # Library es hermana suya y no la toca, que es justo lo que la mantiene caliente.
    & robocopy (Join-Path $frutiSource $frutiFolder) (Join-Path $frutiSnapshot $frutiFolder) /MIR /R:1 /W:1 /NFL /NDL /NJH /NJS /NP
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
