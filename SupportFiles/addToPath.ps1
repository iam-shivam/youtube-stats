 Param(
   [Parameter(Mandatory=$true)]
   [string]$newPath
)

$oldPath = [Environment]::GetEnvironmentVariable('path', 'machine');
[Environment]::SetEnvironmentVariable('path', "$($newPath);$($oldPath)",'machine');