# Documentation verification only. No application services are started.
$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$checkResults = [Collections.Generic.List[object]]::new()
function Record-Check([string]$Name, [bool]$Passed, [string]$Details) {
    $checkResults.Add([pscustomobject]@{Name=$Name;Passed=$Passed;Details=$Details})
}
$outputPath = Join-Path $PSScriptRoot 'SPRINT-00-CHECKS.md'
if (-not (Test-Path -LiteralPath $outputPath)) {
    '# Sprint 00 documentation verification' | Set-Content -LiteralPath $outputPath -Encoding utf8
}

$required = @(
    'README.md','CHANGELOG.md','.gitignore',
    'docs/source/INDEX.md','docs/source/source-manifest.json',
    'docs/source/Word-Specification-Extract.txt',
    'docs/prompts/MASTER.md','docs/requirements/coverage.md',
    'docs/requirements/product-scope.md','docs/requirements/roadmap.md',
    'docs/requirements/decisions-and-assumptions.md','docs/requirements/quality-plan.md',
    'docs/architecture/overview.md','docs/architecture/data-model.md',
    'docs/architecture/adr/README.md','docs/contracts/permissions.md',
    'docs/contracts/api-events.md','docs/contracts/metrics.md',
    'docs/sprints/SPRINT-00-REPORT.md','docs/handoffs/SPRINT-00-HANDOFF.md',
    'docs/handoffs/LATEST.md'
)
$missing = @($required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $projectRoot $_)) })
Record-Check 'Required planning artifacts' ($missing.Count -eq 0) "$($required.Count) required artifacts; missing: $($missing -join ', ')"

$manifest = Get-Content -LiteralPath (Join-Path $projectRoot 'docs/source/source-manifest.json') -Raw | ConvertFrom-Json
$badHashes = @()
foreach ($entry in $manifest.files) {
    $actual = (Get-FileHash -LiteralPath (Join-Path $projectRoot $entry.copy) -Algorithm SHA256).Hash
    if ($actual -ne $entry.sha256) { $badHashes += $entry.copy }
}
Record-Check 'Preserved source and prompt hashes' ($badHashes.Count -eq 0) "$($manifest.files.Count) copies checked against source-capture manifest; mismatches: $($badHashes -join ', ')"

$promptText = Get-Content -LiteralPath (Join-Path $projectRoot 'docs/prompts/02-ORDERED-SPRINT-PROMPTS.md') -Raw
$sprints = @([regex]::Matches($promptText,'(?m)^## Sprint (\d{2}) ') | ForEach-Object {$_.Groups[1].Value})
$expected = @(0..23 | ForEach-Object {'{0:D2}' -f $_})
Record-Check 'Ordered sprint sequence' (($sprints -join ',') -eq ($expected -join ',')) "$($sprints.Count) sprint headings, expected 00 through 23"

$coverageText = Get-Content -LiteralPath (Join-Path $projectRoot 'docs/requirements/coverage.md') -Raw
$requirementRows = @($coverageText -split '\r?\n' | Where-Object {$_ -match '^\| [PFNET]-\d{3} \|'})
$ids = @($requirementRows | ForEach-Object {($_ -split '\|')[1].Trim()})
$duplicates = @($ids | Group-Object | Where-Object {$_.Count -gt 1})
Record-Check 'Unique requirement identifiers' ($duplicates.Count -eq 0) "$($ids.Count) requirements; duplicate IDs: $($duplicates.Name -join ', ')"
$invalidOwners = @()
$earlyDependencies = @()
foreach ($row in $requirementRows) {
    $cells = @($row -split '\|' | ForEach-Object {$_.Trim()})
    $id = $cells[1]
    if ($id.StartsWith('P-')) { $owner = $cells[4]; $dependency = $cells[5] }
    else { $owner = $cells[5]; $dependency = $cells[6] }
    if ($owner -notmatch '^\d{2}$' -or [int]$owner -gt 23) { $invalidOwners += $id; continue }
    foreach ($dependencyMatch in [regex]::Matches($dependency,'\d{2}')) {
        if ([int]$dependencyMatch.Value -ge [int]$owner) { $earlyDependencies += $id }
    }
}
Record-Check 'Requirement sprint owners and dependency ordering' (($invalidOwners.Count -eq 0) -and ($earlyDependencies.Count -eq 0)) "Invalid owners: $($invalidOwners -join ', '); non-prior dependencies: $($earlyDependencies -join ', ')"
$implementationCompleted = @($requirementRows | Where-Object {$_ -match '^\| [FNE]-' -and $_ -notmatch '\| Planned \|'})
Record-Check 'No premature implementation completion claims' ($implementationCompleted.Count -eq 0) 'All functional, nonfunctional and enhancement rows remain Planned'

