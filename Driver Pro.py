from multiprocessing.connection import answer_challenge
import pygame
import random
import math
import sqlite3
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()

width = 1600
height = 900

SURFACE_COLOR = (255, 255, 255)
COLOR = (100,100,100)

window = pygame.display.set_mode((width,height))
pygame.display.set_caption('Driver Pro')

car = pygame.image.load("/Users/matthewmontgomery/Desktop/Driver Pro/car.png").convert()
car = pygame.transform.scale(car,(60,30))
longvertical = pygame.image.load("/Users/matthewmontgomery/Desktop/Driver Pro/longvertical.jpg").convert()
longvertical = pygame.transform.scale(longvertical,(100,200))
longhorizontal = pygame.image.load("/Users/matthewmontgomery/Desktop/Driver Pro/longhorizontal.jpg").convert()
longhorizontal = pygame.transform.scale(longhorizontal,(200,100))
shortvertical = pygame.image.load("/Users/matthewmontgomery/Desktop/Driver Pro/shortvertical.jpg").convert()
shortvertical = pygame.transform.scale(shortvertical,(100,100))
shorthorizontal = pygame.image.load("/Users/matthewmontgomery/Desktop/Driver Pro/shorthorizontal.jpg").convert()
shorthorizontal = pygame.transform.scale(shorthorizontal,(100,100))
curveBL = pygame.image.load("/Users/matthewmontgomery/Desktop/Driver Pro/curveBL.gif").convert()
curveBL = pygame.transform.scale(curveBL,(150,150))
curveTL = pygame.image.load("/Users/matthewmontgomery/Desktop/Driver Pro/curveTL.gif").convert()
curveTL = pygame.transform.scale(curveTL,(150,150))
curveBR = pygame.image.load("/Users/matthewmontgomery/Desktop/Driver Pro/curveBR.gif").convert()
curveBR = pygame.transform.scale(curveBR,(150,150))
curveTR = pygame.image.load("/Users/matthewmontgomery/Desktop/Driver Pro/curveTR.gif").convert()
curveTR = pygame.transform.scale(curveTR,(150,150))
startvertical = pygame.image.load("/Users/matthewmontgomery/Desktop/Driver Pro/startvertical.gif").convert()
startvertical = pygame.transform.scale(startvertical,(100,30))
starthorizontal = pygame.image.load("/Users/matthewmontgomery/Desktop/Driver Pro/starthorizontal.gif").convert()
starthorizontal = pygame.transform.scale(starthorizontal,(30,100))

font1 = pygame.font.Font(None, 32)

laps_completed_text = font1.render('Laps completed: ', True, (0,0,0))
laps_completed_textRect = laps_completed_text.get_rect()
countdown_text = font1.render('', True, (0,0,0))
countdown_textRect = countdown_text.get_rect()
race_time_text = font1.render('', True, (0,0,0))
race_time_textRect = race_time_text.get_rect()
previous_lap_text = font1.render('Previous Lap:', True, (0,0,0))
previous_lap_textRect = previous_lap_text.get_rect()
best_lap_text = font1.render('', True, (0,0,0))
best_lap_textRect = best_lap_text.get_rect()

global checkpoints
checkpoints = []
global lap_time
lap_time = 0
global previous_lap, best_lap
global bestLapSeconds
bestLapSeconds = 0
best_lap = ""
previous_lap = ""
global race_length



class StartVerticalTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = startvertical
        self.image = startvertical
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = startvertical.get_rect(center=(
                300,
                300,
            ))

class StartHorizontalTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = starthorizontal
        self.image = starthorizontal
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = starthorizontal.get_rect(center=(
                300,
                300,
            ))


class LongVerticalTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = longvertical
        self.image = longvertical
      
        self.image.set_colorkey((255, 255,255), RLEACCEL)
        self.rect = longvertical.get_rect(center=(
                300,
                300,
            ))

class LongHorizontalTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = longhorizontal
        self.image = longhorizontal
      
        self.image.set_colorkey((255, 255,255), RLEACCEL)
        self.rect = longhorizontal.get_rect(center=(
                300,
                300,
            ))

class CurveBLTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = curveBL
        self.image = curveBL
        
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = curveBL.get_rect(center=(
                300,
                300,
            ))

class CurveTRTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = curveTR
        self.image = curveTR
        
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = curveTR.get_rect(center=(
                300,
                300,
            ))

class CurveBRTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = curveBR
        self.image = curveBR
        
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = curveBR.get_rect(center=(
                300,
                300,
            ))


class CurveTLTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = curveTL
        self.image = curveTL
        
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = curveTL.get_rect(center=(
                300,
                300,
            ))
      
     
        

       

        


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super(Car, self).__init__()
        self.surf = car
        self.Rotated_image = car
        self.image = car
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = car.get_rect(
            center=(
                80,
                30,
            )
        )
        self.accelerate = False
        self.reverse = False
        self.speed = 0
        self.direction = 0
        self.absdirection = 0
        self.turnleft = False
        self.turnright = False
        self.xspeed = 0
        self.yspeed = 0
        self.orientation = 0
        self.currentorientation = 0
        self.angle = 0
        self.maxangle = 0
        self.minangle = 90
        self.chasemaxangle = False
        self.chaseminangle = False
        self.previousangle = 0
        self.turnspeed = 1
        self.onTrack = False
        self.lapsCompleted = 0
        

    def update(self):
       

        #change direction of car if on track
        if self.onTrack == True:
            if self.turnleft == True and self.speed>2.5:
                self.turnspeed = (28 - self.speed) / 4
                self.direction += self.turnspeed
                if self.direction >=360:
                    car1.direction = 0
            if self.turnright == True and self.speed>2.5:
                self.turnspeed = (28 - self.speed) / 4
                self.direction -= self.turnspeed
                if self.direction <=-360:
                    self.direction = 0

        #change direction of car if off track
        if self.onTrack == False:

            if self.turnleft == True and self.speed>1.5:
                self.turnspeed = (25 - self.speed) / 6
                self.direction += self.turnspeed
                if self.direction >=360:
                    self.direction = 0
            if self.turnright == True and self.speed>1.5:
                self.turnspeed = (25 - self.speed) / 6
                self.direction -= self.turnspeed
                if self.direction <=-360:
                    self.direction = 0
        
        #calculate absolute direction
        self.absdirection = self.direction
        if self.absdirection < 0:
            self.absdirection +=360

        if self.absdirection >= 0 and self.absdirection < 90:
            self.orientation = 0
        if self.absdirection >= 90 and self.absdirection < 180:
            self.orientation = 1
        if self.absdirection >= 180 and self.absdirection < 270:
            self.orientation = 2
        if self.absdirection >= 270 and self.absdirection < 360:
            self.orientation = 3

        self.angle = self.absdirection - self.orientation*90
        if self.orientation == 1:
            self.angle -=90
            self.angle *=-1
        if self.orientation == 3:
            self.angle -=90
            self.angle *=-1

        if self.chaseminangle == False and self.chasemaxangle == False:
           
            if self.angle>self.maxangle:
                self.maxangle = self.angle
        
        if self.maxangle > self.previousangle:
            self.chasemaxangle = True

        if self.chasemaxangle == True:
            if self.angle>self.maxangle:
                self.maxangle = self.angle

        if self.minangle < self.previousangle:
            self.chaseminangle = True 
       
        if self.chaseminangle == True:
            if self.angle < self.minangle:
                self.minangle = self.angle
       
      

        
        wait = False
        traction = 4 - self.speed/8

        if self.chaseminangle == True:
            if (self.previousangle - self.minangle) > traction:
                self.previousangle -=traction
            if self.previousangle <=self.minangle+traction:
                self.chaseminangle = False
                self.chasemaxangle = True
                self.maxangle = self.minangle
                self.minangle = 90
                self.currentorientation = self.orientation
                wait = True
        
        if self.chasemaxangle == True and wait == False:
            if (self.maxangle - self.previousangle) > traction:
                self.previousangle +=traction
            if self.previousangle >=self.maxangle-traction:
                
                self.chasemaxangle = False
                self.chaseminangle = True
                self.minangle = self.maxangle
                self.maxangle = 0
                self.currentorientation = self.orientation


        print(traction)
        

      
       

        if self.accelerate == True and self.onTrack == True and self.speed<20:
            
            if self.speed == 0:
                self.speed = 1.5
            self.speed +=0.4
        if self.accelerate == True and self.onTrack == False and self.speed<5:
            if self.speed == 0:
                self.speed = 1
            self.speed +=0.4
        if self.accelerate == False and self.speed>0:
            self.speed -=0.4
            if self.speed <=1.5:
                self.speed = 0
        
        if self.reverse == True and self.speed>0:
            self.speed -=0.3

        if self.onTrack == False and self.speed>8:
            self.speed -=2
        

        
        if self.speed>0:
            self.xspeed = self.speed
            rad_direction = self.previousangle*0.0175
            self.yspeed = math.tan(rad_direction) * self.xspeed
            abspeed = math.sqrt((self.xspeed*self.xspeed) + (self.yspeed*self.yspeed))
            speedadjust = abspeed/self.speed
            self.xspeed = self.xspeed / speedadjust
            self.yspeed = self.yspeed / speedadjust
        
  

            if self.currentorientation == 0:
                self.yspeed *=-1
            if self.currentorientation == 1:
                self.yspeed *=-1
                self.xspeed *=-1
            if self.currentorientation == 2:
                self.xspeed *=-1
        
        if self.speed == 0:
            self.xspeed = 0
            self.yspeed = 0



        #rotate car
        w, h = self.surf.get_size()
        pos = self.rect.center 
        blitRotate(self.surf, pos, (w/2, h/2), self.direction)
        self.Rotated_image = rotated_image
        self.image = rotated_image
        self.rect = rotated_image.get_rect(center = rotated_image_center)


        self.rect.move_ip(self.xspeed, self.yspeed)  



