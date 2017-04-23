# Giving a new life to your old vintage radio using a Raspberry Pi

## Introduction
Old AM/FM radios have a charm of their own. Their robust materials, polished surfaces and mellow sound rendition provide a listening experience unlike any other. And of course, once you take a peek inside, the palm-sized adjustable capacitors and transistor-based amplifiers will warm the heart of any electronics enthusiast. However, not all of them can stand the test of time. It's now been almost 60 years since portable AM/FM radio had its heyday, and although some models were definitely built to last (like the Beolit series from B&O), some others have aged badly.
Here I'll show you a few very easy steps to turn your dusty old radio set into a WiFi radio, using only a Raspberry Pi and a few programming skills. The whole operation should cost you less than 100$, which is still less than many high-end internet radios.

## Playing (radio) doctor

The first step is to assess the state your radio is in. This is important, because it will determine how we are going to interface the Raspberry Pi to the radio's circuitry. Without going in too much detail, a radio receiver is divided into several parts, or "stages" that feed into each other like a pipeline. By doing a variety of tests we can diagnose if something's wrong, and if yes, where the problem is. The first stage is the receiving end, which consists of an antenna and one or several RF amplifiers. This stage receives the radio signal and boosts it. That is then fed into a detector, which separates the carrier and modulating waves. One or several amplifiers then boost the signal once again to make it audible through a high-powered speaker, usually a few watts. (see a very good guide [here](http://www2.eng.cam.ac.uk/~dmh/ptialcd/trf/trf.htm).)

![Five_tube_TRF_receiver_circuit_1924.png](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Five_tube_TRF_receiver_circuit_1924.png/440px-Five_tube_TRF_receiver_circuit_1924.png)

Let's see what's broken: first, try turning your radio on.

* If you hear no sound at all even at full volume, no matter how you turn the tuning button, there is probably an issue with the power block. This is usually a bulky circuit with one or several transformers. Good news is, these are fairly replaceable and/or easy to fix as the reason for failure is often a [blown capacitor]([http://www.instructables.com/id/Repair-your-electronics-by-replacing-blown-capacit/). Check out [this guide](http://www.giangrandi.ch/electronics/smpsfix/smpsfix.shtml) for fixing SMPS-type power supplies and [this one](https://groupdiy.com/index.php?topic=19810.0) for fixing older linear transformers.
* If you can determine that your radio is powered on (via a LED or the characteristic "twung" sound when power is turned on) but nothing else is working, the amplification stage of your radio might be broken. You might hear a very faint hiss, or low levels of volume. This is annoying, because amplifiers are more tricky ro repair (they usually require transistors, which are not produced in the same way as they were back then). The solution here is to bypass the old electronics entirely and plug in your own amplifier, for example one that you salvaged from PC loudspeakers. 
* If you hear some sound, even if it's crackling, and if turning the volume button is having the expected effect, great. The amplification stage of your radio is working. This means that we'll be able to feed in our modern sound into a vintage amplifier.
* If your radio has a headphone jack or an auxiliary output, try and test that. Usually, if the secondary amplification is working, chances are that will be working as well.
* The last step is to test whether the device is able to actually receive radio signals. In short, you will be extremely lucky if your set is still able to receive the right frequency for a given position of the tuning knob. The next section goes into a bit more detail as to why that is, but it gets a bit technical so feel free to skip it. The bottom line is that this is the hardest part of the circuitry to repair, and it would require a lot of dexterity and knowledge that goes beyond what we are trying to achieve here.

## A bit of history
Nowadays radio receivers mostly deal with digital signals (via **DAB** - **D**igital **A**udio **B**roadcast), whether it's the media player in your car or the wifi chip in your laptop. However in the 60's, radio signals were mostly analog. This meant that there were two ways to transmit information: amplitude and frequency modulation. Basically, a modulating wave (the sound you want to transmit) is embedded in a carrier wave (the frequency of the station you are tuned into). The simplest way to transmit the modulating signal is to boost the carrier wave when the volume of your signal is strong, and to attenuate it when it is weak. In this way the "height", or **amplitude** of the carrier is changed, this procedure is called amplitude modulation or **AM**. In the case of frequency modulation or **FM**, the carrier is compressed (frequency increase) when the signal is strong and dilated (frequency decrease) when it is weak. Here, the frequency of the transmitted signal fluctuates slightly around the carrier frequency, the radio therefore had to listen to a narrow "band" of wavelengths instead of a single frequency. This explains why FM receivers generally have a more complex design than AM receivers, which were historically the first to be developed. Note that in both cases, the frequency of the carrier has to be much higher than that of our signal.

![http://lossenderosstudio.com/img/am-fm.gif](http://lossenderosstudio.com/img/am-fm.gif)

Both modes of transmission are fundamentally different, and require separate circuits to work. The FM receiver is a bit more 

> If you can't get any stations, it might just be a reception problem. Try moving closer to a window. Extending and moving the telescopic antenna around makes a difference only for FM/UKW. For AM bands like SW, MW and LW, try changing the orientation of your radio set to improve reception.

Quite often, for tri-band radio sets, you will find that FM reception is still quite decent, whereas the AM bands have deteriorated notably, leaving you with few or no stations detectable on your receiver.

![http://jvgavila.com/ftone_13.jpg](http://jvgavila.com/ftone_13.jpg)

On older models, oscillating circuits were calibrated to the AM/FM ranges by adjusting several capacitors, which might have gotten slightly shifted with age (they look like the metal boxes with a screw on top in the image above). This means the radio will "listen" to a wrong part of the frequency spectrum, where no stations are emitting. Recalibrating such a circuit is possible, but requires a lot of skill and access to the original engineer's documentation for your model.

## Getting hold of the schematics

This is an important step. Although manufacturers usually followed pretty similar rules in assembling their designs, the insides of two models might differ significantly.

> 50 years ago, people were a bit more comfortable with tinkering, so some models were actually shipped with the schematics inside the radio itself. Remove the bottom or back cover and if you're lucky, you'll find the precious slip of paper inside a small envelope glued to the chassis.

Fortunately, there are a lots of enthusiasts out there, and the schematics for many models were painstakingly scanned. Good places to check out are [Radio Museum](http://www.radiomuseum.org/) and [Valve Radio](http://www.valve-radio.co.uk), other than that, GIYF. Consider donating to these websites, as they are all maintained by amateurs.

In our case, the set was a Roberts R900, for which Valve Radio offers downloadable schematics:

![2.jpg](https://bitbucket.org/repo/8LMRgR/images/1855611607-2.jpg)

### Making sense of it all

This will get easier with habit, but the schematics will usually help you. The idea is to identify the different stages, which will have their components grouped together in an orderly fashion. The schematic above is annotated to make reading easier:

* In red, the power block. It's easy to notice due to the oversized transformer and the mention of 240V AC.
* in orange, the oscillator and FM front-end
* in blue, the AM/FM amplifier and detector
* in light green, the DIN inlet. This type of connector has almost completely disappeared nowadays, but was fairly common in the 70's and 80's. On some models (this one included) it can be used to feed in an auxiliary source of audio (AUX), providing non-invasive access to the loudspeaker. You can see the input line feeding into the amplifier stage just before C37.
* in purple, the amplifier stage. This is what will boost the sound coming in from either the AM/FM stage or the DIN plug to acceptable levels. The loudspeaker pictogram and the 3 variable resistors controlling volume and bass/treble filters (VR1, VR2 and VR3) are clearly visible.

These are actually quite easy to figure out on this model, because it is modern enough to feature integrated circuits (IC). These have standardised part numbers which lead you to their datasheets, most of which are found online.

## Choosing the method



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