'''
4.0 RELEASE.
4.1 key code tidy and timer set adjustment.Bugfix userimages 5-9
4.2 Minor tweeks to greens and better clock routine
4.3 User Image Help
4.4 New fulltime and halftime graphics.
	Timer vanish after 5 seconds below 0:00
	Timer continues to run during input screen.
4.5 Score selection indicator.
4.6 Minor tweeks to score selection screen
4.7 Now responding to a numeric keypad
4.8 Count-up Ready and minor color changes
4.9 Added LT Clock , some refactoring
5.0 Changed 'Resources' folder to 'scorpy_resources'
5.1 Added Watermark
5.2 Bug Fix no score change during Score screen's first run. Code easier to read
5.3 Add score swap Variation (v) during score screen.
5.4 Reset scores to zero if titles screen displayed.
5.5 Quick access to screens.
5.6 Tidy LT bar. Repair LT double trigger
5.7 Clock callable on-air. Corner position tweaks.
5.8 Refactoring, Quick access score bug fixed.
5.9 Corner and graphics tweaks, removed diagnostic printouts. Drop-shaddow on big scores
6.0 Clock display allowed after Replay screen. Team Swap variation allowed on Titles Screen.
6.1 Added timer adjust with    <   >   keys.
6.11 Changed timer adjust for seconds (not minutes)  when off-air.
6.2 Added Software Version on Bars screen.
6.3 Smart countdown reset with user_minutes.
6.4 Smart erase Titles & Teams
6.5 Bugfix: timer adjust seconds
6.6 Blue Titles, Instant Replay.
6.7 Sticky userImages 1~9. 0 = kill all userImages
6.8 No overlap on user images.



'''


import pygame
from pygame.locals import *
import os
import sys


