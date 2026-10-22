# Experimental interactive local chat; does not enable any project AI profile.
$ErrorActionPreference = 'Stop'
$ollamaSmallExecutable = Join-Path $env:LOCALAPPDATA 'Programs\Ollama\ollama.exe'
if (-not (Test-Path -LiteralPath $ollamaSmallExecutable -PathType Leaf)) {
    throw 'The installed Ollama executable was not found.'
}
$ollamaSmallMemory = Get-CimInstance Win32_OperatingSystem
if ($ollamaSmallMemory.FreePhysicalMemory -lt (3584 * 1024)) {
    throw 'Small-model chat needs at least 3.5 GiB available RAM for its measured reservation and headroom.'
}
$ollamaSmallPreviousHost = $env:OLLAMA_HOST
$ollamaSmallPreviousCloud = $env:OLLAMA_NO_CLOUD
try {
    $env:OLLAMA_HOST = '127.0.0.1:11434'
    $env:OLLAMA_NO_CLOUD = '1'
    & $ollamaSmallExecutable run ppm-small --think=false --keepalive 0
    $ollamaSmallExit = $LASTEXITCODE
} finally {
    $env:OLLAMA_HOST = $ollamaSmallPreviousHost
    $env:OLLAMA_NO_CLOUD = $ollamaSmallPreviousCloud
}
exit $ollamaSmallExit
