@echo off
REM TruthLens-UA one-click MVP demo launcher (Windows)
REM Usage: double-click or run in cmd:
REM   run_mvp_demo.bat local   - local API + dashboard
REM   run_mvp_demo.bat render  - Render API + dashboard

set MODE=%1
if "%MODE%"=="" set MODE=render

powershell -ExecutionPolicy Bypass -File "scripts\run_mvp_demo.ps1" -Mode %MODE%

