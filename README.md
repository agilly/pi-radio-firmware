# Giving a new life to your old vintage radio using a Raspberry Pi

## Introduction
Old AM/FM radios have a charm of their own. Their robust materials, polished surfaces and mellow sound rendition provide a listening experience unlike any other. And of course, once you take a peek inside, the palm-sized adjustable capacitors and transistor-based amplifiers will warm the heart of any electronics enthusiast. However, not all of them can stand the test of time. It's now been almost 60 years since portable AM/FM radio had its heyday, and although some models were definitely built to last (like the Beolit series from B&O), some others have aged badly.
Here I'll show you a few very easy steps to turn your dusty old radio set into a WiFi radio, using only a Raspberry Pi and a few programming skills. The whole operation should cost you less than 100$, which is still less than many high-end internet radios.

## Playing (radio) doctor

The first step is to assess the state your radio is in. This is important, because it will determine how we are going to interface the Raspberry Pi to the radio's circuitry. Try turning your radio on.
* If you hear no sound at all even at full volume, no matter how you turn the tuning button, there is probably an issue with the power block. This is usually a bulky circuit with one or several transformers. Good news is, these are fairly replaceable and/or easy to fix as the reason for failure is often a [http://www.instructables.com/id/Repair-your-electronics-by-replacing-blown-capacit/](blown capacitor). Check out this guide

## A bit of history
First, a bit of nomenclature. Nowadays radio receivers mostly deal with digital signals (via **DAB** - **D**igital **A**udio **B**roadcast), whether it's the media player in your car or the wifi chip in your laptop. However in the 60's, radio signals were mostly analog. This meant that there were two ways to transmit information: amplitude and frequency modulation. Basically, a modulating wave (the sound you want to transmit) is embedded in a carrier wave (the frequency of the station you are tuned into). The simplest way to transmit the modulating signal is to boost the carrier wave when the modulating signal is strong, and to attenuate it when it is weak. In this way the "height", or **amplitude** of the carrier is changed, this procedure is called amplitude modulation or **AM**. In the case of frequency modulation or **FM**, the carrier is compressed (frequency increase) when the signal is strong and dilated (frequency decrease) when it is weak. Here, the frequency of the transmitted signal fluctuates slightly around the carrier frequency, the radio therefore had to listen to a narrow "band" of wavelengths instead of a single frequency. This explains why FM receivers generally have a more complex design than AM receivers, which were historically the first to be developed. Note that in both cases, the frequency of the carrier has to be much higher than that of our signal.

<div style="text-align:center;align:center;">
<img src="http://lossenderosstudio.com/img/am-fm.gif" align="center" width=70%>
</div>

> Remember, the antenna makes a difference only for FM/UKW. For AM bands like SW, MW and LW, try changing the orientation of your radio set to improve reception.

Quite often, for tri-band radio sets, you will find that FM reception is still quite decent, whereas the AM bands have deteriorated notably, leaving you with few or no stations detectable on your receiver.

## Setting up the Raspberry Pi

Our preferred distribution would have been Arch, but since it had sone difficulty dealing with the Wifi adapter driver, we fall back to Raspbian.

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

Edit the name of the Pi by modifying `/etc/hosts` and `/etc/hostname`, and change the password using `sudo passwd pi`. 

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