def createOvalTrack():

    global checkpoints
    checkpoints = []
    completed = False

    track = CurveTLTrack()
    track.rect.topleft = (300,150)
    TrackPieces.add(track)

    track = LongVerticalTrack()
    track.rect.topleft = (300,300)
    checkpoints.append([3,track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = CurveBLTrack()
    track.rect.topleft = (300,500)
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (450,550)
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (650,550)
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (850,550)
    TrackPieces.add(track)

    track = CurveBRTrack()
    track.rect.topleft = (1050,500)
    TrackPieces.add(track)

    track = LongVerticalTrack()
    track.rect.topleft = (1100,300)
    checkpoints.append([1, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = CurveTRTrack()
    track.rect.topleft = (1050,150)
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (450,150)
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (650,150)
    checkpoints.append([2,track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (850,150)
    TrackPieces.add(track)

    track = StartHorizontalTrack()
    track.rect.topleft = (650,550)
    checkpoints.append([4, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    #print(checkpoints[3][0])

    

def checkpointsCheck (car, checkpoints):
    global lap_time
    global best_lap
    global previous_lap, best_lap, bestLapSeconds
    length = len(checkpoints)

    for i in range(length):
        canComplete = True
        for x in range(length):
            if checkpoints[x][0] == length-i:
                canComplete = True
                for j in range(length):
                    if checkpoints[j][0]< length-i:
                        if checkpoints[j][2] == False:
                            canComplete = False
                            
                if canComplete == True:
                    if checkpoints[x][0]<length:
                        if car.rect.centerx > checkpoints[x][1][0]-75 and car.rect.centerx < checkpoints[x][1][0]+75 and car.rect.centery > checkpoints[x][1][1]-75 and car.rect.centery < checkpoints[x][1][1]+75:
                            checkpoints[x][2] = True
                    else:
                        if car.rect.centerx > checkpoints[x][1][0]-checkpoints[x][3]/2 and car.rect.centerx < checkpoints[x][1][0]+checkpoints[x][3]/2 and car.rect.centery > checkpoints[x][1][1]-checkpoints[x][4]/2 and car.rect.centery < checkpoints[x][1][1]+checkpoints[x][4]/2:
                            checkpoints[x][2] = True
                
    isBestLap = False
    completedLap = True
    for y in range(length):
        if checkpoints[y][2] == False:
            completedLap = False
    if completedLap == True:
        car.lapsCompleted +=1
        lap_time = round(lap_time,3)

        if car.lapsCompleted == 1:
            isBestLap = True
            bestLapSeconds = lap_time
        elif car.lapsCompleted>1:
            if lap_time < bestLapSeconds:
                isBestLap = True
                bestLapSeconds = lap_time

        minutes = int(lap_time/60)
        seconds = lap_time - (60*minutes)
        if minutes < 10:
            minutes_string = "0"+str(minutes)
        else: 
            minutes_string = str(minutes)
        if seconds < 10:
            seconds_string = "0"+str(seconds)
        else: 
            seconds_string = str(seconds)
        lap_time_string = minutes_string + ":" + seconds_string
        laptimes.append([car.lapsCompleted,lap_time_string])

        if isBestLap == True:
            best_lap = lap_time_string

        lap_time = 0

        length2 = len(laptimes)
        if length2>0:
            for y in range(length2):
                print((laptimes[y][0]),(laptimes[y][1]))
        
        if length2>0:
            previous_lap = laptimes[car.lapsCompleted-1][1]

        

      

        for y in range(length):
            checkpoints[y][2] = False
    


        
    
    


def blitRotate(image, pos, originPos, angle):

    global rotated_image
    global rotated_image_rect
    global rotated_image_center
    global new_rect
    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

TrackPieces = pygame.sprite.Group()
car1 = Car()
car1.rect.topleft = (600,600)

createOvalTrack()

timer = 0
race_countdown = 3
race_time = 0
seconds = 0
minutes = 0
race_length = 10

laptimes = []
raceStarted = False

RACESTART = pygame.USEREVENT + 1
pygame.time.set_timer(RACESTART, 1)


running = True
while running:
    window.fill((200,200,200))

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    if car1.lapsCompleted == race_length:
        raceStarted = False
        countdown_text = font1.render("Race Finished!", True, (0,0,0))
    #    pygame.time.set_timer(RACESTART, 0)


    car1.onTrack = False
    for track in TrackPieces:
        carOnTrack = pygame.sprite.collide_mask(car1,track)
        if carOnTrack:
            car1.onTrack = True
    
        


    # checks if the user has pressed down and/or released the mouse and calls functions accordingly
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
       

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                car1.accelerate = True
                

            if event.key == pygame.K_DOWN:
                car1.reverse = True

            if event.key == pygame.K_LEFT:
                car1.turnleft = True

            if event.key == pygame.K_RIGHT:
                car1.turnright = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                car1.accelerate = False

            if event.key == pygame.K_DOWN:
                car1.reverse = False
            
            if event.key == pygame.K_LEFT:
                car1.turnleft = False
                
            
            if event.key == pygame.K_RIGHT:
                car1.turnright = False
        
        if event.type == RACESTART:
            timer +=1
            if timer == 700:
                timer = 0
                if race_countdown > 0 and raceStarted == False:
                    race_countdown -=1
            if race_countdown == 0:
                raceStarted = True
                race_countdown = -1
            if raceStarted == True:
                seconds+=0.00125
                lap_time +=0.00125
                if seconds >= 60:
                    seconds = 0
                    minutes+=1

    
    if raceStarted == True:
        car1.update()
    TrackPieces.draw(window)
    window.blit(car1.Rotated_image, car1.rect.topleft)

    laps_completed_text = font1.render('Laps completed: '+str(car1.lapsCompleted) +"/"+str(race_length), True, (0,0,0))
    laps_completed_textRect.center = (width *0.45, 20)
    window.blit(laps_completed_text, laps_completed_textRect)
    if race_countdown > 0:
        countdown_text = font1.render(str(race_countdown), True, (0,0,0))
    else:
       if raceStarted == True:
            countdown_text = font1.render("Start!", True, (0,0,0))
    countdown_textRect.center = (width *0.5, 50)
    window.blit(countdown_text, countdown_textRect)
    if minutes<10 and seconds<10:
        race_time_text = font1.render("Race time: 0"+str(minutes)+":0" +str(round(seconds,3)), True, (0,0,0))
    elif minutes<10 and seconds>=10:
        race_time_text = font1.render("Race time: 0"+str(minutes)+":" +str(round(seconds,3)), True, (0,0,0))
    elif minutes>=10 and seconds<10:
        race_time_text = font1.render("Race time: "+str(minutes)+":0" +str(round(seconds,3)), True, (0,0,0))
    else:
        race_time_text = font1.render("Race time: "+str(minutes)+":" +str(round(seconds,3)), True, (0,0,0))

    race_time_textRect.center = (width *0.7, 20)
    window.blit(race_time_text, race_time_textRect)

    previous_lap_text = font1.render("Previous lap: "+ previous_lap, True, (0,0,0))
    previous_lap_textRect.center = (width *0.25, 20)
    window.blit(previous_lap_text, previous_lap_textRect)
    best_lap_text = font1.render("Best lap: "+ best_lap, True, (0,0,0))
    best_lap_textRect.center = (width *0.02, 20)
    window.blit(best_lap_text, best_lap_textRect)
  
    checkpointsCheck(car1, checkpoints)

    pygame.display.update()

    clock.tick(32)


pygame.quit()