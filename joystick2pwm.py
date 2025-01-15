import sys
import subprocess

def main():
    if len(sys.argv) != 6:
        print("Usage: motor.py <axis_0> <axis_1> <axis_2> <zl> <zr>")
        return

    speed = 1
    speed = max(0, min(speed + float(sys.argv[4])/10 - float(sys.argv[5])/10, 2))

    lr = float(sys.argv[1])/2 * speed
    fb = float(sys.argv[2])/2 * speed
    r = float(sys.argv[3])/2 * speed

    m1 = fb + lr + r
    m2 = fb - lr - r
    m3 = fb - lr + r
    m4 = fb + lr - r

    subprocess.Popen(["python3", "Venix/pca9685.py", str(m1), str(m2), str(m3), str(m4)])

if __name__ == "__main__":
    main()
