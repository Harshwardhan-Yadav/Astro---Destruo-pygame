# Name of the game is Astro - Destruo
import pygame
from pygame import mixer
import random
import math
from datetime import datetime
import sys

# We always need to initialize the pygame
pygame.init()


class Button:
    # Constructor for rectangle
    def __init__(self, surface, x, y, width, height):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # Drawing the button
    def drawButton(self):
        pygame.draw.rect(self.surface, (225, 0, 0), (self.x, self.y, self.width, self.height))

    # Drawing the border for button
    def borderDraw(self):
        pygame.draw.rect(self.surface, (0, 255, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 3)

    # Writing text to button
    def text(self, text):
        FoNT = pygame.font.Font('joystix monospace.ttf', 22)
        MessaGE = FoNT.render(text, True, (75, 0, 130))
        screen.blit(MessaGE, (self.x + 5, self.y + 5))

    # Changing the color of button when hovered upon
    def changeColor(self, text):
        pygame.draw.rect(self.surface, (0, 255, 0), (self.x, self.y, self.width, self.height))
        self.text(text)


# Setting a variable for the display name
displayname = 'Anonymous'

# setting the username
username = ''

# Setting the title of Window
pygame.display.set_caption('Astro - Destruo')

# Setting the icon image
icon = pygame.image.load('icon.webp')
pygame.display.set_icon(icon)

# We need to create a window for our game
screen = pygame.display.set_mode((800, 700))

# We need to add a background
background = pygame.image.load('background.jpg').convert()

# Making a planet list
planets = [pygame.image.load('jupiter.png'), pygame.image.load('jupiter1.png'), pygame.image.load('saturn.png'),
           pygame.image.load('mercury.png')]

# Making the current planet list
plist = list()
plistX = list()
plistY = list()

# Adding a background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# defining the position of our character
thanos = pygame.image.load('thanos.png')
thanos_x = 300
thanos_y = 560
gauntlet = pygame.image.load('gauntlet.png')
gauntlet_x = 385
gauntlet_y = 570

# defining the score
score_value = 0
font = pygame.font.Font('joystix monospace.ttf', 16)
textX = 10
textY = 670

# defining the laser
laser = list()
laserX = list()
laserY = list()

# list to store laser indices to be deleted
del_laser = list()

# list to store planet indices to be deleted
del_planet = list()

# lists to store the explosion details
explo_times = list()
exploX = list()
exploY = list()

# Taking the user name
intro_loop = True
tb = False  # Goes to true if the mouse is hovered at the text box
play = False  # Goes to true if the mouse is hovered at the play button
while intro_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro_loop = False
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and tb:
            if event.key == pygame.K_BACKSPACE:
                if len(username) == 0:
                    username = ''
                else:
                    username = username[0:len(username) - 1]
            elif event.key == pygame.K_RETURN:
                intro_loop = False
                break
            elif event.key == pygame.K_SPACE:
                username += '_'
            else:
                username += str(event.unicode)
        elif event.type == pygame.MOUSEBUTTONDOWN and play:
            intro_loop = False
    # Displaying the background
    screen.blit(background, (0, 0))
    # Making a play button
    play_game = Button(screen, 350, 400, 100, 40)
    play_game.drawButton()
    play_game.borderDraw()
    mouse_position = pygame.mouse.get_pos()
    if (mouse_position[0] >= play_game.x) and (mouse_position[1] <= play_game.y + 40) and (
            mouse_position[0] <= play_game.x + max(len(username) * 22 + 10, len('Enter Name') * 22 + 10)) and (
            mouse_position[1] >= play_game.y):
        play_game.changeColor('Play')
        play = True
    else:
        play = False
    play_game.text('Play')
    # making a text box
    text_box = Button(screen, 285, 300, max(len(username) * 22 + 10, len('Enter Name') * 22 + 10), 40)
    text_box.drawButton()
    text_box.borderDraw()
    # setting the text of the textbox
    if username == '':
        text_to_pass = 'Enter Name'
    else:
        text_to_pass = username
    mouse_position = pygame.mouse.get_pos()
    if (mouse_position[0] >= text_box.x) and (mouse_position[1] <= text_box.y + 40) and (
            mouse_position[0] <= text_box.x + max(len(username) * 22 + 10, len('Enter Name') * 22 + 10)) and (
            mouse_position[1] >= text_box.y):
        text_box.changeColor(text_to_pass)
        tb = True
    else:
        tb = False
    text_box.text(text_to_pass)
    pygame.display.update()

# Setting time of start
lower_time = pygame.time.get_ticks()

# Setting the time after which planets are going to be generated
time_limit = 2000

# giving the name to store
if username != '':
    displayname = username


# defining a function to restart the game values, just setting the values to default
def restart():
    global score_value
    explo_times.clear()
    exploX.clear()
    exploY.clear()
    del_planet.clear()
    del_laser.clear()
    laser.clear()
    laserX.clear()
    laserY.clear()
    score_value = 0
    mixer.music.load('background.wav')
    mixer.music.play(-1)
    plist.clear()
    plistX.clear()
    plistY.clear()
    global time_limit
    time_limit = 2000
    global lower_time
    lower_time = pygame.time.get_ticks()


# defining a function to end the game
def gameEnd():
    global running
    # Initially just appending the score in the file
    f = open('Highscores.txt', 'a+')
    f.write(str(score_value) + ' ' + displayname + ' ' + str(datetime.now()) + '\n')
    f.close()
    # Now reading the scores from the file of Highscores.txt
    f = open('Highscores.txt', 'r')
    score_dict = dict()
    # storing the scores in the score_dict dictionary with name, date, time as key making the key unique always and the score as value
    for line in f:
        ll = line.split()
        score_dict[str(ll[1]) + ' ' + str(ll[2]) + ' ' + str(ll[3])] = int(ll[0])
    f.close()
    # Now we sort the above dictionary based on values i.e. scores and create a new dictionary called score_dictionary
    score_sort = sorted(score_dict.values(), reverse=True)  # sorting the dictionary based on values
    score_dictionary = dict()
    for ss in score_sort:  # Iterating through the sorted scores
        for key in score_dict.keys():  # Iterating through keys of the previous dictionary
            if score_dict[key] == ss and score_dictionary.get(
                    key) is None:  # if the key has the same score and has not yet been assigned a value
                score_dictionary[key] = ss
                break
    # till here score_dictionary has been created and now can be used to display highscores
    run = True  # loop to run till the user makes a decision
    mixer.music.stop()  # Stopping the game music
    gameOver = pygame.mixer.Sound('gameover.wav')  # playing the music for game over.
    gameOver.play()
    while run:
        f = open('Highscores.txt', 'w')  # Opening the file in write mode to write the top 500 scores
        fade = pygame.Surface((1920, 1080))  # Creating a surface to fade out the screen and score game over message
        fade.fill((1, 1, 1))
        fade.set_alpha(15)
        screen.blit(fade, (0, 0))
        # Drawing the Button of Play Again
        pA = False  # Used to store if the user wants to play again
        playAgain = Button(screen, 580, 20, 200, 50)
        playAgain.drawButton()
        playAgain.borderDraw()
        playAgain.text('Play Again')
        mouse_position = pygame.mouse.get_pos()
        if (mouse_position[0] >= playAgain.x) and (mouse_position[1] <= playAgain.y + 50) and (
                mouse_position[0] <= playAgain.x + 200) and (mouse_position[1] >= playAgain.y):
            playAgain.changeColor('Play Again')
            # Checking if Play Again Button is pressed then starting the game again
            pA = True
        else:
            pA = False
        # Drawing the Button of Quit
        Q = False
        Quit = Button(screen, 580, 630, 200, 50)
        Quit.drawButton()
        Quit.borderDraw()
        Quit.text('Quit')
        mouse_position = pygame.mouse.get_pos()
        if (mouse_position[0] >= Quit.x) and (mouse_position[1] <= Quit.y + 50) and (
                mouse_position[0] <= Quit.x + 200) and (mouse_position[1] >= Quit.y):
            Quit.changeColor('Quit')
            # Checking if Quit Button is pressed then ending the game
            Q = True
        else:
            Q = False
        # Now showing the message of Highscores
        FoNT = pygame.font.Font('joystix monospace.ttf', 32)
        MessaGE = FoNT.render('High Scores : ', True, (225, 0, 0))
        screen.blit(MessaGE, (50, 150))
        count = 0
        # Loop for showing the top 10 Highscores asa well as writing into the file the top 500 scores from the sorted score_dictionary
        for u in score_dictionary.keys():
            if count > 499:
                break
            key = u.split()  # Splitting the key into name, date, time
            # Displaying the highscores
            if count < 10:
                FonT = pygame.font.Font('joystix monospace.ttf', 32)
                MessagE = FonT.render(str(count + 1) + ' : ' + str(score_dictionary[u]) + " " + str(key[0]), True,
                                      (225, 0, 0))
                screen.blit(MessagE, (50, (160 + (count + 1) * 40)))
            f.write(str(score_dictionary[u]) + ' ' + str(key[0]) + ' ' + str(key[1]) + ' ' + str(key[2]) + '\n')
            count += 1
        f.close()
        # Displaying the Score
        fonT = pygame.font.Font('joystix monospace.ttf', 26)
        messagE = fonT.render('Score : ' + str(score_value), True, (225, 0, 0))
        screen.blit(messagE, (textX, textY))
        # Displaying the Gameover message
        fonT = pygame.font.Font('joystix monospace.ttf', 64)
        message = fonT.render('Game Over', True, (225, 0, 0))
        screen.blit(message, (0, 0))
        # Checking for events
        for evenT in pygame.event.get():
            # If the play again button is pressed then restarting the game
            if evenT.type == pygame.MOUSEBUTTONDOWN and pA:
                restart()
                run = False
                continue
            # If the Quit button is pressed then Quiting the game
            if evenT.type == pygame.MOUSEBUTTONDOWN and Q:
                restart()  # Just to ensure no error occurs
                run = False
                running = False
                continue
            # If the button is pressed anywhere else on the screen where not intended to
            if evenT.type == pygame.MOUSEBUTTONDOWN:
                pass
            if evenT.type == pygame.QUIT:
                restart()  # Just to ensure no error occurs
                run = False
                running = False
        # Updating the screen
        pygame.display.update()


# Defining a function to generate a planet
def generate_planet():
    plist.append(random.choice(planets))
    plistX.append(random.randint(110, 725))
    plistY.append(0)
    screen.blit(plist[len(plist) - 1], (plistX[len(plistX) - 1], 0))


def update_planet(k):
    screen.blit(plist[k], (plistX[k], plistY[k]))


# Defining function to shoot laser from gauntlet
def laser_shoot(g):
    screen.blit(laser[g], (laserX[g], laserY[g]))


# Defining a function to show the score. First we need to render the score and then blit
def score_show():
    score = font.render('Score : ' + str(score_value), True, (255, 255, 0))
    screen.blit(score, (textX, textY))


# Defining a function to set the character onto the screen
# using the screen blit(to draw)
def Thanos_Pos():
    screen.blit(thanos, (thanos_x, thanos_y))
    screen.blit(gauntlet, (gauntlet_x, gauntlet_y))


# Updating the score
def update_score():
    global score_value
    if time_limit == 2000:
        score_value += 1
    elif time_limit == 1800:
        score_value += 2
    elif time_limit == 1600:
        score_value += 4
    elif time_limit == 1400:
        score_value += 8
    elif time_limit == 1200:
        score_value += 16
    elif time_limit == 1000:
        score_value += 32
    elif time_limit == 800:
        score_value += 64
    else:
        score_value *= 1.1
        score_value = round(score_value)


# Updating time limit
def update_time_limit():
    global time_limit
    if score_value <= 20:
        time_limit = 1600
    elif score_value <= 100:
        time_limit = 1400
    elif score_value <= 250:
        time_limit = 1200
    elif score_value <= 600:
        time_limit = 1000
    elif score_value <= 2000:
        time_limit = 800
    else:
        time_limit = 600


# Creating a explosion function
def explosion(p, q):
    del_laser.append(p)
    del_planet.append(q)
    explode_sound = pygame.mixer.Sound('explosion.wav')
    explode_sound.play()
    explo_times.append(0)
    exploX.append(plistX[q])
    exploY.append(plistY[q])
    update_score()
    update_time_limit()


# Game Loop is an infinite loop for running game until exited
running = True
while running:
    for event in pygame.event.get():  # Used to get the events
        if event.type == pygame.QUIT:  # Making the game quit when cross is pressed(Quit Event)
            running = False
        if event.type == pygame.KEYDOWN and len(laser) <= 15:
            if event.key == pygame.K_SPACE:
                laser.append(pygame.image.load('laser.jpg'))
                laserX.append(gauntlet_x + 20)
                laserY.append(570)
                shot_sound = mixer.Sound('laser.wav')
                shot_sound.play()

    # Drawing the screen
    screen.blit(background, (0, 0))

    # Looping to check if there is any explosion between planet and laser
    for i in range(len(laser)):
        for j in range(len(plist)):
            d = math.sqrt(math.pow(laserX[i] - plistX[j], 2) + math.pow(laserY[i] - plistY[j], 2))
            if d <= 32:
                explosion(i, j)

    # updating the image of our character
    mouse_pos = list(pygame.mouse.get_pos())
    thanos_x = int(mouse_pos[0])
    gauntlet_x = thanos_x + 85
    if thanos_x > 640:  # Preventing the character from leaving the screen.
        thanos_x = 640
        gauntlet_x = thanos_x + 85
    Thanos_Pos()
    score_show()

    # Generating planets according to timer
    if pygame.time.get_ticks() - lower_time >= time_limit:
        lower_time = pygame.time.get_ticks()
        generate_planet()

    # Updating lasers
    for i in range(len(laser)):
        laserY[i] -= 3
        if laserY[i] <= 0:
            del_laser.append(i)
            continue
        laser_shoot(int(i))

    # Updating planets
    for i in range(len(plist)):
        plistY[i] += 0.7
        update_planet(int(i))
        if plistY[i] >= 570:
            gameEnd()
            break

    del_explo = list()
    # Displaying explosion
    for i in range(len(exploX)):
        explo_times[i] += 1
        screen.blit(pygame.image.load('explosion.png'), (exploX[i], exploY[i]))
        if explo_times[i] >= 100:
            del_explo.append(i)

    # Deleting the explosion image
    for i in del_explo:
        del (explo_times[i])
        del (exploX[i])
        del (exploY[i])

    # deleting planet
    for v in del_planet:
        del (plist[v])
        del (plistY[v])
        del (plistX[v])
    del_planet.clear()

    # deleting laser
    for v in del_laser:
        del (laser[v])
        del (laserY[v])
        del (laserX[v])
    del_laser.clear()

    # We need to update our screen always Hence
    pygame.display.update()
