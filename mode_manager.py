import sys
import subprocess

select = int(sys.argv[1])
funtion = int(sys.argv[2])

l = int(sys.argv[3])
r = int(sys.argv[4])

mode = 0
modecount = 2 # Excluding passive

if select == 1:
    if 0 <= mode < modecount:
        if r == 1:
            mode += 1
    if 0 < mode <= modecount:
        if l == 1:
            mode -= 1

while True:
    subprocess.run(["python3", "Venix/oled.py", str(mode)])
