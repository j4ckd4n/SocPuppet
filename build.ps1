param(
  $config_file = ".\config.json"
)

$version = (Get-Content $config_file | ConvertFrom-Json).version

Write-Output "[BUILD]: Running 'pyinstaller' against SocPuppet.spec"
.\\.venv\\Scripts\\pyinstaller.exe .\SocPuppet.spec --noconfirm

Write-Output "[BUILD]: Copying over required files to the dist folder"
Copy-Item -Recurse .\.venv\Lib\site-packages\gpt4all\* .\dist\SocPuppet\gpt4all\ -Verbose
Copy-Item -Recurse .\.venv\Lib\site-packages\grapheme\* .\dist\SocPuppet\grapheme\ -Verbose
Copy-Item .\config.json .\dist\SocPuppet -Verbose

Write-Output "[BUILD]: Creating a zip SocPuppet-$version.zip"
if (Test-Path -Path ".\dist\SocPuppet-$version.zip") {
  Remove-Item -Path ".\dist\SocPuppet-$version.zip" -Verbose -Confirm
}

Compress-Archive .\dist\SocPuppet ".\dist\SocPuppet-$version.zip"
Remove-Item -Recurse -Force .\dist\SocPuppet