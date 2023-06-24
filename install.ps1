Set-Location $PSScriptRoot

$Env:PIP_DISABLE_PIP_VERSION_CHECK = 1

if (!(Test-Path -Path "venv")) {
    Write-Output  "Creating venv for python..."
    python -m venv venv
}
.\venv\Scripts\activate

Write-Output "Installing deps..."
pip install --upgrade -r requirements.txt

Write-Output "Installing torch+cuda"
pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

$modelsDirectory = "Models"
if (!(Test-Path -Path $modelsDirectory)) {
    Write-Output "Creating Models directory..."
    New-Item -ItemType Directory -Path $modelsDirectory | Out-Null
}

Write-Output "Downloading models"
python "Scripts/models_dl.py"

Write-Output "Install completed"
Read-Host | Out-Null ;