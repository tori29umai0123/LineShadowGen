:modelupdate
echo.
echo �� ���f���̍X�V ��
echo.
echo �p�D���s���܂����H�H
echo �@�@�@YES �̏ꍇ�� y �Ɠ��͂��� Enter �������Ă�������
echo �@�@�@No �̏ꍇ�͂��̂܂� Enter ���������A�E�B���h�E����Ă�������
echo.
SET /P selected= �� 
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
echo �X�V��Ƃ��I�����܂�
echo.
echo.
pause
exit