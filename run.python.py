import os

os.system('nohub python3 -u getDate.py > getDate.out 2>&1 &')
os.system('nohub python3 -u app.py > app.out 2>&1 &')
