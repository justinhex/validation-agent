@echo off

cd /d %~dp0
cmake -S dut -B dut/build -G "Visual Studio 18 2026" -A x64
cmake --build dut/build --config Release

pause