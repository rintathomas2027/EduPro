@echo off
cd /d c:\eduport
echo ==============================================
echo Automating Git: Adding, Committing, and Pushing to EduPro
echo ==============================================
git status
git add .
git commit -m "Complete EduPro Learner Analytics project and reports"
git branch -M main
git push -u origin main
echo ==============================================
echo DONE!
pause