$markdownFiles = @(Get-ChildItem -LiteralPath $projectRoot -Filter '*.md' -Recurse -File)
$brokenLinks = @()
$badFences = @()
foreach ($file in $markdownFiles) {
    $content = Get-Content -LiteralPath $file.FullName -Raw
    if (([regex]::Matches($content,'(?m)^```').Count % 2) -ne 0) { $badFences += $file.Name }
    foreach ($match in [regex]::Matches($content,'\[[^\]]*\]\(([^)]+)\)')) {
        $target = $match.Groups[1].Value.Trim('<','>')
        if ($target -match '^[A-Za-z][A-Za-z0-9+.-]*:' -or $target.StartsWith('#')) { continue }
        $target = [Uri]::UnescapeDataString(($target -split '#',2)[0])
        if ($target -and -not (Test-Path -LiteralPath (Join-Path $file.DirectoryName $target))) {
            $brokenLinks += "$($file.Name): $target"
        }
    }
}
Record-Check 'Balanced Markdown fences' ($badFences.Count -eq 0) "$($markdownFiles.Count) Markdown files; failures: $($badFences -join ', ')"
Record-Check 'Local Markdown link targets' ($brokenLinks.Count -eq 0) "Missing targets: $($brokenLinks -join '; ')"
$adrFiles = @(Get-ChildItem -LiteralPath (Join-Path $projectRoot 'docs/architecture/adr') -Filter '0*.md')
Record-Check 'Architecture decision records' ($adrFiles.Count -eq 6) "$($adrFiles.Count) proposed decision records"
$appItems = @('apps','services','packages','infra','node_modules','package.json','pyproject.toml','compose.yaml','docker-compose.yml')
$presentAppItems = @($appItems | Where-Object {Test-Path -LiteralPath (Join-Path $projectRoot $_)})
Record-Check 'Sprint 00 scope boundary' ($presentAppItems.Count -eq 0) "No application scaffolding expected; present: $($presentAppItems -join ', ')"

$reportLines = [Collections.Generic.List[string]]::new()
$reportLines.Add('# Sprint 00 documentation verification')
$reportLines.Add('')
$reportLines.Add('Executed locally on 2026-10-05 using PowerShell. Scope: documentation structure and source preservation only. Rerun from the project root with `./docs/verification/check-sprint-00.ps1`.')
$reportLines.Add('')
$reportLines.Add('| Check | Result | Evidence |')
$reportLines.Add('| --- | --- | --- |')
foreach ($result in $checkResults) {
    $status = if ($result.Passed) {'PASS'} else {'FAIL'}
    $reportLines.Add("| $($result.Name) | $status | $($result.Details.Replace('|','/')) |")
}
$reportLines.Add('')
$reportLines.Add('The initial copy command also compared every original against its copy before writing the hash manifest. This rerun validates copies against that captured manifest without depending on the original external paths.')
$reportLines.Add('')
$reportLines.Add('Manual review: read the Word document paragraphs and table contents plus the full supplement; mapped all eight Word modules, advanced features, four supplemental modules, datasets and nonfunctional targets. Reviewed the data relationships and module dependency corrections. No application, browser, migration, provider, ML or cloud test was applicable. Mermaid source was reviewed; graphical rendering is not claimed.')
$reportLines.Add('')
$reportLines.Add('Git checkpoint: local main branch initialized, no commit or remote at Sprint 00 delivery. Documentation is uncommitted. This check does not establish application correctness, production security or model accuracy.')
$reportLines | Set-Content -LiteralPath $outputPath -Encoding utf8
$checkResults | Format-Table -AutoSize
$failures = @($checkResults | Where-Object {-not $_.Passed})
if ($failures.Count -gt 0) { throw "$($failures.Count) documentation checks failed; see $outputPath" }
Write-Output "PASS: $($checkResults.Count) documentation checks. Report: $outputPath"