scorpy_version = "Scorpy 6.8"
sys.path.append('../../mnt/volume/')
pygame.init()
windowSizeX = 1920
windowSizeY = 1080
team1Score = 0
team2Score = 0
# sys.path.append('/boot/')
liveshot = False
screen = pygame.display.set_mode([windowSizeX, windowSizeY])
screen = pygame.display.set_mode([windowSizeX, windowSizeY], pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
dropShaddowDistance = 4
bigScorePositionRight = 1443
bigScorePositionLeft = 480
countdown_seconds = 0
countdown_minutes = 40
user_minutes = 0
timer_running = False
variation_timer = 5
variation_replay = 1
variation_watermark = 3
countdown_ticks = (countdown_minutes*60)+(countdown_seconds)
countdownMinutesText = str(countdown_minutes)
previousKey = "0"
showWatermark = False
showReplay = False
counting_down = True
white = (250,250,250)
yellow = (220,200,160)
black = (0,0,0)
blue = (30, 30, 140)
red = (250, 80, 80)
greenScreen = (0, 150, 0)
green2 = (0, 175, 0)
green3 = (10, 195, 10)
green4 = (15, 230, 15) # bright green for timer preview
green_filter = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
green_filter.fill((0, 150, 0, 190))
grey = (100, 100, 100)
clock = pygame.time.Clock()
lowerThirdBoxThickness = 190 #110
LT_rasing = False
LT_lowering = False
transition_trigger = False
LT_counter = 0
LT_box_position_UP = 1045
LT_box_position_DOWN = 1105
LT_box_position = LT_box_position_DOWN #  1105 is offscreen, (1045 is onscreen)
shiftDown = False
showTimer = False
running = True
activeTextBox = 0 # 1&2=teamNames;  3&4=scores;  11&12 Titles
validChars = " `1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = ' ~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
live_screen_ID = "Bars"
on_air = True
showImage1 = False
showImage2 = False
showImage3 = False
showImage4 = False
showImage5 = False
showImage6 = False
showImage7 = False
showImage8 = False
showImage9 = False


fontGeneral = pygame.font.Font('scorpy_resources/Fonts/Roboto-Medium.ttf', 60)
fontDigital_big = pygame.font.Font('scorpy_resources/Fonts/digital-7 (mono).ttf', 260)
fontDigital_timer = pygame.font.Font('scorpy_resources/Fonts/digital-7 (mono).ttf', 62)
tabexit = " Use curser keys to move,  TAB key to exit. "
tabexitR = fontGeneral.render(tabexit, True, greenScreen, green2)
tabexit_rect = tabexitR.get_rect()
tabexit_rect.center = tabexitR.get_rect().center # Get it's dimentions.


versionR = fontGeneral.render(scorpy_version, True, grey, black)
version_rect = versionR.get_rect()
version_rect.center = versionR.get_rect().center # Use the center from now on.
# Use it...
# version_rect.center = [windowSizeX / 2, 950]  # Put it somewhere
# screen.blit(versionR, version_rect)





titlesRequestText = " Titles                       "
teamsRequestText  =  " Teams                     "
requestFont = pygame.font.Font('scorpy_resources/Fonts/xxii_geom_slab/XXIIGeomSlabDEMO-Bold.otf', 180)
teamNamesRequestText = requestFont.render(teamsRequestText, True, greenScreen, green2)
teamNamesRequestText_rect = teamNamesRequestText.get_rect()
titlesNamesRequestText = requestFont.render(titlesRequestText, True, greenScreen, green2)
titleNamesRequestText_rect = titlesNamesRequestText.get_rect()
bars = screen
help1 = screen
full_screen_rect = [0, 0]
full_screen_rect = bars.get_rect()
full_screen_rect.center = screen.get_rect().center  # Set image centers
bars = pygame.image.load('scorpy_resources/Graphics/bars1080.png').convert()
halfTimeGraphic = pygame.image.load('scorpy_resources/Graphics/halfTimeImage.png').convert_alpha()
fullTimeGraphic = pygame.image.load('scorpy_resources/Graphics/fullTimeImage.png').convert_alpha()
help1 = pygame.image.load('scorpy_resources/Graphics/help1.png').convert()
help2 = pygame.image.load('scorpy_resources/Graphics/help2.png').convert()
liveshot_graphic = pygame.image.load('scorpy_resources/Graphics/liveshot.png').convert()
titleVS_graphic = pygame.image.load('scorpy_resources/Graphics/VS_graphic.png').convert_alpha()
replay = pygame.image.load('scorpy_resources/Graphics/replay.png').convert_alpha()
corner1 = [(windowSizeX // 2) - 800, (windowSizeY // 2) + 440] # bottom, left
corner2 = [(windowSizeX // 2) - 800, (windowSizeY // 2) - 470] # top, left
corner3 = [(windowSizeX // 2) + 800, (windowSizeY // 2) - 470] # top, right
corner4 = [(windowSizeX // 2) + 800, (windowSizeY // 2) + 440] # bottom, right
replay_rect = replay.get_rect() # Get it's dimentions.
replay_rect.center = replay.get_rect().center  # Set it's center.
# replay_rect.center = corner3 # Put it somewhere
# screen.blit(replay, replay_rect) # Draw
class TextBox(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.text = ""
		self.font = pygame.font.Font('scorpy_resources/Fonts/Roboto-Medium.ttf', 50) #55
		self.image = self.font.render("", True, [70, 255, 70])
		self.rect = self.image.get_rect()
	def add_chr(self, char):
		global shiftDown
		if char in validChars and not shiftDown:
			self.text += char
		elif char in validChars and shiftDown:
			self.text += shiftChars[validChars.index(char)]
		self.update()
	def update(self):
		old_rect_pos = self.rect.center # memory
		# self.image = self.fontGeneral.render(self.text, True, green3)
		self.rect = self.image.get_rect()
		self.rect.center = old_rect_pos
	def white(self):
		self.image = self.font.render(self.text, True, white)
	def green2(self):
		self.image = self.font.render(self.text, True, green2)
	def green3(self):
		self.image = self.font.render(self.text, True, green3)
	def green4(self):
		self.image = self.font.render(self.text, True, green4)
	def green0(self):
		self.image = self.font.render(self.text, True, greenScreen)
	def black(self):
		self.image = self.font.render(self.text, True, black)
	def fontBigScore(self):
		self.font = pygame.font.Font('scorpy_resources/Fonts/Roboto-Light.ttf', 270)
		self.image = self.font.render(self.text, True, white)
		self.update()
	def fontBigPreviewScore(self):
		self.font = pygame.font.Font('scorpy_resources/Fonts/Roboto-Medium.ttf', 500)
		self.image = self.font.render(self.text, True, green3)
		self.update()
	def fontLowerThird(self):
		self.font = pygame.font.Font('scorpy_resources/Fonts/Roboto-Medium.ttf', 40)
		self.update()
	def fontTeamNameUnderScore(self):
		self.font = pygame.font.Font('scorpy_resources/Fonts/Roboto-Medium.ttf', 60)  #55
		self.update()
	def fontTeamVS(self):
		self.font = pygame.font.Font('scorpy_resources/Fonts/xxii_geom_slab/XXIIGeomSlabDEMO-Bold.otf', 100)  #55
		self.update()
	def fontMajorTitle(self):
		self.font = pygame.font.Font('scorpy_resources/Fonts/Roboto-Medium.ttf', 90)  #55
		self.update()
	def fontMinorTitle(self):
		self.font = pygame.font.Font('scorpy_resources/Fonts/Roboto-Medium.ttf', 70)  #55
		self.update()
	def blue(self):
		self.image = self.font.render(self.text, True, blue)
		self.update()

majorTitleName = TextBox() # active text box 11
minorTitleName = TextBox() # active text box 12
majorTitleName.text = "Major Title"
minorTitleName.text = "Minor Title"
majorTitleName.fontMajorTitle()
minorTitleName.fontMinorTitle()
majorTitleName.green3()
minorTitleName.green3()
majorTitleName.update()
minorTitleName.update()
team1name = TextBox()
team2name = TextBox()
team1name.text = "Team1"
team2name.text = "Team2"
team1name.green3()
team1name.update()
team2name.green3()
team2name.update()
team1ScoreBox = TextBox()
team1ScoreBox.text = str(team1Score)
team2ScoreBox = TextBox()
team2ScoreBox.text = str(team2Score)
lowerThirdText = TextBox()
lowerThirdText.text = ""


watermark = pygame.image.load('scorpy_resources/Graphics/watermark.png').convert_alpha()
try:
	watermark = pygame.image.load('../../mnt/volume/watermark.jpg').convert_alpha()
except:
	pass
try:
	watermark = pygame.image.load('../../mnt/volume/watermark.png').convert_alpha()
except:
	pass
watermark_rect = watermark.get_rect()  # Get it's dimentions.
watermark_rect.center = watermark.get_rect().center  # Set it's center.

try:
	userImage1 = pygame.image.load('../../mnt/volume/image1.png').convert_alpha()
except:
	userImage1 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
try:
	userImage2 = pygame.image.load('../../mnt/volume/image2.png').convert_alpha()
except:
	userImage2 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
try:
	userImage3 = pygame.image.load('../../mnt/volume/image3.png').convert_alpha()
except:
	userImage3 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
try:
	userImage4 = pygame.image.load('../../mnt/volume/image4.png').convert_alpha()
except:
	userImage4 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
try:
	userImage5 = pygame.image.load('../../mnt/volume/image5.png').convert_alpha()
except:
	userImage5 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
try:
	userImage6 = pygame.image.load('../../mnt/volume/image6.png').convert_alpha()
except:
	userImage6 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
try:
	userImage7 = pygame.image.load('../../mnt/volume/image7.png').convert_alpha()
except:
	userImage7 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
try:
	userImage8 = pygame.image.load('../../mnt/volume/image8.png').convert_alpha()
except:
	userImage8 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
try:
	userImage9 = pygame.image.load('../../mnt/volume/image9.png').convert_alpha()
except:
	userImage9 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()




def draw_bars_screen():
	screen.blit(bars, full_screen_rect)
	version_rect.center = [windowSizeX / 2, 140] # Put it somewhere
	screen.blit(versionR, version_rect)
def draw_greenscreen():
	screen.fill(greenScreen)
	if liveshot == True:
		screen.blit(liveshot_graphic, full_screen_rect)
def draw_input_screen():
	global timer_running
	global countdownTextR
	global countdown_ticks
	global countdown_seconds
	global countdown_minutes
	global showTimer
	showTimer = False
	team1name.green0()
	team2name.green0()
	majorTitleName.green0()
	minorTitleName.green0()
	if activeTextBox == 1:
		team1name.green4()
	if activeTextBox == 2:
		team2name.green4()
	if activeTextBox == 11:
		majorTitleName.green4()
	if activeTextBox == 12:
		minorTitleName.green4()
	majorTitleName.fontMinorTitle()
	minorTitleName.fontMinorTitle()
	team1name.fontMinorTitle()
	team2name.fontMinorTitle()
	screen.blit(titlesNamesRequestText, [100, 200])
	screen.blit(teamNamesRequestText, [100, 450])
	screen.blit(majorTitleName.image, [800, 200])
	screen.blit(minorTitleName.image, [800, 300])
	screen.blit(team1name.image, [800, 450])
	screen.blit(team2name.image, [800, 550])
	countdown_ticks = (countdown_minutes * 60) + (countdown_seconds)
	countdown_minutes = countdown_ticks//60
	countdown_seconds = countdown_ticks % 60
	if countdown_seconds < 10:
		countdownSecondsText = "0" + str(countdown_seconds)
	else:
		countdownSecondsText =  str(countdown_seconds)
	if countdown_minutes < 10:
		countdownMinutesText = "" + str(countdown_minutes)
	else:
		countdownMinutesText = str(countdown_minutes)
	countdownMinutesText = "< " + countdownMinutesText
	countdownSecondsText = countdownSecondsText + " >  Timer"
	if activeTextBox == 5:
		countdownText = countdownMinutesText + ":" + countdownSecondsText
		countdownTextR = fontGeneral.render(countdownText, False, green4, green2)  # Render it.
	else:
		countdownText = countdownMinutesText + ":" + countdownSecondsText
		countdownTextR = fontGeneral.render(countdownText, False, green2)  # Render it.
	countdown_rect = [800, 700]  # Put the center of the rect somewhere
	screen.blit(countdownTextR, countdown_rect)  # Draw the render, here.
	tabexit_rect.center = [windowSizeX / 2, 950] # Put it somewhere
	screen.blit(tabexitR, tabexit_rect)
def draw_title_screen():
	team1name.blue()
	team2name.blue()
	majorTitleName.blue()
	minorTitleName.blue()
	majorTitleName.rect.center = [(windowSizeX // 2), 180]
	minorTitleName.rect.center = [(windowSizeX // 2), 315]
	team1name.rect.center = [(windowSizeX // 2), 580]
	team2name.rect.center = [(windowSizeX // 2),855]
	majorTitleName.fontMajorTitle()
	minorTitleName.fontMinorTitle()
	team1name.fontTeamVS()
	team2name.fontTeamVS()
	screen.blit(titleVS_graphic, full_screen_rect)
	screen.blit(majorTitleName.image, majorTitleName.rect)
	screen.blit(minorTitleName.image, minorTitleName.rect)
	screen.blit(team1name.image, team1name.rect)
	screen.blit(team2name.image, team2name.rect)
	draw_OFFAIR_filter()
def draw_halftime_screen():
	global countdown_ticks
	global timer_running
	# global user_minutes
	if countdown_ticks < 1:
		countdown_ticks = user_minutes * 60
		timer_running = False
	screen.blit(halfTimeGraphic, full_screen_rect)
	draw_big_score_screen()
	draw_OFFAIR_filter()
def draw_fulltime_screen():
	global countdown_ticks
	global timer_running

	if countdown_ticks < 1:
		countdown_ticks = user_minutes * 60
		timer_running = False
	screen.blit(fullTimeGraphic, full_screen_rect)
	draw_big_score_screen()
	draw_OFFAIR_filter()
def draw_score_screen():
	global LT_rasing
	global LT_lowering
	global transition_trigger
	global LT_counter
	global LT_box_position
	global activeTextBox
	global LT_box_position_UP



	if LT_box_position < 991:
		lowerThirdBoxThickness = 45 # small box 45
	if LT_box_position > 990:
		lowerThirdBoxThickness = 100 # large box 100

	draw_timer_preview()
	team1name.green3()
	team2name.green3()
	team1ScoreBox.green3()
	team2ScoreBox.green3()
	pygame.draw.rect(screen, black, (0, LT_box_position - 22, windowSizeX, lowerThirdBoxThickness))  #-22 the size of LT box top
	lowerThirdText.text = team1name.text + "  " + team1ScoreBox.text + "                                                                     " + team2name.text + "  " + team2ScoreBox.text
	lowerThirdText.rect.center = [(windowSizeX // 2), LT_box_position]
	lowerThirdText.white()
	lowerThirdText.fontLowerThird()
	lowerThirdText.update()

	if transition_trigger == True:
		if on_air == True:
			LT_rasing = True
			LT_lowering = False
		else: #  transition_trigger false:
			LT_rasing = False
			LT_lowering = True
	if LT_rasing == True and LT_box_position > LT_box_position_UP:
		LT_counter = LT_counter - 1 # raise
	else:
		LT_rasing = False
	if LT_lowering == True and LT_box_position < LT_box_position_DOWN: # 1105 is below screen
		LT_counter = LT_counter + 1 # lower
	else:
		LT_lowering = False
	LT_box_position = LT_box_position_DOWN + (LT_counter * (LT_box_position_DOWN - LT_box_position_UP) // 10)
	screen.blit(lowerThirdText.image, lowerThirdText.rect)
	if on_air == False and LT_lowering == False and LT_rasing == False: # lower thirds off-air marker...
		if LT_box_position_UP - 22 < 991:
			lowerThirdBoxThickness = 45  # 45 small box
		if LT_box_position_UP - 22 > 990:
			lowerThirdBoxThickness = 100  # 100 large box
		pygame.draw.rect(screen, green3, (0, LT_box_position_UP - 22, windowSizeX, lowerThirdBoxThickness))  #-22
	if LT_lowering == False or LT_rasing == False:
		transition_trigger = False # reset the trigger
	draw_score_preview_screen()
	draw_timer_panel()
def draw_score_preview_screen():
	team1name.fontTeamNameUnderScore()
	team2name.fontTeamNameUnderScore()
	team1name.green3()
	team2name.green3()
	team1ScoreBox.fontBigPreviewScore()
	team2ScoreBox.fontBigPreviewScore()
	if activeTextBox == 3:
		team1ScoreBox.green4()
		team1name.green4()
		team2ScoreBox.green2()
		team2name.green2()
	if activeTextBox == 0:
		team1ScoreBox.green4()
		team2ScoreBox.green4()
		team1name.green4()
		team2name.green4()
		team1ScoreBox.green2()
		team1name.green2()
	if activeTextBox == 4:
		team2ScoreBox.green4()
		team2name.green4()
	if activeTextBox == 0:
		team1ScoreBox.green4()
		team2ScoreBox.green4()
		team1name.green4()
		team2name.green4()
	team1name.rect.center = [bigScorePositionLeft, (windowSizeY // 2) + 300]
	team2name.rect.center = [bigScorePositionRight, ((windowSizeY // 2) + 300)]
	team1ScoreBox.rect.center = [bigScorePositionLeft, (windowSizeY // 2) + 20]
	team2ScoreBox.rect.center = [bigScorePositionRight, (windowSizeY // 2) + 20]
	screen.blit(team1name.image, team1name.rect)
	screen.blit(team2name.image, team2name.rect)
	screen.blit(team1ScoreBox.image, team1ScoreBox.rect)
	screen.blit(team2ScoreBox.image, team2ScoreBox.rect)
	draw_timer_preview()
def draw_timer_preview():
	triangleY = 175
	if counting_down == True:
		pygame.draw.polygon(screen, green3, [[(windowSizeX // 2-40), (triangleY+100)], [(windowSizeX // 2+40), (triangleY+100)],[(windowSizeX // 2), (triangleY+140)]])
	else:
		pygame.draw.polygon(screen, green3, [[(windowSizeX // 2-40), (triangleY-100)], [(windowSizeX // 2+40), (triangleY-100)],[(windowSizeX // 2), (triangleY-140)]])
	if timer_running == False:
		countdownTextR = fontDigital_big.render(countdownText, False, green2, green3)  # Render it.
	elif timer_running == True and activeTextBox == 0:
		countdownTextR = fontDigital_big.render(countdownText, False, green4)  # Render it.
	else:
		countdownTextR = fontDigital_big.render(countdownText, False, green3)  # Render it.
	countdown_rect = countdownTextR.get_rect()  # Get the render's rect
	countdown_rect.center = [windowSizeX // 2, 170]  # Put the center of the rect somewhere
	screen.blit(countdownTextR, countdown_rect)  # Draw the render, here.
def draw_big_score_screen():
	teamNameYoffset = 290 # 260
	teamScoreYoffset = 120 # 60
	team1name.fontTeamNameUnderScore()
	team2name.fontTeamNameUnderScore()
	team1name.black()
	team2name.black()
	team1name.rect.center = [bigScorePositionLeft + dropShaddowDistance, (windowSizeY // 2) + teamNameYoffset + dropShaddowDistance]
	team2name.rect.center = [bigScorePositionRight + dropShaddowDistance, ((windowSizeY // 2) + teamNameYoffset + dropShaddowDistance)]
	screen.blit(team1name.image, team1name.rect)
	screen.blit(team2name.image, team2name.rect)
	team1name.white()
	team2name.white()
	team1name.rect.center = [bigScorePositionLeft, (windowSizeY // 2) + teamNameYoffset]
	team2name.rect.center = [bigScorePositionRight, ((windowSizeY // 2) + teamNameYoffset)]
	screen.blit(team1name.image, team1name.rect)
	screen.blit(team2name.image, team2name.rect)

	#----- Drop Shaddow START
	team1ScoreBox.fontBigScore()
	team2ScoreBox.fontBigScore()
	team1ScoreBox.black()
	team2ScoreBox.black()
	# lower-right
	team1ScoreBox.rect.center = [bigScorePositionLeft + dropShaddowDistance, (windowSizeY // 2)+teamScoreYoffset + dropShaddowDistance]
	team2ScoreBox.rect.center = [bigScorePositionRight + dropShaddowDistance, (windowSizeY // 2)+teamScoreYoffset + dropShaddowDistance]
	screen.blit(team1ScoreBox.image, team1ScoreBox.rect)
	screen.blit(team2ScoreBox.image, team2ScoreBox.rect)
	# upper-left
	team1ScoreBox.rect.center = [bigScorePositionLeft - dropShaddowDistance, (windowSizeY // 2)+teamScoreYoffset - dropShaddowDistance]
	team2ScoreBox.rect.center = [bigScorePositionRight - dropShaddowDistance, (windowSizeY // 2)+teamScoreYoffset - dropShaddowDistance]
	screen.blit(team1ScoreBox.image, team1ScoreBox.rect)
	screen.blit(team2ScoreBox.image, team2ScoreBox.rect)
	# upper-right
	team1ScoreBox.rect.center = [bigScorePositionLeft + dropShaddowDistance, (windowSizeY // 2)+teamScoreYoffset - dropShaddowDistance]
	team2ScoreBox.rect.center = [bigScorePositionRight + dropShaddowDistance, (windowSizeY // 2)+teamScoreYoffset - dropShaddowDistance]
	screen.blit(team1ScoreBox.image, team1ScoreBox.rect)
	screen.blit(team2ScoreBox.image, team2ScoreBox.rect)
	# lower-left
	team1ScoreBox.rect.center = [bigScorePositionLeft - dropShaddowDistance, (windowSizeY // 2)+teamScoreYoffset + dropShaddowDistance]
	team2ScoreBox.rect.center = [bigScorePositionRight - dropShaddowDistance, (windowSizeY // 2)+teamScoreYoffset + dropShaddowDistance]
	screen.blit(team1ScoreBox.image, team1ScoreBox.rect)
	screen.blit(team2ScoreBox.image, team2ScoreBox.rect)
	#----- Drop Shaddow END

	team1ScoreBox.white()
	team2ScoreBox.white()
	team1ScoreBox.rect.center = [bigScorePositionLeft, (windowSizeY // 2) +teamScoreYoffset]
	team2ScoreBox.rect.center = [bigScorePositionRight, (windowSizeY // 2) +teamScoreYoffset]
	screen.blit(team1ScoreBox.image, team1ScoreBox.rect)
	screen.blit(team2ScoreBox.image, team2ScoreBox.rect)
def draw_OFFAIR_filter():
	global team1Score
	global team2Score
	if on_air == False:
		screen.blit(green_filter, full_screen_rect)
	else:
		#  Reset scores to zero if titles displayed.
		if previousKey =="space" and live_screen_ID == "Titles":
			team1Score = 0
			team2Score = 0
			team1ScoreBox.text = str(team1Score)
			team1ScoreBox.update()
			team2ScoreBox.text = str(team2Score)
			team2ScoreBox.update()
def draw_userImages():
	if showImage1 == True:
		screen.blit(userImage1, full_screen_rect) # Draw it.
	if showImage2 == True:
		screen.blit(userImage2, full_screen_rect)  # Draw it.
	if showImage3 == True:
		screen.blit(userImage3, full_screen_rect) # Draw it.
	if showImage4 == True:
		screen.blit(userImage4, full_screen_rect)  # Draw it.
	if showImage5 == True:
		screen.blit(userImage5, full_screen_rect) # Draw it.
	if showImage6 == True:
		screen.blit(userImage6, full_screen_rect)  # Draw it.
	if showImage7 == True:
		screen.blit(userImage7, full_screen_rect) # Draw it.
	if showImage8 == True:
		screen.blit(userImage8, full_screen_rect)  # Draw it.
	if showImage9 == True:
		screen.blit(userImage9, full_screen_rect)  # Draw it.
def update_tick():
	global countdown_ticks
	if timer_running == True:
		if counting_down == True:
			countdown_ticks = countdown_ticks - 1
		else:
			countdown_ticks = countdown_ticks + 1
	update_clocks()
def update_clocks():
	global countdownText
	global countdown_seconds
	global countdown_minutes
	global showTimer

	if countdown_ticks < -4:
		showTimer = False
	if countdown_ticks > -1:
		countdown_minutes = countdown_ticks//60
		countdown_seconds = countdown_ticks % 60
	if countdown_seconds < 10:
		countdownSecondsText = "0" + str(countdown_seconds)
	else:
		countdownSecondsText =  str(countdown_seconds)
	if countdown_minutes < 10:
		countdownMinutesText = "" + str(countdown_minutes)
	else:
		countdownMinutesText = str(countdown_minutes)
	countdownText = countdownMinutesText + ":" + countdownSecondsText
def draw_timer_panel():

	if showTimer == True and variation_timer < 5:
		if timer_running == False:
			countdownTextR = fontDigital_timer.render(countdownText, True, red, black)  # Render it.
		else:
			countdownTextR = fontDigital_timer.render(countdownText, True, white, black) # Render it.
	if showTimer == False and variation_timer < 5:
		countdownTextR = fontDigital_timer.render(countdownText, True, green4, green3)  # Render it.

	if showTimer == True and variation_timer > 4:
		if timer_running == False:
			countdownTextR = fontDigital_timer.render(countdownText, True, red )  # Render it.
		else:
			countdownTextR = fontDigital_timer.render(countdownText, True, white) # Render it.
	if showTimer == False and variation_timer > 4:
		countdownTextR = fontDigital_timer.render(countdownText, True, black)  # Render it.


	countdown_rect = countdownTextR.get_rect()  # Get the render's rect
	if variation_timer == 1:
		countdown_rect.center = corner1  # Put the center of the rect somewhere
	if variation_timer == 2:
		countdown_rect.center = corner2  # Put the center of the rect somewhere
	if variation_timer == 3:
		countdown_rect.center = corner3  # Put the center of the rect somewhere
	if variation_timer == 4:
		countdown_rect.center = corner4  # Put the center of the rect somewhere
	if variation_timer == 5: # lower third position
		countdown_rect.center = [(windowSizeX // 2), LT_box_position + 2]
	screen.blit(countdownTextR, countdown_rect)  # Draw the render, here.
def draw_watermark_image():
	if showWatermark == True:
		if variation_watermark == 1:
			watermark_rect.center = corner1  # Put it somewhere
		if variation_watermark == 2:
			watermark_rect.center = corner2  # Put it somewhere
		if variation_watermark == 3:
			watermark_rect.center = corner3  # Put it somewhere
		if variation_watermark == 4:
			watermark_rect.center = corner4  # Put it somewhere
		screen.blit(watermark, watermark_rect)  # Draw it.
def draw_replay_image():
	if showReplay == True:
		if variation_replay == 1:
			replay_rect.center = corner1
		if variation_replay == 2:
			replay_rect.center = corner2
		if variation_replay == 3:
			replay_rect.center =corner3
		if variation_replay == 4:
			replay_rect.center = corner4
		screen.blit(replay, replay_rect)
def adjust_timer(tick_delta):
	global countdown_ticks
	global countdown_seconds
	global countdown_minutes
	countdown_ticks = countdown_ticks + tick_delta
	countdown_seconds = countdown_ticks % 60
	countdown_minutes = countdown_ticks//60
	update_clocks()
def killUserImages():
	global showImage1
	global showImage2
	global showImage3
	global showImage4
	global showImage5
	global showImage6
	global showImage7
	global showImage8
	global showImage9
	showImage1 = False
	showImage2 = False
	showImage3 = False
	showImage4 = False
	showImage5 = False
	showImage6 = False
	showImage7 = False
	showImage8 = False
	showImage9 = False




# ------------------------------------------------


pygame.time.set_timer(USEREVENT + 0, 1000)
while running:
	draw_greenscreen()
	if live_screen_ID == "Titles":
		draw_title_screen()
	if live_screen_ID == "Scores":
		draw_score_screen()
	if live_screen_ID == "Halftime":
		draw_halftime_screen()
	if live_screen_ID == "Fulltime":
		draw_fulltime_screen()
	if live_screen_ID == "Bars":
		draw_bars_screen()
		draw_OFFAIR_filter()
	if live_screen_ID == "input":
		draw_input_screen()
	if live_screen_ID == "Help1":
		screen.blit(help1, full_screen_rect)
		activeTextBox = 0

	if live_screen_ID == "Help2":
		screen.blit(help2, full_screen_rect)
		on_air = False

	for event in pygame.event.get():
		if event.type == USEREVENT + 0:
			update_tick()
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_r:
				showReplay = False
			if majorTitleName.text == "Major Titl":
				majorTitleName.text = ""
			if minorTitleName.text == "Minor Titl":
				minorTitleName.text = ""
			if team1name.text == "Team":
				team1name.text = ""
			if team2name.text == "Team":
				team2name.text = ""
			if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
				shiftDown = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if live_screen_ID == "Help2":
					pygame.quit()
					quit()
			if event.key == pygame.K_TAB:
				if live_screen_ID == "input":  # if inputscreen true then
					live_screen_ID = "Scores"  # exit.
					activeTextBox = 0
				elif live_screen_ID != "input" and on_air == False:
					killUserImages()
					activeTextBox = 11  #make active
					live_screen_ID = "input"
					draw_input_screen()
			if live_screen_ID == "input":
				if activeTextBox == 11:  # major title
					if event.key == pygame.K_DOWN or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
						activeTextBox = 12  # minor title
					if event.key == pygame.K_SPACE:
						majorTitleName.text += " "
						majorTitleName.update()
					if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
						shiftDown = True
					if event.key == pygame.K_BACKSPACE:
						majorTitleName.text = majorTitleName.text[:-1]
					majorTitleName.add_chr(pygame.key.name(event.key))
					majorTitleName.update()
				elif activeTextBox == 12:  # minor title
					if event.key == pygame.K_UP:
						activeTextBox = 11
					if event.key == pygame.K_DOWN or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
						activeTextBox = 1  #
					if event.key == pygame.K_SPACE:
						minorTitleName.text += " "
						minorTitleName.update()
					if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
						shiftDown = True
					if event.key == pygame.K_BACKSPACE:
						minorTitleName.text = minorTitleName.text[:-1]
					minorTitleName.add_chr(pygame.key.name(event.key))
					minorTitleName.update()
				elif activeTextBox == 1:  #team1 Name set
					if event.key == pygame.K_DOWN or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
						activeTextBox = 2
					if event.key == pygame.K_UP:
						activeTextBox = 12
					if event.key == pygame.K_SPACE:
						team1name.text += " "
						team1name.update()
					if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
						shiftDown = True
					if event.key == pygame.K_BACKSPACE:
						team1name.text = team1name.text[:-1]
					team1name.add_chr(pygame.key.name(event.key))
					team1name.update()
				elif activeTextBox == 2:  # move
					if event.key == pygame.K_UP:
						activeTextBox = 1
					if event.key == pygame.K_DOWN or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
						timer_running = False
						countdown_seconds = 0
						countdown_minutes = 40
						activeTextBox = 5
						counting_down = True
					if event.key == pygame.K_SPACE:
						team2name.text += " "
						team2name.update()
					if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
						shiftDown = True
					if event.key == pygame.K_BACKSPACE:
						team2name.text = team2name.text[:-1]
					team2name.add_chr(pygame.key.name(event.key))
					team2name.update()
				elif activeTextBox == 5:  #timer set
					if event.key == pygame.K_UP:
						activeTextBox = 2
					if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
						activeTextBox = 0
						live_screen_ID = "Titles"  # exit.
						on_air = False
					if event.key == pygame.K_LEFT:
						if countdown_minutes > 20:
							countdown_minutes = countdown_minutes - 5
						else:
							if countdown_minutes > 0:
								countdown_minutes = countdown_minutes - 1
								if countdown_minutes < 1:
									counting_down = False
					if event.key == pygame.K_RIGHT:
						if countdown_minutes > 24:
							countdown_minutes = countdown_minutes + 5
						else:
							countdown_minutes = countdown_minutes + 1
					user_minutes = countdown_minutes
			else:  # ------ NOT THE INPUT SCREEN
				if event.key == pygame.K_w:
					previousKey = "w"
					showWatermark = not showWatermark
				if event.key == pygame.K_1:
					if showImage1 == True:
						showImage1 = False
					else:
						killUserImages()
						showImage1 = True
				if event.key == pygame.K_2:
					if showImage2 == True:
						showImage2 = False
					else:
						killUserImages()
						showImage2 = True
				if event.key == pygame.K_3:
					if showImage3 == True:
						showImage3 = False
					else:
						killUserImages()
						showImage3 = True
				if event.key == pygame.K_4:
					if showImage4 == True:
						showImage4 = False
					else:
						killUserImages()
						showImage4 = True
				if event.key == pygame.K_5:
					if showImage5 == True:
						showImage5 = False
					else:
						killUserImages()
						showImage5 = True
				if event.key == pygame.K_6:
					if showImage6 == True:
						showImage6 = False
					else:
						killUserImages()
						showImage6 = True
				if event.key == pygame.K_7:
					if showImage7 == True:
						showImage7 = False
					else:
						killUserImages()
						showImage7 = True
				if event.key == pygame.K_8:
					if showImage8 == True:
						showImage8 = False
					else:
						killUserImages()
						showImage8 = True
				if event.key == pygame.K_9:
					if showImage9 == True:
						showImage9 = False
					else:
						killUserImages()
						showImage9 = True
				if event.key == pygame.K_0:
					killUserImages()
				if event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER:
					previousKey = "space"
					if activeTextBox > 0:
						activeTextBox = 0
					on_air = not on_air
					transition_trigger = True
					if live_screen_ID == "Bars" and activeTextBox == -1:
						live_screen_ID = "Help1"
						on_air = False
						activeTextBox = 11
				if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
					pass
					timer_running = False
				if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
					pass
					timer_running = True
				if event.key == pygame.K_c or event.key == pygame.K_KP_MULTIPLY:
					if live_screen_ID == "Scores":
						previousKey = "c"
						showTimer = not showTimer
				if LT_box_position == LT_box_position_DOWN:
					if event.key == pygame.K_t:
						live_screen_ID = "Titles"
						on_air = False
					if event.key == pygame.K_s:
						previousKey = "s"
						live_screen_ID = "Scores"
						activeTextBox = 0
						on_air = False
					if event.key == pygame.K_h:
						on_air = False
						live_screen_ID = "Halftime"
					if event.key == pygame.K_f:
						on_air = False
						live_screen_ID = "Fulltime"
					if event.key == pygame.K_r:
						previousKey = "r"
						showReplay = True
						showTimer = False
					if event.key == pygame.K_b:
						killUserImages()
						on_air = False
						if live_screen_ID == "Bars":
							live_screen_ID = "Scores"
							on_air = False
						elif on_air == False:
							live_screen_ID = "Bars"
					if event.key == pygame.K_QUESTION or event.key == pygame.K_SLASH:
						on_air = False
						previousKey = "?"
						if live_screen_ID != "Help1":
							live_screen_ID = "Help1"
						else:
							live_screen_ID = "Scores"
				if event.key == pygame.K_v:
					if live_screen_ID == "Help2":
						live_screen_ID = "Help1"
					elif live_screen_ID == "Help1":
						live_screen_ID = "Help2"
					if previousKey == "r":
						variation_replay = variation_replay + 1
						if variation_replay > 4:
							variation_replay = 1
					if previousKey == "w":
						variation_watermark = variation_watermark + 1
						if variation_watermark > 4:
							variation_watermark = 1
					if previousKey == "c" and live_screen_ID == "Scores":
						variation_timer = variation_timer + 1
						if variation_timer > 5:
							variation_timer = 1
					if live_screen_ID == "Fulltime" or live_screen_ID == "Titles" or live_screen_ID == "Halftime" or (
							previousKey == "s" and live_screen_ID == "Scores"):
						temp1score = team1Score
						team1Score = team2Score
						team2Score = temp1score
						temp1name = team1name
						team1name = team2name
						team2name = temp1name
						team1ScoreBox.text = str(team1Score)
						team1ScoreBox.update()
						team2ScoreBox.text = str(team2Score)
						team2ScoreBox.update()
				if on_air == False :
					if event.key == pygame.K_PERIOD:
						if live_screen_ID ==  "Scores":
							adjust_timer(1)
					elif event.key == pygame.K_COMMA:
						if live_screen_ID ==  "Scores":
							adjust_timer(-1)

					if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:  # Team1 score select
						activeTextBox = 3
					if event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:  # Team2 score select
						activeTextBox = 4
					if activeTextBox == 3:  # SCORE1 CHANGE
						if event.key == pygame.K_UP or event.key == pygame.K_KP8:
							team1Score = team1Score + 1
						if event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
							team1Score = team1Score - 1
						team1ScoreBox.text = str(team1Score)
						team1ScoreBox.update()
						team2ScoreBox.text = str(team2Score)
						team2ScoreBox.update()
					if activeTextBox == 4:  # SCORE2 CHANGE
						if event.key == pygame.K_UP or event.key == pygame.K_KP8:
							team2Score = team2Score + 1
						if event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
							team2Score = team2Score - 1
						team1ScoreBox.text = str(team1Score)
						team1ScoreBox.update()
						team2ScoreBox.text = str(team2Score)
						team2ScoreBox.update()
					if activeTextBox == 0:  # Lower third position adjustments...
						if event.key == pygame.K_DOWN and LT_box_position_UP < 1045:
							LT_box_position_UP = LT_box_position_UP + 2
						if event.key == pygame.K_UP and LT_box_position_UP > 700:
							LT_box_position_UP = LT_box_position_UP - 2

	draw_userImages()
	draw_watermark_image()
	draw_replay_image()
	pygame.display.update()
	clock.tick(25)
pygame.quit()
