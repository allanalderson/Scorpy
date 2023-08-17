'''
4.0 RELEASE.
4.1 key code tidy and timer set adjustment.Bugfix userimages 5-9
4.2 Minor tweeks to greens and better clock routine
4.3 User Image Help
4.4 New fulltime and halftime graphics.
	Timer vanish after 5 seconds below 0:00
	Timer continues to run during INPUT screen.
4.5 Score selection indicator.
4.6 Minor tweeks to score selection screen
4.7 Now responding to a numeric keypad
4.8 Count-up Ready and minor color changes
4.9 Added LT Clock , some refactoring
5.0 Changed 'Resources' folder to 'scorpy_resources'
5.1 Added Watermark
5.2 Bug Fix no score change during Score screen's first run. Code easier to read
5.3 Add score swap Variation (v) during score screen.
5.4 Reset SCORES to zero if TITLES screen displayed.
5.5 Quick access to screens.
5.6 Tidy LT bar. Repair LT double trigger
5.7 Clock callable on-air. Corner position tweaks.
5.8 Refactoring, Quick access score bug fixed.
5.9 Corner and graphics tweaks, removed diagnostic printouts. Drop-shaddow on big SCORES
6.0 Clock display allowed after Replay screen. Team Swap variation allowed on TITLES Screen.
6.1 Added timer adjust with    <   >   keys.
6.11 Changed timer adjust for seconds (not minutes)  when off-air.
6.2 Added Software Version on BARS screen.
6.3 Smart countdown reset with user_minutes.
6.4 Smart erase TITLES & Teams
6.5 Bugfix: timer adjust seconds
6.6 Blue TITLES, Instant Replay.
6.7 Sticky userImage_s 1~9. 0 = kill all userImage_s
6.8 No overlap on user images.
6.9 Tab key on BARS allowed. Replay key kills on-air graphics.
	Showing Timer on first run.
	Score reset on team name change
7.0 Code Tidy.
7.1 Polite Replay routines.
7.1a Refactoring
7.1b more refactoring.
8.0beta
8.0 Polite display. (except input screen)
8.1 Seconds adjust polite.
8.2 Seconds and minutes adjustments are polite.
8.3 Input screen polite.
8.4 Next Up graphic variation installed.
8.6 More Graphics and 6 title variations.
9beta Bug: user_minutes = countdown_minutes
9b1 3 messages Ready.
9b2 user minutes bug fixed
9b3 Nicer input menu behaviour
9b4 Saftey Timer
9b5 Safty Timer accessable in Input screen
9b6 messages3 ok
9.0 Release.
9.1 Tidy up
9.2 blue text now appears as white






'''


import pygame
from pygame.locals import *
import os
import sys


scorpy_version = "Scorpy 9.2"
sys.path.append('../../mnt/volume/')
pygame.init()
windowSizeX = 1920
windowSizeY = 1080
team1Score = 0
team2Score = 0
# sys.path.append('/boot/')
liveshot = False
screen = pygame.display.set_mode([windowSizeX, windowSizeY])
#screen = pygame.display.set_mode([windowSizeX, windowSizeY], pygame.FULLSCREEN)
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
variation_titles = 3
countdown_ticks = (countdown_minutes*60)+(countdown_seconds)
countdownMinutesText = str(countdown_minutes)
previousKey = "0"
showWatermark = False
showReplay = False
counting_down = True
white = (250,250,250)
yellow = (220,200,160)
black = (0,0,0)
blue = (200, 200, 240)
red = (250, 60, 60)
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
showTimer = True
running = True
activeTextBox = 0 # 1&2=teamNames;  3&4=SCORES;  11&12 TITLES
validChars = " `1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = ' ~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
current_screen_name = "BARS"
on_air = True
showImage_1 = False
showImage_2 = False
showImage_3 = False
showImage_4 = False
showImage_5 = False
showImage_6 = False
showImage_7 = False
showImage_8 = False
showImage_9 = False
fontGeneral = pygame.font.Font('scorpy_resources/Fonts/Roboto-Medium.ttf', 55)
fontDigital_big = pygame.font.Font('scorpy_resources/Fonts/digital-7 (mono).ttf', 260)
fontDigital_timer = pygame.font.Font('scorpy_resources/Fonts/digital-7 (mono).ttf', 55)
advertMenu = " Messages...     "
messagesR = fontGeneral.render(advertMenu, True, greenScreen, green2)
advertMenu_rect = messagesR.get_rect()
advertMenu_rect.center = messagesR.get_rect().center # Get it's dimentions.


versionR = fontGeneral.render(scorpy_version, True, grey, black)
version_rect = versionR.get_rect()
version_rect.center = versionR.get_rect().center # Use the center from now on.
# Use it...
# version_rect.center = [windowSizeX / 2, 950]  # Put it somewhere
# screen.blit(versionR, version_rect)



current_screen_name = "BARS"
reqested_screen_name = ""


