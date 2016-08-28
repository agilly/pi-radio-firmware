# Giving a new life to your old vintage radio using a Raspberry Pi

## Description
Here, we describe how to recycle old AM/FM radios and turn them into web-connected internet radios using a Raspberry Pi.

## Configuring the Pi
First, install Raspbian using NOOBS following these simple steps:

* Download the NOOBS network install image from the Raspberry Pi website
* You will get a very small (~25Mb) zip file. Put the content of that onto an SD card that you will just have formatted in FAT32 format
* If you have an HDMI display, you might need to create a `config.txt` file in the root of the SD card. I have a 7" capacitive display, which needs the lines described in [`boot/config.txt`](boot/config.txt).
* NOOBS will walk you through the installation of the Raspbian distribution.
* After installation, power off the Pi, connect it to another machine and edit config.txt again to make Raspbian compatible with your display.

After installing Raspbian using NOOBS, we have to clean up the filesystem a bit. We will run the Pi headless (without display), so there is no need for the X graphical interface.

```bash
sudo apt-get -y remove --auto-remove --purge cups*
sudo apt-get -y remove auto-remove --purge gnome*
sudo apt-get -y remove auto-remove --purge x11-common*
sudo apt-get -y autoremove
```

We do not need Java or Wolfram or games or a synthetiser either:

```bash
sudo apt-get -y remove --auto-remove --purge wolfram-engine penguinpuzzle java-common minecraft-pi raspberrypi-artwork sonic-pi 
```
To remove all of them at once, use this README file:

```bash
grep apt README.md | source /dev/stdin
```

We will need some packages to build Python libraries and play MP3 streams:
```bash
sudo apt-get install mpg321 python2.7-dev
```

We install the Python libraries we need:
```bash
sudo pip install llist
```

All that's left is to replace `admin` to your username in `firmware.py` at line `radiolist="/home/admin/pi-radio-firmware/firmware/radiolist"`. Now we are ready to test the firmware:
```bash
pi-radio-firmware/firmware/firnware.py
```

You should see something like:
```


=====WAIT STATE====

```

This means the firmware is running. Press `Ctrl+C` to interrupt.