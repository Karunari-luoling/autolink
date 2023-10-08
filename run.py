import os

os.system('nohup `python3 -u getDate.py > getDate.out 2>&1` &')
os.system('nohup `python3 -u app.py > app.out 2>&1` &')
