@echo off
REM AI 6人圆桌讨论 - 主启动脚本

echo.
echo ========================================
echo   AI 6人圆桌讨论大会
echo   主启动脚本
echo ========================================
echo.

cd /d D:\aiwork

echo 启动圆桌讨论版本...
python -m streamlit run ai_team_roundtable.py

pause
