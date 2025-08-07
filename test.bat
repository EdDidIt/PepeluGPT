@echo off
REM PepeluGPT Test Commands for Windows
REM Usage: test.bat [type]
REM Types: all, unit, integration, core, plugins, demo, coverage

setlocal

if "%1"=="" (
    echo 🧪 Running all tests...
    python tests\run_tests.py --all
    goto :end
)

if "%1"=="all" (
    echo 🧪 Running all tests...
    python tests\run_tests.py --all
    goto :end
)

if "%1"=="unit" (
    echo 🧪 Running unit tests...
    python tests\run_tests.py --unit
    goto :end
)

if "%1"=="integration" (
    echo 🧪 Running integration tests...
    python tests\run_tests.py --integration
    goto :end
)

if "%1"=="core" (
    echo 🧪 Running core functionality tests...
    python -m pytest tests\unit\core\ -v
    goto :end
)

if "%1"=="plugins" (
    echo 🧪 Running plugin tests...
    python -m pytest tests\unit\plugins\ -v
    goto :end
)

if "%1"=="demo" (
    echo 🧪 Running demo/showcase tests...
    python tests\run_tests.py --demo
    goto :end
)

if "%1"=="coverage" (
    echo 🧪 Running tests with coverage report...
    python -m pytest --cov=. --cov-report=html --cov-report=term tests\
    goto :end
)

echo ❌ Unknown test type: %1
echo Available types: all, unit, integration, core, plugins, demo, coverage

:end
endlocal