TITLES_requestText = " Titles                       "
TEAMS_requestText  = " Teams                     "
requestFont = pygame.font.Font('scorpy_resources/Fonts/xxii_geom_slab/XXIIGeomSlabDEMO-Bold.otf', 180)
teamNamesRequestText = requestFont.render(TEAMS_requestText, True, greenScreen, green2)
teamNamesRequestText_rect = teamNamesRequestText.get_rect()
TITLESNamesRequestText = requestFont.render(TITLES_requestText, True, greenScreen, green2)
titleNamesRequestText_rect = TITLESNamesRequestText.get_rect()
bars = screen
help1 = screen
full_screen_rect = [0, 0]
full_screen_rect = bars.get_rect()
full_screen_rect.center = screen.get_rect().center  # Set image centers
bars = pygame.image.load('scorpy_resources/Graphics/bars1080.png').convert()
halfTimeGraphic = pygame.image.load('scorpy_resources/Graphics/halfTimeImage.png').convert_alpha()
nextUpGraphic = pygame.image.load('scorpy_resources/Graphics/upNext.png').convert_alpha()
fullTimeGraphic = pygame.image.load('scorpy_resources/Graphics/fullTimeImage.png').convert_alpha()
help1 = pygame.image.load('scorpy_resources/Graphics/help1.png').convert()
help2 = pygame.image.load('scorpy_resources/Graphics/help2.png').convert()
liveshot_graphic = pygame.image.load('scorpy_resources/Graphics/liveshot.png').convert()
VS_title_graphic1 = pygame.image.load('scorpy_resources/Graphics/VS_graphic1.png').convert_alpha()
VS_title_graphic2 = pygame.image.load('scorpy_resources/Graphics/VS_graphic2.png').convert_alpha()
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
		# self.image = self.font.render(self.text, True, greenMid)
		self.rect = self.image.get_rect()
		self.rect.center = old_rect_pos
	def white(self):
		self.image = self.font.render(self.text, True, white)
	def greenQuiet(self):
		self.image = self.font.render(self.text, True, green2)
	def greenMid(self):
		self.image = self.font.render(self.text, True, green3)
	def greenLoud(self):
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
		self.font = pygame.font.Font('scorpy_resources/Fonts/Roboto-Medium.ttf', 450)
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
majorTitleName.greenMid()
minorTitleName.greenMid()
majorTitleName.update()
minorTitleName.update()

team1name = TextBox()
team2name = TextBox()
team1name.text = "Team1"
team2name.text = "Team2"
team1name.greenMid()
team1name.update()
team2name.greenMid()
team2name.update()
team1ScoreBox = TextBox()
team1ScoreBox.text = str(team1Score)
team2ScoreBox = TextBox()
team2ScoreBox.text = str(team2Score)
lowerThirdText = TextBox()
lowerThirdText.text = ""

message_1 = TextBox()
message_1.text = "Message 1"
message_1.greenQuiet()
message_1.update()

message_2 = TextBox()
message_2.text = "Message 2"
message_2.greenQuiet()
message_2.update()

message_3 = TextBox()
message_3.text = "Message 3"
message_3.greenQuiet()
message_3.update()


showNEXTUP = False

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
useMessage_1 = False
useMessage_2 = False
useMessage_3 = False
try:
	userImage_1 = pygame.image.load('../../mnt/volume/image1.png').convert_alpha()
except:
	userImage_1 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
	useMessage_1 = True
try:
	userImage_2 = pygame.image.load('../../mnt/volume/image2.png').convert_alpha()
except:
	userImage_2 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
	useMessage_2 = True
try:
	userImage_3 = pygame.image.load('../../mnt/volume/image3.png').convert_alpha()
except:
	userImage_3 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
	useMessage_3 = True
try:
	userImage_4 = pygame.image.load('../../mnt/volume/image4.png').convert_alpha()
except:
	userImage_4 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
try:
	userImage_5 = pygame.image.load('../../mnt/volume/image5.png').convert_alpha()
except:
	userImage_5 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
try:
	userImage_6 = pygame.image.load('../../mnt/volume/image6.png').convert_alpha()
except:
	userImage_6 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
try:
	userImage_7 = pygame.image.load('../../mnt/volume/image7.png').convert_alpha()
except:
	userImage_7 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
try:
	userImage_8 = pygame.image.load('../../mnt/volume/image8.png').convert_alpha()
except:
	userImage_8 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()
try:
	userImage_9 = pygame.image.load('../../mnt/volume/image9.png').convert_alpha()
except:
	userImage_9 = pygame.image.load('scorpy_resources/Graphics/missingUserImage.png').convert_alpha()



def erase_screen():
	screen.fill(greenScreen)
	if liveshot == True:
		screen.blit(liveshot_graphic, full_screen_rect)
