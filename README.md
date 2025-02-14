# Venix

A 4WD menacum wheel car for raspberry pi

---

## Table of Contents

1. [About](#about-venix)
2. [Features](#features)
3. [Part List (Build your own)](#part-list)
4. [Getting Started](#getting-started)
5. [Usage](#usage)
6. [License](LICENSE)

---

## About Venix

### Description

**Venix** is a custom-built, versatile 4WD robot car designed to showcase the power of precision control and adaptability in motion. At its core, Venix features a set of mecanum wheels that provide omnidirectional mobility, enabling smooth movement in any direction, including diagonal and rotational paths. Powered by a Raspberry Pi Zero W, Venix relies on cutting-edge technology to execute commands and process data seamlessly. The car’s sleek design and impressive capabilities make it ideal for robotics enthusiasts looking to explore advanced locomotion.

The heart of Venix’s drive system lies in its motor control setup. Each of the four 12V motors is controlled by two Cytron MDD3A dual-channel motor drivers, ensuring robust and efficient operation. These motor drivers, in turn, are managed by a PCA9685 PWM controller, allowing for precise speed and direction adjustments. This integration guarantees smooth transitions and responsive handling, critical for the precise movements required by mecanum-wheel systems. The 12V power supply is delivered through a reliable pack of AA batteries, ensuring portability and ample energy to sustain long operating sessions.

Control over Venix is achieved wirelessly using a game controller, which offers intuitive and responsive command input. This wireless interface enables seamless interaction with the Raspberry Pi, allowing users to control forward, backward, lateral, and rotational movements effortlessly. The programming logic is fine-tuned to interpret the controller’s inputs and convert them into synchronized motor operations, ensuring the car responds accurately to even the most complex navigation demands.

Venix’s ability to combine movement vectors—such as forward motion with simultaneous rotation—is a standout feature that underscores its advanced capabilities. The robot calculates motor values dynamically through a custom function, which processes input parameters. These are multiplied by a speed factor, enabling Venix to adjust its responsiveness and adapt to various terrains or operational requirements. This level of control ensures a seamless blend of agility and stability.

Built for exploration and experimentation, Venix serves as both a learning platform and a showcase of engineering ingenuity. Its modular design allows for easy modifications and upgrades, making it a perfect candidate for integrating sensors, cameras, or additional functionality. Whether used for educational purposes, competitions, or personal projects, Venix is a testament to the creativity and precision that define modern robotics.


### Built With

- [Python](https://www.python.org/)
- [luma.oled](https://pypi.org/project/luma.oled/)
- [1.3" OLED Driven by luma.oled](https://thepihut.com/products/1-3-oled-display-module-128x64)
- [PCA9685](https://thepihut.com/products/16-channel-servo-driver-hat-for-raspberry-pi-12-bit-i2c?variant=32138518364222)
- [PCA9685 Custom library](pca9685.py)
- [Cytron MDD3A driven by PCA9685](https://thepihut.com/products/3a-4v-16v-2-channel-dc-motor-driver?variant=31985056907326)
- [ThePiHut Custom game controller](https://thepihut.com/products/raspberry-pi-compatible-wireless-gamepad-controller) 

---

## Features

- ✅ **Feedback:** OLED Displaying information
- ✅ **Precise:** With axis combined movments, you can drive anywhere!
- ✅ **Relaible:** Rated for 6 months of downtime
- ✅ **Input:** Custom ThePiHut USB wireless controller
- 🛜 **Roaming mode:** No need for wi-fi, driven by a wireless gamepad
- 🍓 **Main chip:** The powerful yet small Raspberry Pi Zero 2W
- 🔌 **Power supply:** Eight AA in series to produce a whopping 12V
- 🛞 **Wheels:** Metal mecanum wheels; very strong!
- 🚀 **Motor speed:** Peaking at 380RPM@12V

---

## Part List

| Function | Component | Where to buy |
| --- | --- | --- |
| Main PSU | 8x AA @ 12V | [ThePiHut](https://thepihut.com/products/8aa-holder)
| Main PSU cable | 9V connector clip | [ThePiHut](https://thepihut.com/products/9v-battery-connector-clip-with-bare-wires)
| Main PSU jumper cable | 2 Dupont connecter cables | [ThePiHut](https://thepihut.com/products/thepihuts-jumper-bumper-pack-120pcs-dupont-wire)
| Main computer | Raspberry Pi Zero (WH) | [ThePiHut](https://thepihut.com/products/raspberry-pi-zero-wh-with-pre-soldered-header)
| Motor | Micro metal gearmotor (1:75) (x4) | [ThePiHut](https://thepihut.com/products/micro-metal-gear-motor-with-connector-75-1)
| Motor driver | Cytron MDD3A (x2) | [ThePiHut](https://thepihut.com/products/3a-4v-16v-2-channel-dc-motor-driver?variant=31985056907326)
| PWM driver | Waveshare PCA9685 | [ThePiHut](https://thepihut.com/products/16-channel-servo-driver-hat-for-raspberry-pi-12-bit-i2c?variant=32138518364222)
| OLED | 1.3" I2C OLED | [ThePiHut](https://thepihut.com/products/1-3-oled-display-module-128x64)
| Mecanum wheels (left) | Mecanum wheels (left) (x2) | [ThePiHut](https://thepihut.com/products/metal-mecanum-wheel-with-motor-shaft-coupling-65mm-left)
| Mecanum wheels (right) | Mecanum wheels (right) (x2) | [ThePiHut](https://thepihut.com/products/metal-mecanum-wheel-with-motor-shaft-coupling-65mm-right)
| M4 screws | M4 screws for mecanum wheels (4x) | [Screwfix](https://www.screwfix.com/p/easyfix-cap-head-socket-screws-a2-stainless-steel-m4-x-16mm-50-pack/2649t)
| M3 screws | M3 screws (20x) | [ThePiHut](https://thepihut.com/products/m3-20mm-pozi-pan-head-screws)
| M3 nuts| M3 nuts (20x) | [ThePiHut](https://thepihut.com/products/m3-steel-nuts-10-pack)
| M2 screws | M2 screws (10x) | [ThePiHut](https://thepihut.com/products/nylon-slotted-cheese-head-screws-m2-x-20mm-10-pack)
| M2 nuts | M2 nuts (10x) | [ThePiHut](https://thepihut.com/products/nylon-nut-m2-10-pack)
| Motor mount | Plastic motor mount (4x) | [ThePiHut](https://thepihut.com/products/pololu-micro-metal-gearmotor-bracket-pair-black)

## Usage
- 12V, 2 hour runtime
- ~2cm distance from ground to cables (to be fixed)
- 65cm metal wheels
- Plastic frame
- Signal antenna

## Getting Started

Follow these steps to set up your project 

#### Download Raspberry Pi imager:
- [For Windows](https://downloads.raspberrypi.org/imager/imager_latest.exe)
- [For MacOS](https://downloads.raspberrypi.org/imager/imager_latest.dmg)
- [For Ubuntu for x86](https://downloads.raspberrypi.org/imager/imager_latest_amd64.deb)
- For Raspberry Pi OS ```sudo apt install rpi-imager```

#### Get the OS:
- Download [Venos](Venos)
- Click the download icon

#### Flash the OS:

Open [Raspberry Pi Imager](#download-raspberry-pi-imager). Choose the *Operating System* tab and select *Use custom*. When prompted, choose [Venos](venos.img) and flash it to the SD card that you have connected to your computer.

#### Read the OS:

When it has finished writing to the SD card, eject it and connect it to Venix.
