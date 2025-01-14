import sys
import subprocess

def main():
    if len(sys.argv) != 6:
        print("Usage: motor.py <axis_0> <axis_1> <axis_2>")
        return

    # Read axis data from command-line arguments
    lrRAW = float(sys.argv[1])
    fbRAW = float(sys.argv[2])
    rRAW = float(sys.argv[3])

    speed = 1

    if len(sys.argv) > 5:
        speed += float(sys.argv[4])/10 - float(sys.argv[5])/10

    speed = max(0, min(speed, 2))

    lr = round(lrRAW, 3)/2 * speed
    fb = round(fbRAW, 3)/2 * speed
    r = round(rRAW, 3)/2 * speed

    m1 = fb + lr + r
    m2 = fb - lr - r
    m3 = fb - lr + r
    m4 = fb + lr - r

    subprocess.run(["python3", "Venix/pca9685.py", str(m1), str(m2), str(m3), str(m4)])

if __name__ == "__main__":
    main()