def draw_INPUT_screen():
	global timer_running
	global countdownTextR
	global countdown_ticks
	global countdown_seconds
	global countdown_minutes
	global messagesR
	team1name.green0()
	team2name.green0()
	majorTitleName.green0()
	minorTitleName.green0()
	if activeTextBox == 1:
		team1name.greenLoud()
	if activeTextBox == 2:
		team2name.greenLoud()
	if activeTextBox == 11:
		majorTitleName.greenLoud()
	if activeTextBox == 12:
		minorTitleName.greenLoud()

	if activeTextBox == 20:
		messagesR = fontGeneral.render(advertMenu, True, green4, green2)
	else:
		messagesR = fontGeneral.render(advertMenu, True, greenScreen, green2)
	majorTitleName.fontMinorTitle()
	minorTitleName.fontMinorTitle()
	team1name.fontMinorTitle()
	team2name.fontMinorTitle()
	screen.blit(TITLESNamesRequestText, [100, 200])
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
	countdownSecondsText = countdownSecondsText + " >  Timer "
	if activeTextBox == 5: # selected.  (timer is stopped)
		countdownText = countdownMinutesText + ":" + countdownSecondsText
		countdownTextR = fontGeneral.render(countdownText, False, green4, green2)  # Render it.
	else:  # not selected
		countdownText = countdownMinutesText + ":" + countdownSecondsText
		if timer_running == False:
			countdownTextR = fontGeneral.render(countdownText, False, greenScreen, green2)  # Render it.
		else: #timer running
			countdownTextR = fontGeneral.render(countdownText, False, green4, greenScreen)  # Render it.
	messageMenu_rect = [800, 720] # Put it somewhere
	screen.blit(messagesR, messageMenu_rect)
	countdown_rect = [800, 850]  # Put the center of the rect somewhere
	screen.blit(countdownTextR, countdown_rect)  # Draw the render, here.
def draw_INPUT_messages():
	screen.blit(message_1.image, [100, 100])
	screen.blit(message_2.image, [100, 200])
	screen.blit(message_3.image, [100, 300])
def draw_LT_screen():
	global LT_rasing
	global LT_lowering
	global transition_trigger
	global LT_counter
	global LT_box_position
	global activeTextBox
	global LT_box_position_UP
	global current_screen_name
	global reqested_screen_name
	global activeTextBox
	global on_air
	if reqested_screen_name == "SCORES":
		activeTextBox = 0
		on_air = False
		current_screen_name = "SCORES"
		reqested_screen_name = ""
	if LT_box_position < 991:
		lowerThirdBoxThickness = 45 # small box 45
	if LT_box_position > 990:
		lowerThirdBoxThickness = 100 # large box 100
	draw_bigGreenTimer()
	team1name.greenMid()
	team2name.greenMid()
	team1ScoreBox.greenMid()
	team2ScoreBox.greenMid()
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
		if LT_box_position_UP < 991:
			lowerThirdBoxThickness = 45  # 45 small box
		if LT_box_position_UP > 990:
			lowerThirdBoxThickness = 100  # 100 large box
		pygame.draw.rect(screen, green3, (0, LT_box_position_UP - 22, windowSizeX, lowerThirdBoxThickness))  #-22
	if LT_lowering == False or LT_rasing == False:
		transition_trigger = False # reset the trigger
	draw_bigGreenScores()
	draw_timer_panel()
