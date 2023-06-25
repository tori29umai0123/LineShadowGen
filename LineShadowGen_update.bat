@echo off
:update
echo.
echo ■ LineShadowGenの更新 ■
echo.
echo Ｑ．実行しますか？？
echo 　　　YES の場合は y と入力して Enter を押してください
echo 　　　No の場合はそのまま Enter を押すか、ウィンドウを閉じてください
echo.
SET /P selected= ⇒ 
echo.
if /i "%selected%"=="y" (goto :start)
if /i "%selected%"=="Y" (goto :start)
echo.
goto EXIT

:start
::更新
git pull https://github.com/tori29umai0123/LineShadowGen.git

:: 更新した後、LineShadowGen_update.batを以前のバージョンに戻します。
git checkout HEAD -- LineShadowGen_update.bat

pip install --use-pep517 --upgrade -r requirements.txt
pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

:EXIT
echo.
echo.
echo 更新作業を終了します
echo.
echo.
pause
exit