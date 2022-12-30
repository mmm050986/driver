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

car = pygame.image.load("car.png").convert()
car = pygame.transform.scale(car,(60,30))
longvertical = pygame.image.load("longvertical.jpg").convert()
longvertical = pygame.transform.scale(longvertical,(100,200))
longhorizontal = pygame.image.load("longhorizontal.jpg").convert()
longhorizontal = pygame.transform.scale(longhorizontal,(200,100))
shortvertical = pygame.image.load("shortvertical.jpg").convert()
shortvertical = pygame.transform.scale(shortvertical,(100,100))
shorthorizontal = pygame.image.load("shorthorizontal.jpg").convert()
shorthorizontal = pygame.transform.scale(shorthorizontal,(100,100))
curveBL = pygame.image.load("curveBL.gif").convert()
curveBL = pygame.transform.scale(curveBL,(150,150))
curveTL = pygame.image.load("curveTL.gif").convert()
curveTL = pygame.transform.scale(curveTL,(150,150))
curveBR = pygame.image.load("curveBR.gif").convert()
curveBR = pygame.transform.scale(curveBR,(150,150))
longcurveBR = pygame.image.load("longlongcurveBR.gif").convert()
longcurveBR = pygame.transform.scale(longcurveBR,(392,288))
longcurveTR = pygame.image.load("longlongcurveTR.gif").convert()
longcurveTR = pygame.transform.scale(longcurveTR,(288,392))
curveTR = pygame.image.load("curveTR.gif").convert()
curveTR = pygame.transform.scale(curveTR,(150,150))
startvertical = pygame.image.load("startvertical.gif").convert()
startvertical = pygame.transform.scale(startvertical,(100,30))
starthorizontal = pygame.image.load("starthorizontal.gif").convert()
starthorizontal = pygame.transform.scale(starthorizontal,(30,100))
tree1 = pygame.image.load("tree1.gif").convert()
tree1 = pygame.transform.scale(tree1,(60,60))
tree2 = pygame.image.load("tree2.gif").convert()
tree2 = pygame.transform.scale(tree2,(60,60))
tree3 = pygame.image.load("tree3.gif").convert()
tree3 = pygame.transform.scale(tree3,(60,60))
tree4 = pygame.image.load("tree3.gif").convert()
tree4 = pygame.transform.scale(tree4,(15,15))

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
speed_text = font1.render('', True, (0,0,0))
speed_textRect = speed_text.get_rect()

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
global treeTopLeft
treeTopLeft = (0,0)
global cantSetTreeHere
cantSetTreeHere = True
global half_second, car_kmh
car_kmh = 0
half_second = 0
global justCollided
justCollided = False
global canReverse, canAccelerate
canReverse = True
canAccelerate = True

