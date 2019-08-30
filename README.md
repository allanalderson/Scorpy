# Scorpy

Using a raspberry pi, python and pygame, I use this code to generate a score overlay (green chroma-key) for sporting events (football). It displays a timer, titles and scores and user images.

Make sure the raspberry-pi has the screen resolution set to 1920x1080

NOTE: The Raspberry Pi doesn't actually do the keying, it just generates a score/timer overlay for your vision mixer's keyer.

(see demo images.jpg   ... With 29 miutes, 36 seconds, Magpies are in front 13 to 7)

___________________________________
Keyboard operation:

curser (up, down, left, right): Move/adjust scores.

tab = Set the team-names and timer (tab again to exit)

spacebar = On-air / Off-air toggle.

t = Titles.

h = Halftime Score.

f = Fulltime Score.

r = Replay logo.

c = Clock (show/hide).

'+' = Clock run.

'-' = Clock stop.

<  > = Adjust countdown seconds

v = Variation on the current theme.

b = Bars (but no tone)

w = watermark.png (show/hide)

? = help screen.

1~9 User images (e.g:  1.jpg @ 1920x1080).

If the Raspberry Pi is configured to mount an external
USB drive to '../../mnt/volume/', 9 user images will be
read from a FAT32 format USB drive during power-up.
User Image filenames should be this format:  image1.jpg
and be 1920 x 1080 pixels.

Scorpy will also attempt to load 1 watermark image from the same drive.
It's filename should be this format:  watermark.png
and should contain an alpha (transparency) channel.
The watermark filesize should be about 250 x 100 pixels.


The folder 'scorpy_resources' contains fonts and images that Scorpy needs. Regardless of version, this zipped file will always contain all scorpy resources.


