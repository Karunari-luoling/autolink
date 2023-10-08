import os

os.system('nohup python3 -u getData.py > getData.out 2>&1 &')
os.system('nohup python3 -u app.py > app.out 2>&1 &')
