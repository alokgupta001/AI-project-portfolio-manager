$ErrorActionPreference = 'Stop'
$docPath = 'C:\Users\alokg\OneDrive\Documents\Codex\Enterprise PPM Presentation Guide.docx'
$pdfPath = 'C:\Users\alokg\OneDrive\Documents\Codex\artifacts\ppm-presentation-guide\word-layout.pdf'
$wordApp = $null
$wordDocument = $null
try {
    $wordApp = New-Object -ComObject Word.Application
    $wordApp.Visible = $false
    $wordApp.DisplayAlerts = 0
    $wordDocument = $wordApp.Documents.Open($docPath, $false, $true, $false)
    $wordDocument.Repaginate()
    $wordDocument.ExportAsFixedFormat($pdfPath, 17)
    Write-Output ('Exported ' + $pdfPath)
} finally {
    if ($null -ne $wordDocument) { $wordDocument.Close(0) }
    if ($null -ne $wordApp) { $wordApp.Quit() }
}
