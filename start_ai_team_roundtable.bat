@echo off
REM 启动 AI 6人圆桌讨论 - 圆桌版本

echo.
echo ========================================
echo   AI 6人圆桌讨论大会
echo   圆桌版本
echo ========================================
echo.

cd /d D:\aiwork
python -m streamlit run ai_team_roundtable.py

pause
