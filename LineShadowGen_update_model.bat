:modelupdate
echo.
echo ■ モデルの更新 ■
echo.
echo Ｑ．実行しますか？？
echo 　　　YES の場合は y と入力して Enter を押してください
echo 　　　No の場合はそのまま Enter を押すか、ウィンドウを閉じてください
echo.
SET /P selected= ⇒ 
echo.
if /i {%selected%}=={y} (goto :modelDL)
if /i {%selected%}=={Y} (goto :modelDL)
echo.
goto EXIT

:modelDL
rmdir /s /q Models
python Scripts/models_dl.py

:EXIT
echo.
echo.
echo 更新作業を終了します
echo.
echo.
pause
exit