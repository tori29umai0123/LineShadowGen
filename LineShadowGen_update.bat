:update
echo.
echo �� LineShadowGen�̍X�V ��
echo.
echo �p�D���s���܂����H�H
echo �@�@�@YES �̏ꍇ�� y �Ɠ��͂��� Enter �������Ă�������
echo �@�@�@No �̏ꍇ�͂��̂܂� Enter ���������A�E�B���h�E����Ă�������
echo.
SET /P selected= �� 
echo.
if /i {%selected%}=={y} (goto :start)
if /i {%selected%}=={Y} (goto :start)
echo.
goto EXIT

:start
git pull https://github.com/tori29umai0123/LineShadowGen.git
call venv\Scripts\activate.bat
pip install --use-pep517 --upgrade -r requirements.txt
pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
goto modelupdate

:EXIT
echo.
echo.
echo �X�V��Ƃ��I�����܂�
echo.
echo.
pause
exit