class TreeTrunk(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = tree4
        self.image = tree4
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = tree4.get_rect(center=(
                300,
                300,
            ))


class Tree1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = tree1
        self.image = tree1
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = tree1.get_rect(center=(
                300,
                300,
            ))

class Tree2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = tree2
        self.image = tree2
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = tree2.get_rect(center=(
                300,
                300,
            ))

class Tree3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = tree3
        self.image = tree3
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = tree3.get_rect(center=(
                300,
                300,
            ))



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

class ShortVerticalTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = shortvertical
        self.image = shortvertical
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = shortvertical.get_rect(center=(
                300,
                300,
            ))

class ShortHorizontalTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = shorthorizontal
        self.image = shorthorizontal
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = shorthorizontal.get_rect(center=(
                300,
                300,
            ))

class LongCurveBRTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = longcurveBR
        self.image = longcurveBR
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = longcurveBR.get_rect(center=(
                300,
                300,
            ))

class LongCurveTRTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = longcurveTR
        self.image = longcurveTR
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = longcurveTR.get_rect(center=(
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
        self.reversing = False
        

    def update(self):
       
       #Stops the car from moving backwards once it comes to a halt, and starts it moving forwards
        if self.accelerate == True and self.speed == 0:
            self.reversing = False

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

            if self.turnleft == True and self.speed>1:
                self.turnspeed = (28 - self.speed) / 4
                self.direction += self.turnspeed
                if self.direction >=360:
                    self.direction = 0
            if self.turnright == True and self.speed>1:
                self.turnspeed = (28 - self.speed) / 4
                self.direction -= self.turnspeed
                if self.direction <=-360:
                    self.direction = 0
        
        #calculate absolute direction
        absdirection = self.direction
        if absdirection < 0:
            absdirection +=360


        #calculate which quadrant the car is facing
        self.orientation = absdirection // 90

        #change the car's angle to a positive degree from the x axis
        self.angle = absdirection - self.orientation*90
        if self.orientation == 1:
            self.angle -=90
            self.angle *=-1
        if self.orientation == 3:
            self.angle -=90
            self.angle *=-1
        
        #adjust the user's steering direction, so that it doesn't get too far ahead of where the car is actually heading
        if self.angle > self.previousangle:
            if self.angle - self.previousangle > 30:
                self.angle -=20
        if self.angle < self.previousangle:
            if self.previousangle - self.angle > 30:
                self.angle +=20

        #when the user starts to steer, set the angle that the car should be turning in
        if self.chaseminangle == False and self.chasemaxangle == False:
            if self.angle>self.maxangle:
                self.maxangle = self.angle
        #if the user's steering direction is greater than the angle the car is currently facing in
        #then adjust the car's direction 
        if self.maxangle > self.previousangle:
            self.chasemaxangle = True
        #if the user is continuing to steer in the same direction, change the car's desired heading to the new steer direction
        if self.chasemaxangle == True:
            if self.angle>self.maxangle:
                self.maxangle = self.angle
        #if the user's steering direction is a smaller angle than the car's current direction, then set the car to 
        #change heading towards the steering direction
        if self.minangle < self.previousangle:
            self.chaseminangle = True 
        #if the user is continuing to steer in the same direction, change the car's desired heading to the new steer direction
        if self.chaseminangle == True:
            if self.angle < self.minangle:
                self.minangle = self.angle
       
    
        wait = False
        # traction variable is the speed with which the car's direction approaches the user's steering direction
        # if traction value is higher, then the car's traction is higher, so the car changes is direction quicker
        # and approaches the user's steering direction faster
        # set traction to lower value if the car is traveling at a higher speed
        if self.onTrack == True:
            if self.speed<=10:
                traction = 7 - self.speed/5
            elif self.speed <=15:
                traction = 3
            elif self.speed <=20:
                traction = 2.7
            elif self.speed <=30:
                traction = 1.5
        # set traction to lower value if the car is off the track
        if self.onTrack == False:
            traction = 5 - self.speed/4  
        # set traction to lower value if the car is accelerating
        if self.accelerate == True:
            traction -=0.5 

        # adjust the car's direction to approach the user's steering direction
        if self.chaseminangle == True:
            if (self.previousangle - self.minangle) > traction:
                self.previousangle -=traction
        # if the car's direction is close enough to the user's steering direction
        # set the car to approach the new steering direction
            if self.previousangle <=self.minangle+traction:
                self.chaseminangle = False
                self.chasemaxangle = True
                self.maxangle = self.minangle
                self.minangle = 90
                self.currentorientation = self.orientation
                wait = True
        # adjust the car's direction to approach the user's steering direction
        if self.chasemaxangle == True and wait == False:
            if (self.maxangle - self.previousangle) > traction:
                self.previousangle +=traction
        # if the car's direction is close enough to the user's steering direction
        # set the car to approach the new steering direction
            if self.previousangle >=self.maxangle-traction:
                self.chasemaxangle = False
                self.chaseminangle = True
                self.minangle = self.maxangle
                self.maxangle = 0
                self.currentorientation = self.orientation
       
        # check that the car is on the track, and the user is accelerating, and the car is less than its max speed
        if self.accelerate == True and self.reversing == False and self.onTrack == True and self.speed<30:
            # accelerate the car at different rates depending on the current speed of the car
            if self.speed == 0:
                self.speed = 1.5
            if self.speed < 5:
                if self.turnleft == False and self.turnright == False:
                    self.speed +=0.9
                else:
                    self.speed +=0.3
            if self.speed >= 5 and self.speed <10:
                if self.turnleft == False and self.turnright == False:
                    self.speed +=0.6
                else:
                    self.speed +=0.3
            if self.speed >= 10 and self.speed <15:
                if self.turnleft == False and self.turnright == False:
                    self.speed +=0.4
                else:
                    self.speed +=0.2
            if self.speed >= 15 and self.speed <30:
                if self.turnleft == False and self.turnright == False:
                    self.speed +=0.3
                else:
                    self.speed +=0.1

        # adjust the speed of the car if the car is reversing, and the user is accelerating
        if self.accelerate == True and self.reversing == True and self.speed>0:
            self.speed -=0.4
            if self.speed <=1.5:
                self.speed = 0
        # adjust the speed of the car if the car is moving forward and the car is off the track, and the user is accelerating
        # max speed of car when off the track is 8
        if self.accelerate == True and self.reversing == False and self.onTrack == False and self.speed<8:
            if self.speed == 0:
                self.speed = 1
            self.speed +=0.2
        # adjust the speed of the car if the user is not accelerating or reversing
        if self.accelerate == False and self.reverse == False and self.speed>0:
            self.speed -=0.4
            if self.speed <=1.5:
                self.speed = 0
        # adjust the speed of the car if the user is reversing, but the car is still moving forward
        if self.reverse == True and self.reversing == False and self.speed>0:
            self.speed -=0.8
            if self.speed <=1.5:
                self.speed = 0
        # set the car to move backwards if the user is reversing and the car is no longer moving forward
        if self.reverse == True and self.speed==0:
            self.reversing = True
        # adjust the reversing speed of the car - max reversing speed = 8
        if self.reversing == True and self.reverse == True and self.speed<8:
            self.speed +=0.9
         

        # slow the car down if it is off the track and going faster than 8
        if self.onTrack == False and self.speed>8:
            self.speed -=3
        
        # calculate the amount to move car on the x axis and y axis so that it moves in the correct direction
        if self.speed>0:
            self.xspeed = self.speed
            rad_direction = self.previousangle*0.0175
            self.yspeed = math.tan(rad_direction) * self.xspeed
            abspeed = math.sqrt((self.xspeed*self.xspeed) + (self.yspeed*self.yspeed))
            speedadjust = abspeed/self.speed
            self.xspeed = self.xspeed / speedadjust
            self.yspeed = self.yspeed / speedadjust
        
  
            # adjust the directions to move on the x axis and y axis based on the direcion the car is facing
            if self.currentorientation == 0:
                self.yspeed *=-1
            if self.currentorientation == 1:
                self.yspeed *=-1
                self.xspeed *=-1
            if self.currentorientation == 2:
                self.xspeed *=-1
        # don't move the car if the car's speed is zero
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

        
        # change the direction of the car if the car is reversing
        if self.reversing == True:
            self.xspeed *=-1
            self.yspeed *=-1
        
        # move the car
        self.rect.move_ip(self.xspeed, self.yspeed)  

        

# create track number 2
def createTrack2():

    # create a list of the checkpoints on the track that need to be completed for a lap to be successful
    global checkpoints
    checkpoints = []
    # set checkpoint default as not completed
    completed = False

    # create track pieces and set their position. add them to the track pieces group. If the track piece is a checkpoint that needs to be completed
    # then add the position of the trackpiece to the checkpoints list
    track = LongHorizontalTrack()
    track.rect.topleft = (580,750)
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (780,750)
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (980,750)
    TrackPieces.add(track)

    track = LongCurveBRTrack()
    track.rect.topleft = (1180,562)
    TrackPieces.add(track)

    track = ShortVerticalTrack()
    track.rect.topleft = (1472,462)
    # add checkpoint: (checkpoint number, position of trackpiece center, bool ischeckpointcompleted, width and height of track piece)
    checkpoints.append([1, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = LongCurveTRTrack()
    track.rect.topleft = (1284,70)
    TrackPieces.add(track)

    track = ShortHorizontalTrack()
    track.rect.topleft = (1184,70)
    checkpoints.append([2, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = CurveTLTrack()
    track.rect.topleft = (1034,70)
    TrackPieces.add(track)

    track = LongVerticalTrack()
    track.rect.topleft = (1034,220)
    checkpoints.append([3, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = ShortVerticalTrack()
    track.rect.topleft = (1034,420)
    TrackPieces.add(track)

    track = CurveBRTrack()
    track.rect.topleft = (984,520)
    checkpoints.append([4, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = CurveBLTrack()
    track.rect.topleft = (834,520)
    TrackPieces.add(track)

    track = ShortVerticalTrack()
    track.rect.topleft = (834,420)
    TrackPieces.add(track)

    track = LongVerticalTrack()
    track.rect.topleft = (834,220)
    checkpoints.append([5, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = CurveTRTrack()
    track.rect.topleft = (784,70)
    checkpoints.append([6, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = CurveTLTrack()
    track.rect.topleft = (634,70)
    TrackPieces.add(track)

    track = CurveBRTrack()
    track.rect.topleft = (584,220)
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (384,270)
    TrackPieces.add(track)

    track = ShortHorizontalTrack()
    track.rect.topleft = (284,270)
    checkpoints.append([7, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = CurveTLTrack()
    track.rect.topleft = (134,270)
    TrackPieces.add(track)

    track = LongVerticalTrack()
    track.rect.topleft = (134,420)
    checkpoints.append([8, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = ShortVerticalTrack()
    track.rect.topleft = (134,620)
    TrackPieces.add(track)

    track = CurveBLTrack()
    track.rect.topleft = (134,700)
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (284,750)
    TrackPieces.add(track)

    track = ShortHorizontalTrack()
    track.rect.topleft = (484,750)
    TrackPieces.add(track)

    track = StartHorizontalTrack()
    track.rect.topleft = (550,750)
    checkpoints.append([9, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

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

# function to detect collision with trees  
def treeCollisionCheck(car, Treetrunks):
    global justCollided
    global canReverse, canAccelerate

    # for loop checks each tree for collision
    for treetrunk in Treetrunks:
        collided = pygame.sprite.collide_mask(car,treetrunk)
        if collided:
            #check whether the car can go forward or backward based on its relative position to the tree it has collided with
            if car.orientation == 0:
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery>treetrunk.rect.centery-20: 
                  
                    canReverse = True
                    canAccelerate = False
                
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery<=treetrunk.rect.centery-20: 
                  
                    canReverse = False
                    canAccelerate = True
            
                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery<treetrunk.rect.centery+20:
                 
                    canReverse = False
                    canAccelerate = True

                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery>=treetrunk.rect.centery+20:
               
                    canReverse = True
                    canAccelerate = False

            if car.orientation == 3:
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery<treetrunk.rect.centery+20: 
                
                    canReverse = True
                    canAccelerate = False
                
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery>=treetrunk.rect.centery+20: 
                   
                    canReverse = False
                    canAccelerate = True
            
                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery>treetrunk.rect.centery-20:
                    
                    canReverse = False
                    canAccelerate = True

                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery<=treetrunk.rect.centery-20:
                    
                    canReverse = True
                    canAccelerate = False
            
            if car.orientation == 1:
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery<treetrunk.rect.centery+20: 
                  
                    canReverse = False
                    canAccelerate = True
                
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery>=treetrunk.rect.centery+20: 
                  
                    canReverse = True
                    canAccelerate = False
            
                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery>treetrunk.rect.centery-20:
                 
                    canReverse = True
                    canAccelerate = False

                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery<=treetrunk.rect.centery-20:
               
                    canReverse = False
                    canAccelerate = True

            if car.orientation == 2:
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery>treetrunk.rect.centery-20: 
                
                    canReverse = False
                    canAccelerate = True
                
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery<=treetrunk.rect.centery-20: 
                   
                    canReverse = True
                    canAccelerate = False
            
                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery<treetrunk.rect.centery+20:
                    
                    canReverse = True
                    canAccelerate = False

                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery>=treetrunk.rect.centery+20:
                    
                    canReverse = False
                    canAccelerate = True
           
            

            #if the car has just collided with a tree, change car to opposite direction and slow down the car
            if justCollided == False:
                car.speed = car.speed *0.3
                if car.speed == 0:
                    car.speed = 1.5
                if car.reversing == True:
                    car.reversing = False
            
                else:
                    car.reversing = True
                    car.accelerate = False
                # set justCollided to true and set timer to wait for half a second before continuing to check for future collisions
                justCollided = True
                pygame.time.set_timer(COLLISION, 500)
           
                   

    
# function to check if the car is completing the necessary checkpoints in order to have a successfully completed lap
# function also records successful lap times and best lap times
# function is given the car object and the checkpoints list for the track
def checkpointsCheck (car, checkpoints):
    global lap_time
    global best_lap
    global previous_lap, best_lap, bestLapSeconds
    global race_length
    length = len(checkpoints)

    # for loop runs through the checkpoints in the checkpoints list
    for i in range(length):
        canComplete = True
        # for loop starts with the checkpoint that has the highest checkpoint number in the list (i.e. the final checkpoint) and works backwards to the first checkpoint
        for x in range(length):
            if checkpoints[x][0] == length-i:
                # assumes that the checkpoints before the current checkpoint have been completed
                canComplete = True
                # finds checkpoints that have a lower checkpoint number than the current checkpoint, and checks if they have all been completed or not
                # if one of the checkpoints with a lower checkpoint has not been completed, then the current checkpoint can not be completed
                # if all checkpoints with a lower checkpoint number have already been completed, then canComplete remains True
                for j in range(length):
                    if checkpoints[j][0]< length-i:
                        if checkpoints[j][2] == False:
                            canComplete = False

                # If the current checkpoint can be completed, then check if the car's position is within the bounds of the checkpoint to be completed
                if canComplete == True:
                    # check that the checkpoint is not the final checkpoint (i.e. the finish line)
                    if checkpoints[x][0]<length:
                        # for all checkpoints that are not the finish line, the car only needs to get close enough to the checkpoint (within a 75 pixel boundary), to complete the checkpoint
                        if car.rect.centerx > checkpoints[x][1][0]-75 and car.rect.centerx < checkpoints[x][1][0]+75 and car.rect.centery > checkpoints[x][1][1]-75 and car.rect.centery < checkpoints[x][1][1]+75:
                            checkpoints[x][2] = True
                    else:
                        # if the checkpoint is the final checkpoint (i.e. the finish line) then the car must intersect with the track piece in order to complete the final checkpoint
                        if car.rect.centerx > checkpoints[x][1][0]-checkpoints[x][3]/2 and car.rect.centerx < checkpoints[x][1][0]+checkpoints[x][3]/2 and car.rect.centery > checkpoints[x][1][1]-checkpoints[x][4]/2 and car.rect.centery < checkpoints[x][1][1]+checkpoints[x][4]/2:
                            checkpoints[x][2] = True
                
    isBestLap = False
    completedLap = True

    # checks if any of the checkpoints are not completed - if any are not completed then the car has not completed the lap
    for y in range(length):
        if checkpoints[y][2] == False:
            completedLap = False

    # if all checkpoints are completed then a new lap has been completed
    if completedLap == True:
        # add 1 to number of laps completed and round the lap time to 3 decimal places
        car.lapsCompleted +=1
        lap_time = round(lap_time,3)
        # check if this current lap time is lower than previous best lap time - if so, then set it as the new best lap time
        if car.lapsCompleted == 1:
            isBestLap = True
            bestLapSeconds = lap_time
        elif car.lapsCompleted>1:
            if lap_time < bestLapSeconds:
                isBestLap = True
                bestLapSeconds = lap_time

        # convert the lap time into minutes and seconds and add to the list of laptimes as a string, along with the lap number
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

        # set String best lap 
        if isBestLap == True:
            best_lap = lap_time_string
        # reset the lap time
        lap_time = 0

        # print out lap times in terminal after race ends

        length2 = len(laptimes)
        if length2==race_length:
            for y in range(length2):
                print((laptimes[y][0]),(laptimes[y][1]))
        
        # if there is more than one recorded lap time, then set the previous lap time as the previous lap time in the list of lap times
        if length2>0:
            previous_lap = laptimes[car.lapsCompleted-1][1]

        # if a lap has just been completed, then reset all the checkpoints to not completed
        for y in range(length):
            checkpoints[y][2] = False

# function to set the tree position
def setTreePosition(newtree):
    global treeTopLeft
    global cantSetTreeHere
    cantSetTreeHere = False

    #ranomly select a coordinate on the screen
    randx = random.randint(-60,width)
    randy = random.randint(-60,height)
    newtree.rect.topleft = (randx,randy)

    #check if the tree position intersects with a track piece
    for track in TrackPieces:
        collided = pygame.sprite.collide_mask(newtree,track)
        if collided:
            cantSetTreeHere = True
    
    #if the tree position did not intersect with a track piece, then check if it intersects with any of the trees in the tree Group
    if cantSetTreeHere == False and len(Trees) > 0:
        for tree in Trees:
            collided = pygame.sprite.collide_mask(newtree,tree)
            if collided:
                cantSetTreeHere = True

    # if the tree position intersected with either a track piece or another tree, call the setTreePosition function again to 
    # set a new tree position until the position does not intersect with a track piece or another tree
    if cantSetTreeHere == True:
        setTreePosition(newtree)

# function to place a number of trees around the track
def setTrees(number):     
    global treeTopLeft
    global cantSetTreeHere
    
    # for loop to place the number of trees that has been passed to the function
    for x in range(number):
        # select a random tree type (1-3)
        treetype = random.randint(1,3)
        # create a new tree of randomly selected type, then pass that tree object to setTreePosition function, to set it's position
        # after the setTreePosition has successfully set the tree position, then add the tree to the list of trees
        # finally, create a tree trunk object, which is positioned in the center of the tree object, which will be used for car collisions
        # add tree trunk to list of tree trunks
        if treetype == 1:
            newtree = Tree1()
            setTreePosition(newtree)
            if cantSetTreeHere == False:
                Trees.add(newtree)
                treetrunk = TreeTrunk()
                treetrunk.rect.center = newtree.rect.center
                Treetrunks.add(treetrunk)
        if treetype == 2:
            newtree = Tree2()
            setTreePosition(newtree)
            if cantSetTreeHere == False:
                Trees.add(newtree)
                treetrunk = TreeTrunk()
                treetrunk.rect.center = newtree.rect.center
                Treetrunks.add(treetrunk)
        if treetype == 3:
            newtree = Tree3()
            setTreePosition(newtree)
            if cantSetTreeHere == False:
                Trees.add(newtree)
                treetrunk = TreeTrunk()
                treetrunk.rect.center = newtree.rect.center
                Treetrunks.add(treetrunk)
            

# function to rotate image
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
Trees = pygame.sprite.Group()
Treetrunks = pygame.sprite.Group()
car1 = Car()

# here i can select a different track to be drawn on the screen, and set the car position accordingly. I will create more tracks and then allow the 
# user to select which track they want to play at the beginning of the game

#car1.rect.topleft = (600,600)
#createOvalTrack()
car1.rect.topleft = (500,800)
createTrack2()

# create a number of trees to be displayed on the screen
setTrees(150)


timer = 0
race_countdown = 3
race_time = 0
seconds = 0
minutes = 0
race_length = 10

laptimes = []
raceStarted = False

# set the timer to record lap times and race time
RACESTART = pygame.USEREVENT + 1
pygame.time.set_timer(RACESTART, 1)
COLLISION = pygame.USEREVENT +2


running = True
while running:
    window.fill((200,200,200))

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # check if the car has collided with a tree (this function needs some work)
    treeCollisionCheck(car1, Treetrunks)

    # check if the user has completed the required number of laps. If so, then stop the race
    if car1.lapsCompleted == race_length:
        raceStarted = False
        countdown_text = font1.render("Race Finished!", True, (0,0,0))
    #    pygame.time.set_timer(RACESTART, 0)


    # check if the car is currently on the track
    car1.onTrack = False
    for track in TrackPieces:
        carOnTrack = pygame.sprite.collide_mask(car1,track)
        if carOnTrack:
            car1.onTrack = True
    
        

    # checks if the user has pressed down and/or released the mouse and calls functions accordingly
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
       
        # check which directional keys the user is pressing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and justCollided == False:
                car1.accelerate = True

            if event.key == pygame.K_UP and justCollided == True  and canAccelerate == True:
                car1.accelerate = True
                
            if event.key == pygame.K_DOWN and justCollided == False:
                car1.reverse = True
            
            if event.key == pygame.K_DOWN and justCollided == True and canReverse == True:
                car1.reverse = True

            if event.key == pygame.K_LEFT and justCollided == False:
                car1.turnleft = True

            if event.key == pygame.K_RIGHT and justCollided == False:
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
        
        # start the 3 second countdown to the beginning of the race
        if event.type == RACESTART:
            timer +=1
            if timer == 700:
                timer = 0
                if race_countdown > 0 and raceStarted == False:
                    race_countdown -=1
            if race_countdown == 0:
                raceStarted = True
                race_countdown = -1
            # start the race timer when the race starts
            if raceStarted == True:
                seconds+=0.00125
                half_second +=0.00125
                # update the car's (virtual) speed every tenth of a second
                if half_second >=0.1:
                    half_second = 0
                    car_kmh = int(car1.speed*5)
                lap_time +=0.00125
                if seconds >= 60:
                    seconds = 0
                    minutes+=1

        if event.type == COLLISION:
            justCollided = False
            pygame.time.set_timer(COLLISION, 0)


    # allow the car to move once the race has started
    if raceStarted == True:
        car1.update()

    # draw track pieces, car, and trees on the display (don't draw tree trunks)
    TrackPieces.draw(window)
    window.blit(car1.Rotated_image, car1.rect.topleft)
    Trees.draw(window)


    # edit text values and display at the top of the screen (might create a bar at the top of the screen for displaying this info so it doesn't intersect with images)
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
    speed_text = font1.render("Speed (km/h): "+ str(car_kmh), True, (0,0,0))
    speed_textRect.center = (width *0.85, 20)
    window.blit(speed_text, speed_textRect)
  
    # check if the car has completed any checkpoints or completed a lap
    checkpointsCheck(car1, checkpoints)

    pygame.display.update()

    clock.tick(32)


pygame.quit()