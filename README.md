# Scorpy

Using a raspberry pi, python and pygame, I use this code to generate a score overlay (green chroma-key) for sporting events (football). It displays a timer, titles and scores and user images.

Make sure the raspberry-pi has the screen resolution set to 1920x1080

NOTE: The Raspberry Pi doesn't actually do the keying, it just generates a score/timer overlay for your vision mixer's keyer.

(demo images.jpg   ... With 29 miutes, 36 seconds, Magpies are in front 13 to 7)

Keyboard operation:

curser-keys: Move/adjust.

tab = enter the team-names and set timer/clock (tab again to exit)

spacebar = On-air / Off-air toggle.

t = Titles.

h = Halftime Score.

f = Fulltime Score.

r = Replay logo.

c = Clock (show/hide).

v = Variation.

b = Bars.

1~9 User images (e.g:  1.jpg @ 1920x1080).

The Resources folder contains fonts and images that Scorpy needs (put in the same directory as scorpy.py)

NOTE: I've made it difficult to exit the app because the last thing you want is to have a chroma-key going live to air when a desktop appears! For this reason, to exit the app, choose help screen [?], then [v] then [escape]
