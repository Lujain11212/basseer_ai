$ErrorActionPreference = "Stop"
$ProjectDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectDir

Write-Host "🛡️  بصير AI – الحارس الدلالي v2" -ForegroundColor Cyan

if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env"; Write-Host "📄 .env created" }
if (-not (Test-Path "venv")) { python -m venv venv }
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt -q

python scripts/generate_dataset.py
$backend = Start-Process python -ArgumentList "-m","uvicorn","backend.main:app","--host","127.0.0.1","--port","8000","--reload" -PassThru -NoNewWindow
Start-Sleep 3
python scripts/ingest_dataset.py
$dash = Start-Process python -ArgumentList "-m","streamlit","run","dashboard/app.py","--server.port","8501","--server.headless","true" -PassThru -NoNewWindow

Write-Host "`n✅ Backend: http://127.0.0.1:8000  |  Dashboard: http://127.0.0.1:8501" -ForegroundColor Green
Write-Host "Press any key to stop..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Stop-Process -Id $backend.Id -Force -EA SilentlyContinue
Stop-Process -Id $dash.Id -Force -EA SilentlyContinue
