Set-Location $PSScriptRoot

$agents = @(64, 128, 256, 512, 1024, 2048)
$files = Get-Item ..\input\*

& C:\Users\ipzwi\.virtualenvs\aoin-aco-max-clique\Scripts\activate.ps1

for ($file_idx = 0; $file_idx -lt $files.Length; $file_idx++)
{
    Write-Progress -Activity "File" -Status $files[$file_idx] -PercentComplete (($file_idx/$files.Length)*100) -Id 0
    for ($agents_idx = 0; $agents_idx -lt $agents.Length; $agents_idx++)
    {
        Write-Progress -Activity "Agents" -Status $agents[$agents_idx] -PercentComplete (($agents_idx/$agents.Length)*100) -Id 1 -ParentId 0
        for ($i = 0; $i -lt 100; $i++) {
            $agents_count = $agents[$agents_idx]
            $fname = $files[$file_idx].BaseName
            Write-Progress -Activity 'Repeats' -Status $i -PercentComplete $i -Id 2 -ParentId 1
            New-item ..\output\ref\$fname.csv -Force
            python ..\main.py --input $files[$file_idx] --output ..\output\ref\$fname.csv ref --agents $agents_count > execution.log
        }
    }
}