mv requirements.txt.bk requirements.txt 
python3 -m pip install -r requirements.txt
gunicorn analysisapi.wsgi --log-file -
