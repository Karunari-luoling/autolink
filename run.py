import os

os.system('nohup python3 -u src/getData.py > getData.out 2>&1 &')
os.system('nohup python3 -u src/app.py > app.out 2>&1 &')
