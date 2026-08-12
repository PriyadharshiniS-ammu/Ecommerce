@echo off
REM Quick Start Script for ShopMart E-Commerce Application

echo.
echo ========================================
echo   ShopMart E-Commerce - Quick Start
echo ========================================
echo.

REM Install requirements
echo [1/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies. Please check your Python installation.
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [2/4] Creating database migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo Error creating migrations.
    pause
    exit /b 1
)
echo ✓ Migrations created

echo.
echo [3/4] Applying migrations...
python manage.py migrate
if errorlevel 1 (
    echo Error applying migrations.
    pause
    exit /b 1
)
echo ✓ Database ready

echo.
echo [4/4] Creating superuser (admin account)...
echo Please provide the following information:
python manage.py createsuperuser

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To start the development server, run:
echo   python manage.py runserver
echo.
echo Then open your browser and go to:
echo   http://localhost:8000
echo.
echo Admin panel:
echo   http://localhost:8000/admin
echo.
pause
