@echo off
REM Batch file to automate git add, commit, and push

REM Stage all changes
git add .

REM Commit with a timestamped message
set dt=%date:~10,4%-%date:~4,2%-%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
git commit -m "Automated commit %dt%"

REM Push to GitHub
git push origin main

REM Show status
git status
