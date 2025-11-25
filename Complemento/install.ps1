# Script de Instalación Inteligente - Chatbot Importaciones v5.0
# Ejecuta esto en PowerShell: .\install.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🚀 INSTALACIÓN CHATBOT IMPORTACIONES V5.0" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Paso 1: Verificar Python
Write-Host "📍 Paso 1: Verificando versión de Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "   $pythonVersion" -ForegroundColor Green

if ($pythonVersion -match "Python 3\.([0-9]+)\.") {
    $minorVersion = [int]$matches[1]
    if ($minorVersion -ge 9 -and $minorVersion -le 11) {
        Write-Host "   ✅ Versión compatible`n" -ForegroundColor Green
    } elseif ($minorVersion -ge 12) {
        Write-Host "   ⚠️  Python 3.12+ puede tener problemas. Recomendado: 3.9-3.11`n" -ForegroundColor Yellow
    }
}

# Paso 2: Actualizar pip
Write-Host "📍 Paso 2: Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
Write-Host "   ✅ pip actualizado`n" -ForegroundColor Green

# Paso 3: Instalar dependencias básicas primero
Write-Host "📍 Paso 3: Instalando dependencias básicas..." -ForegroundColor Yellow
$basicPackages = @(
    "python-dotenv",
    "pandas",
    "requests"
)

foreach ($package in $basicPackages) {
    Write-Host "   📦 Instalando $package..." -ForegroundColor Cyan
    pip install $package --quiet
}
Write-Host "   ✅ Dependencias básicas instaladas`n" -ForegroundColor Green

# Paso 4: Instalar Streamlit
Write-Host "📍 Paso 4: Instalando Streamlit..." -ForegroundColor Yellow
pip install "streamlit>=1.31.0,<2.0.0"
Write-Host "   ✅ Streamlit instalado`n" -ForegroundColor Green

# Paso 5: Instalar Supabase (con dependencias automáticas)
Write-Host "📍 Paso 5: Instalando Supabase..." -ForegroundColor Yellow
pip install "supabase>=2.3.0,<3.0.0"
Write-Host "   ✅ Supabase instalado (gotrue y httpx incluidos)`n" -ForegroundColor Green

# Paso 6: Instalar AI Providers
Write-Host "📍 Paso 6: Instalando AI Providers..." -ForegroundColor Yellow
pip install "openai>=1.10.0,<2.0.0"
pip install "groq>=0.4.0,<1.0.0"
Write-Host "   ✅ OpenAI y Groq instalados`n" -ForegroundColor Green

# Paso 7: Instalar LangChain (versiones específicas)
Write-Host "📍 Paso 7: Instalando LangChain Stack..." -ForegroundColor Yellow
Write-Host "   ⚠️  Instalando versiones específicas (0.1.x)..." -ForegroundColor Yellow

$langchainPackages = @(
    "langchain==0.1.4",
    "langchain-core==0.1.16",
    "langchain-community==0.0.16",
    "langchain-openai==0.0.5"
)

foreach ($package in $langchainPackages) {
    Write-Host "   📦 Instalando $package..." -ForegroundColor Cyan
    pip install $package --quiet
}
Write-Host "   ✅ LangChain instalado`n" -ForegroundColor Green

# Paso 8: Instalar Database Connectors
Write-Host "📍 Paso 8: Instalando PostgreSQL connectors..." -ForegroundColor Yellow
pip install "SQLAlchemy>=2.0.0,<3.0.0"
pip install "psycopg2-binary>=2.9.0"
Write-Host "   ✅ Connectors instalados`n" -ForegroundColor Green

# Paso 9: Verificar instalación
Write-Host "📍 Paso 9: Verificando instalación..." -ForegroundColor Yellow

$criticalPackages = @(
    "streamlit",
    "supabase",
    "openai",
    "groq",
    "langchain",
    "pandas",
    "sqlalchemy",
    "psycopg2"
)

$allInstalled = $true
foreach ($package in $criticalPackages) {
    $installed = pip show $package 2>&1
    if ($installed -match "Name:") {
        Write-Host "   ✅ $package" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $package - NO INSTALADO" -ForegroundColor Red
        $allInstalled = $false
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
if ($allInstalled) {
    Write-Host "✅ INSTALACIÓN COMPLETA" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Cyan
    
    Write-Host "🎯 Próximos pasos:" -ForegroundColor Yellow
    Write-Host "   1. Ejecuta: python Diagnostico.py" -ForegroundColor White
    Write-Host "   2. Si todo OK: streamlit run app.py`n" -ForegroundColor White
} else {
    Write-Host "⚠️  INSTALACIÓN INCOMPLETA" -ForegroundColor Yellow
    Write-Host "========================================`n" -ForegroundColor Cyan
    Write-Host "Algunos paquetes fallaron. Intenta instalarlos manualmente.`n" -ForegroundColor Red
}

pause