def draw_bigGreenScores():
	team1name.fontTeamNameUnderScore()
	team2name.fontTeamNameUnderScore()
	team1name.greenMid()
	team2name.greenMid()
	team1ScoreBox.fontBigPreviewScore()
	team2ScoreBox.fontBigPreviewScore()
	if activeTextBox == 3:
		team1ScoreBox.greenLoud()
		team1name.greenLoud()
		team2ScoreBox.greenQuiet()
		team2name.greenQuiet()
	if activeTextBox == 4:
		team2ScoreBox.greenLoud()
		team2name.greenLoud()
	if activeTextBox == 0:
		team1ScoreBox.greenLoud()
		team2ScoreBox.greenLoud()
		team1name.greenLoud()
		team2name.greenLoud()
	team1name.rect.center = [bigScorePositionLeft, (windowSizeY // 2) + 300]
	team2name.rect.center = [bigScorePositionRight, ((windowSizeY // 2) + 300)]
	team1ScoreBox.rect.center = [bigScorePositionLeft, (windowSizeY // 2) + 70]
	team2ScoreBox.rect.center = [bigScorePositionRight, (windowSizeY // 2) + 70]
	screen.blit(team1name.image, team1name.rect)
	screen.blit(team2name.image, team2name.rect)
	screen.blit(team1ScoreBox.image, team1ScoreBox.rect)
	screen.blit(team2ScoreBox.image, team2ScoreBox.rect)
	draw_bigGreenTimer()
def draw_bigGreenTimer():
	triangleY = 170
	if counting_down == True:
		pygame.draw.polygon(screen, green2, [[(windowSizeX // 2-40), (triangleY+100)], [(windowSizeX // 2+40), (triangleY+100)],[(windowSizeX // 2), (triangleY+130)]])
	else:
		pygame.draw.polygon(screen, green2, [[(windowSizeX // 2-40), (triangleY-100)], [(windowSizeX // 2+40), (triangleY-100)],[(windowSizeX // 2), (triangleY-130)]])
	if timer_running == False:
		countdownTextR = fontDigital_big.render(countdownText, False, green2, green3)  # Render it.
	elif timer_running == True and activeTextBox == 0:
		countdownTextR = fontDigital_big.render(countdownText, False, green4)  # Render it.
	else:
		countdownTextR = fontDigital_big.render(countdownText, False, green3)  # Render it.
	countdown_rect = countdownTextR.get_rect()  # Get the render's rect
	countdown_rect.center = [windowSizeX // 2, 170]  # Put the center of the rect somewhere
	screen.blit(countdownTextR, countdown_rect)  # Draw the render, here.
def draw_HalfFulltime_scores():
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
def draw_offair_filter():
	global team1Score
	global team2Score
	if on_air == False:
		screen.blit(green_filter, full_screen_rect)
	else:
		#  Reset SCORES to zero if TITLES displayed.
		if previousKey =="space" and current_screen_name == "TITLES":
			team1Score = 0
			team2Score = 0
			team1ScoreBox.text = str(team1Score)
			team1ScoreBox.update()
			team2ScoreBox.text = str(team2Score)
			team2ScoreBox.update()
def draw_user_data():
	if showImage_1 == True:
		message_1centers = message_1.image.get_rect().center
		if useMessage_1 == True:
			if current_screen_name == "SCORES":
				goOffAir()
			message_1.fontLowerThird()
			message_1.black()
			screen.blit(message_1.image, [windowSizeX / 2 - message_1centers[0], LT_box_position_UP - 26]) # LT_box_position_UP-20
		else:
			screen.blit(userImage_1, full_screen_rect)  # Draw it.
	elif showImage_2 == True:
		message_2centers = message_2.image.get_rect().center
		if useMessage_2 == True:
			if current_screen_name == "SCORES":
				goOffAir()
			message_2.fontLowerThird()
			message_2.black()
			screen.blit(message_2.image,
			            [windowSizeX / 2 - message_2centers[0], LT_box_position_UP - 26])  # LT_box_position_UP-20
		else:
			screen.blit(userImage_2, full_screen_rect)  # Draw it.
	elif showImage_3 == True:
		message_3centers = message_3.image.get_rect().center
		if useMessage_3 == True:
			if current_screen_name == "SCORES":
				goOffAir()
			message_3.fontLowerThird()
			message_3.black()
			screen.blit(message_3.image,
			            [windowSizeX / 2 - message_3centers[0], LT_box_position_UP - 26])  # LT_box_position_UP-20
		else:
			screen.blit(userImage_3, full_screen_rect)  # Draw it.
	elif showImage_4 == True:
		screen.blit(userImage_4, full_screen_rect)  # Draw it.
	elif showImage_5 == True:
		screen.blit(userImage_5, full_screen_rect) # Draw it.
	elif showImage_6 == True:
		screen.blit(userImage_6, full_screen_rect)  # Draw it.
	elif showImage_7 == True:
		screen.blit(userImage_7, full_screen_rect) # Draw it.
	elif showImage_8 == True:
		screen.blit(userImage_8, full_screen_rect)  # Draw it.
	elif showImage_9 == True:
		screen.blit(userImage_9, full_screen_rect)  # Draw it.
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
	if countdown_ticks < -2:
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
		countdown_rect.center = [(windowSizeX // 2), LT_box_position]
	screen.blit(countdownTextR, countdown_rect)  # Draw the render, here.
def draw_WATERMARK_graphic():
	if showWatermark == True:
		if variation_watermark == 1:
			watermark_rect.center = corner1  # Put it somewhere
		elif variation_watermark == 2:
			watermark_rect.center = corner2  # Put it somewhere
		elif variation_watermark == 3:
			watermark_rect.center = corner3  # Put it somewhere
		elif variation_watermark == 4:
			watermark_rect.center = corner4  # Put it somewhere
		screen.blit(watermark, watermark_rect)  # Draw it.
def draw_REPLAY_graphic():
	if showReplay == True:
		if variation_replay == 1:
			replay_rect.center = corner1
		elif variation_replay == 2:
			replay_rect.center = corner2
		elif variation_replay == 3:
			replay_rect.center =corner3
		elif variation_replay == 4:
			replay_rect.center = corner4
		screen.blit(replay, replay_rect)
def adjust_seconds(tick_delta):
	global countdown_ticks
	global countdown_seconds
	global countdown_minutes
	if current_screen_name == "SCORES" and on_air == True:
			goOffAir()
	else:
		countdown_ticks = countdown_ticks + tick_delta
		countdown_seconds = countdown_ticks % 60
		countdown_minutes = countdown_ticks//60
		update_clocks()
def killUserImages():
	global showImage_1
	global showImage_2
	global showImage_3
	global showImage_4
	global showImage_5
	global showImage_6
	global showImage_7
	global showImage_8
	global showImage_9
	showImage_1 = False
	showImage_2 = False
	showImage_3 = False
	showImage_4 = False
	showImage_5 = False
	showImage_6 = False
	showImage_7 = False
	showImage_8 = False
	showImage_9 = False
def updateScoreText():
	team1ScoreBox.text = str(team1Score)
	team1ScoreBox.update()
	team2ScoreBox.text = str(team2Score)
	team2ScoreBox.update()
def goOffAir():
	global on_air
	global transition_trigger
	if LT_box_position == LT_box_position_UP:
		transition_trigger = True
	on_air = False
def swapTeamNamePositions():
	global team1Score
	global team2Score
	global team1name
	global team2name

	temp1score = team1Score
	team1Score = team2Score
	team2Score = temp1score
	temp1name = team1name
	team1name = team2name
	team2name = temp1name
def updateScreen():
	global current_screen_name
	global reqested_screen_name
	global showReplay
	global countdown_ticks
	global user_minutes
	global timer_running

	if LT_box_position == LT_box_position_DOWN: # This is the condition.
		if reqested_screen_name == "BARS":
			current_screen_name = "BARS"
			reqested_screen_name = ""
			goOffAir()
		elif reqested_screen_name == "TITLES":
			current_screen_name = "TITLES"
			reqested_screen_name = ""
			goOffAir()
		elif reqested_screen_name == "HALFTIME":
			current_screen_name = "HALFTIME"
			reqested_screen_name = ""
			goOffAir()
		elif reqested_screen_name == "FULLTIME":
			current_screen_name = "FULLTIME"
			reqested_screen_name = ""
			goOffAir()
		elif reqested_screen_name == "HELP1":
			current_screen_name = "HELP1"
			reqested_screen_name = ""
			goOffAir()
		elif reqested_screen_name == "SCORES":
			current_screen_name = "SCORES"
			reqested_screen_name = ""
			goOffAir()
		elif reqested_screen_name == "REPLAY":
			showReplay = True
			reqested_screen_name = ""
			goOffAir()
		elif reqested_screen_name == "INPUT":
			current_screen_name = "INPUT"
			reqested_screen_name = ""
			goOffAir()
		elif reqested_screen_name == "ADVERTS":
			current_screen_name = "ADVERTS"
			reqested_screen_name = ""
			goOffAir()
	if current_screen_name == "BARS":
		screen.blit(bars, full_screen_rect)
		version_rect.center = [windowSizeX / 2, 140]  # Put it somewhere
		screen.blit(versionR, version_rect)
		draw_offair_filter()
	elif current_screen_name == "TITLES":
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
		if variation_titles == 1: # Just title
			screen.blit(majorTitleName.image, majorTitleName.rect)
			screen.blit(minorTitleName.image, minorTitleName.rect)
		if variation_titles == 2:#  Title and upNext
			screen.blit(majorTitleName.image, majorTitleName.rect)
			screen.blit(minorTitleName.image, minorTitleName.rect)
			screen.blit(nextUpGraphic, full_screen_rect)  # Draw it.
		if variation_titles == 3:# Title, Names and Graphic1
			screen.blit(majorTitleName.image, majorTitleName.rect)
			screen.blit(minorTitleName.image, minorTitleName.rect)
			screen.blit(VS_title_graphic1, full_screen_rect)
			screen.blit(team1name.image, team1name.rect)
			screen.blit(team2name.image, team2name.rect)
		if variation_titles == 4:  # Title, Names  Graphic1 and Next up
			screen.blit(majorTitleName.image, majorTitleName.rect)
			screen.blit(minorTitleName.image, minorTitleName.rect)
			screen.blit(VS_title_graphic1, full_screen_rect)
			screen.blit(team1name.image, team1name.rect)
			screen.blit(team2name.image, team2name.rect)
			screen.blit(nextUpGraphic, full_screen_rect)  # Draw it.
		if variation_titles == 5:  # Title, Names  Graphic2
			screen.blit(majorTitleName.image, majorTitleName.rect)
			screen.blit(minorTitleName.image, minorTitleName.rect)
			screen.blit(VS_title_graphic2, full_screen_rect)
			screen.blit(team1name.image, team1name.rect)
			screen.blit(team2name.image, team2name.rect)
		if variation_titles == 6:  # Title, Names  Graphic2 and Next up
			screen.blit(majorTitleName.image, majorTitleName.rect)
			screen.blit(minorTitleName.image, minorTitleName.rect)
			screen.blit(VS_title_graphic2, full_screen_rect)
			screen.blit(team1name.image, team1name.rect)
			screen.blit(team2name.image, team2name.rect)
			screen.blit(nextUpGraphic, full_screen_rect)  # Draw it.
		draw_offair_filter()
	elif current_screen_name == "HALFTIME":
		if countdown_ticks < 1:
			countdown_ticks = user_minutes * 60
			timer_running = False
		screen.blit(halfTimeGraphic, full_screen_rect)
		draw_HalfFulltime_scores()
		draw_offair_filter()
	elif current_screen_name == "FULLTIME":
		if countdown_ticks < 1:
			countdown_ticks = user_minutes * 60
			timer_running = False
		screen.blit(fullTimeGraphic, full_screen_rect)
		draw_HalfFulltime_scores()
		draw_offair_filter()
	elif current_screen_name == "HELP1":
		screen.blit(help1, full_screen_rect)
		activeTextBox = 0
	elif current_screen_name == "HELP2":
		screen.blit(help2, full_screen_rect)
		on_air = False
	elif current_screen_name == "INPUT":
		draw_INPUT_screen()
	elif current_screen_name == "SCORES":
		draw_LT_screen()
	elif current_screen_name == "ADVERTS":
		draw_INPUT_messages()

	draw_user_data()
	draw_WATERMARK_graphic()
	draw_REPLAY_graphic()



# ------------------------------------------------
pygame.time.set_timer(USEREVENT + 0, 1000)
while running:
	erase_screen()
	for event in pygame.event.get():
		if event.type == USEREVENT + 0:
			update_tick()
		elif event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_r:
				showReplay = False
				reqested_screen_name = ""
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
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if current_screen_name == "HELP2":
					pygame.quit()
					quit()
			elif event.key == pygame.K_TAB:
				if current_screen_name == "INPUT":  # if INPUT screen true then
					current_screen_name = "SCORES"  # exit.
					activeTextBox = 0
					user_minutes = countdown_minutes
					if countdown_seconds == 0 and countdown_minutes == 0:
						counting_down = False
						timer_running = False
					else:
						counting_down = True
						# timer_running = False
				else:
					reqested_screen_name = "INPUT"
					activeTextBox = 11  #make active
					killUserImages()
					goOffAir()

# activeTextBox 0=none; 11=Major; 12=Minor; 1=team1; 2=team2; 5=timer; 20=AdvertsMenu; >20=AdvertsInput

			if activeTextBox == 11:  # major title
				if event.key == pygame.K_DOWN or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
					activeTextBox = 12  # minor title
				elif event.key == pygame.K_SPACE:
					majorTitleName.text += " "
					majorTitleName.update()
				elif event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
					shiftDown = True
				elif event.key == pygame.K_BACKSPACE:
					majorTitleName.text = majorTitleName.text[:-1]
				majorTitleName.add_chr(pygame.key.name(event.key))
				majorTitleName.update()
			elif activeTextBox == 12:  # minor title
				if event.key == pygame.K_UP:
					activeTextBox = 11
				elif event.key == pygame.K_DOWN or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
					activeTextBox = 1  #
				elif event.key == pygame.K_SPACE:
					minorTitleName.text += " "
					minorTitleName.update()
				elif event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
					shiftDown = True
				elif event.key == pygame.K_BACKSPACE:
					minorTitleName.text = minorTitleName.text[:-1]
				minorTitleName.add_chr(pygame.key.name(event.key))
				minorTitleName.update()
			elif activeTextBox == 1:  #team1 Name set
				if event.key == pygame.K_DOWN or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
					activeTextBox = 2
				elif event.key == pygame.K_UP:
					activeTextBox = 12
				elif event.key == pygame.K_SPACE:
					team1name.text += " "
					team1name.update()
				elif event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
					shiftDown = True
				elif event.key == pygame.K_BACKSPACE:
					team1name.text = team1name.text[:-1]
					team1Score = 0
					team2Score = 0
					updateScoreText()
				team1name.add_chr(pygame.key.name(event.key))
				team1name.update()
			elif activeTextBox == 2:  #team2 Name set
				if event.key == pygame.K_DOWN or event.key == pygame.K_RETURN:
					activeTextBox = 20
				elif event.key == pygame.K_UP:
					activeTextBox = 1
				elif event.key == pygame.K_SPACE:
					team2name.text += " "
					team2name.update()
				elif event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
					shiftDown = True
				elif event.key == pygame.K_BACKSPACE:
					team2name.text = team2name.text[:-1]
					team2Score = 0
					team2Score = 0
					updateScoreText()
				team2name.add_chr(pygame.key.name(event.key))
				team2name.update()
			elif activeTextBox == 20: # Adverts Select
				if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
					timer_running = False
				elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
					timer_running = True
				elif event.key == K_UP:
					activeTextBox = 2 # go up
				elif event.key == pygame.K_RETURN:
					current_screen_name = "ADVERTS"
					activeTextBox = 21
				elif event.key == pygame.K_DOWN:
					if timer_running == False:
						activeTextBox = 5
						countdown_seconds = 0
				if activeTextBox > 20:
					message_1.greenLoud()
					message_2.greenQuiet()
					message_3.greenQuiet()
					break
			elif activeTextBox == 21: # The first one
				if event.key == pygame.K_UP:
					activeTextBox = 2
					reqested_screen_name = "INPUT"
					break
				if event.key == pygame.K_DOWN or event.key == pygame.K_RETURN:
					activeTextBox += 1
					message_1.greenQuiet()
					message_2.greenLoud()
					message_3.greenQuiet()
					break
				if event.key == pygame.K_SPACE:
					message_1.text += " "
				elif event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
					shiftDown = True
				elif event.key == pygame.K_BACKSPACE:
					message_1.text = message_1.text[:-1]
				message_1.add_chr(pygame.key.name(event.key))
				message_1.greenLoud()
				message_2.greenQuiet()
				message_3.greenQuiet()

			elif activeTextBox == 22: # The middle one
				if event.key == pygame.K_UP:
					activeTextBox -= 1
					message_1.greenLoud()
					message_2.greenQuiet()
					message_3.greenQuiet()
					break
				if event.key == pygame.K_DOWN or event.key == pygame.K_RETURN:
					activeTextBox += 1
					message_1.greenQuiet()
					message_2.greenQuiet()
					message_3.greenLoud()
					break
				if event.key == pygame.K_SPACE:
					message_2.text += " "
				elif event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
					shiftDown = True
				elif event.key == pygame.K_BACKSPACE:
					message_2.text = message_2.text[:-1]
				message_2.add_chr(pygame.key.name(event.key))
				message_1.greenQuiet()
				message_2.greenLoud()
				message_3.greenQuiet

			elif activeTextBox == 23: # The last one
				if event.key == pygame.K_UP:
					activeTextBox -= 1
					message_1.greenQuiet()
					message_2.greenLoud()
					message_3.greenQuiet()
					break
				elif  event.key == pygame.K_RETURN:
					activeTextBox = 11
					reqested_screen_name = "INPUT"
					message_1.greenQuiet()
					message_2.greenQuiet()
					message_3.greenQuiet()
					break
				elif event.key == pygame.K_SPACE:
					message_3.text += " "
				elif event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
					shiftDown = True
				elif event.key == pygame.K_BACKSPACE:
					message_3.text = message_3.text[:-1]
				message_3.add_chr(pygame.key.name(event.key))
				message_1.greenQuiet()
				message_2.greenQuiet()
				message_3.greenLoud()

			elif activeTextBox == 5:  #timer set
				if event.key == pygame.K_UP:
					activeTextBox = 20
				if event.key == pygame.K_RETURN:
					current_screen_name = "SCORES"  # exit.
					activeTextBox = 0
					user_minutes = countdown_minutes
				if event.key == pygame.K_LEFT:
					if countdown_minutes > 20 and countdown_minutes % 5 == 0:
						countdown_minutes = countdown_minutes - 5
					else:
						if countdown_minutes > 0:
							countdown_minutes = countdown_minutes - 1
							if countdown_minutes < 1 and countdown_seconds < 1:
								counting_down = False
				if event.key == pygame.K_RIGHT:
					if countdown_minutes > 24 and countdown_minutes % 5 == 0:
						countdown_minutes = countdown_minutes + 5
					else:
						countdown_minutes = countdown_minutes + 1
				if event.key == pygame.K_PERIOD:
					adjust_seconds(1)
				if event.key == pygame.K_COMMA:
					adjust_seconds(-1)
			else:  # ------ NOT THE INPUT SCREEN
				if event.key == pygame.K_PERIOD:
					adjust_seconds(1)
				elif event.key == pygame.K_COMMA:
					adjust_seconds(-1)
				elif event.key == pygame.K_GREATER: # Doesn't work on mac?
					adjust_seconds(60)
				elif event.key == pygame.K_LESS:
					adjust_seconds(-60)
				elif event.key == pygame.K_t:
					previousKey = "t"
					killUserImages()
					reqested_screen_name = "TITLES"
					if LT_box_position != LT_box_position_DOWN:
						goOffAir()
				elif event.key == pygame.K_f:
					killUserImages()
					reqested_screen_name = "FULLTIME"
					if LT_box_position != LT_box_position_DOWN:
						goOffAir()
				elif event.key == pygame.K_h:
					killUserImages()
					reqested_screen_name = "HALFTIME"
					if LT_box_position != LT_box_position_DOWN:
						goOffAir()
				elif event.key == pygame.K_s:
					previousKey = "s"
					killUserImages()
					reqested_screen_name = "SCORES"
					if LT_box_position != LT_box_position_DOWN:
						goOffAir()
				elif event.key == pygame.K_b:
					killUserImages()
					if current_screen_name == "BARS":
						current_screen_name = "SCORES"
					else:
						reqested_screen_name = "BARS"
						if LT_box_position != LT_box_position_DOWN:
							goOffAir()
				elif event.key == pygame.K_QUESTION or event.key == pygame.K_SLASH:
					previousKey = "?"
					if current_screen_name != "HELP1":
						killUserImages()
						reqested_screen_name = "HELP1"
						if LT_box_position != LT_box_position_DOWN:
							goOffAir()
					else:
						current_screen_name = "SCORES"
				elif event.key == pygame.K_w:
					previousKey = "w"
					showWatermark = not showWatermark
				elif event.key == pygame.K_r:
					killUserImages()
					reqested_screen_name = "REPLAY"
					if LT_box_position != LT_box_position_DOWN:
						goOffAir()
					previousKey = "r"
				elif event.key == pygame.K_1:
					if showImage_1 == True:
						showImage_1 = False
					else:
						killUserImages()
						showImage_1 = True
				elif event.key == pygame.K_2:
					if showImage_2 == True:
						showImage_2 = False
					else:
						killUserImages()
						showImage_2 = True
				elif event.key == pygame.K_3:
					if showImage_3 == True:
						showImage_3 = False
					else:
						killUserImages()
						showImage_3 = True
				elif event.key == pygame.K_4:
					if showImage_4 == True:
						showImage_4 = False
					else:
						killUserImages()
						showImage_4 = True
				elif event.key == pygame.K_5:
					if showImage_5 == True:
						showImage_5 = False
					else:
						killUserImages()
						showImage_5 = True
				elif event.key == pygame.K_6:
					if showImage_6 == True:
						showImage_6 = False
					else:
						killUserImages()
						showImage_6 = True
				elif event.key == pygame.K_7:
					if showImage_7 == True:
						showImage_7 = False
					else:
						killUserImages()
						showImage_7 = True
				elif event.key == pygame.K_8:
					if showImage_8 == True:
						showImage_8 = False
					else:
						killUserImages()
						showImage_8 = True
				elif event.key == pygame.K_9:
					if showImage_9 == True:
						showImage_9 = False
					else:
						killUserImages()
						showImage_9 = True
				elif event.key == pygame.K_0:
					killUserImages()
				elif event.key == pygame.K_SPACE:
					showImage_1 = False
					showImage_2 = False
					showImage_3 = False
					previousKey = "space"
					if activeTextBox > 0:
						activeTextBox = 0
					on_air = not on_air
					transition_trigger = True
					if current_screen_name == "BARS" and activeTextBox == -1:
						current_screen_name = "HELP1"
						on_air = False
						activeTextBox = 11
				elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
					timer_running = False
				elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
					timer_running = True
				elif event.key == pygame.K_c or event.key == pygame.K_KP_MULTIPLY:
					if current_screen_name == "SCORES":
						previousKey = "c"
						showTimer = not showTimer
				elif event.key == pygame.K_v:
					if current_screen_name == "HELP2":
						current_screen_name = "HELP1"
					elif current_screen_name == "HELP1":
						current_screen_name = "HELP2"
					if previousKey == "r":
						variation_replay = variation_replay + 1
						if variation_replay > 4:
							variation_replay = 1
					if previousKey == "w":
						variation_watermark = variation_watermark + 1
						if variation_watermark > 4:
							variation_watermark = 1
					if previousKey == "c" and current_screen_name == "SCORES":
						variation_timer = variation_timer + 1
						if variation_timer > 5:
							variation_timer = 1
					if previousKey == "s" and current_screen_name == "SCORES":
						swapTeamNamePositions()
						updateScoreText()
					if  current_screen_name == "TITLES":
						variation_titles = variation_titles + 1
						goOffAir()
						if variation_titles > 6:
							variation_titles = 1

				if on_air == False :
					if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:  # Team1 score select
						activeTextBox = 3
					elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:  # Team2 score select
						activeTextBox = 4
					elif activeTextBox == 3:  # SCORE1 CHANGE
						if event.key == pygame.K_UP or event.key == pygame.K_KP8:
							team1Score = team1Score + 1
						if event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
							team1Score = team1Score - 1
						updateScoreText()
					elif activeTextBox == 4:  # SCORE2 CHANGE
						if event.key == pygame.K_UP or event.key == pygame.K_KP8:
							team2Score = team2Score + 1
						if event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
							team2Score = team2Score - 1
						updateScoreText()
					elif activeTextBox == 0:  # Lower third position adjustments...
						if event.key == pygame.K_DOWN and LT_box_position_UP < 1045:
							LT_box_position_UP = LT_box_position_UP + 2
						if event.key == pygame.K_UP and LT_box_position_UP > 700:
							LT_box_position_UP = LT_box_position_UP - 2



	updateScreen()
	pygame.display.update()
	clock.tick(25) # 25
pygame.quit()
