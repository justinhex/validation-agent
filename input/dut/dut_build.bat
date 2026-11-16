@echo off

cd /d %~dp0
cmake -S . -B build -G "Visual Studio 18 2026" -A x64
cmake --build build --config Release

pause