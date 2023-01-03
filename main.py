from multiprocessing.connection import answer_challenge
import pygame
import random
from car import *

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


longvertical = pygame.image.load("longvertical.jpg").convert()
longvertical = pygame.transform.scale(longvertical,(100,200))
longhorizontal = pygame.image.load("longhorizontal.jpg").convert()
longhorizontal = pygame.transform.scale(longhorizontal,(200,100))
rtlongvertical = pygame.image.load("rtracklongvertical.gif").convert()
rtlongvertical = pygame.transform.scale(rtlongvertical,(100,200))
rtlonghorizontal = pygame.image.load("rtracklonghorizontal.gif").convert()
rtlonghorizontal = pygame.transform.scale(rtlonghorizontal,(200,100))
bridgehorizontal = pygame.image.load("bridgehorizontal.gif").convert()
bridgehorizontal = pygame.transform.scale(bridgehorizontal,(400,110))
shortvertical = pygame.image.load("shortvertical.jpg").convert()
shortvertical = pygame.transform.scale(shortvertical,(100,100))
shorthorizontal = pygame.image.load("shorthorizontal.jpg").convert()
shorthorizontal = pygame.transform.scale(shorthorizontal,(100,100))
rtshortvertical = pygame.image.load("rtrackshortvertical.gif").convert()
rtshortvertical = pygame.transform.scale(rtshortvertical,(100,100))
rtshorthorizontal = pygame.image.load("rtrackshorthorizontal.gif").convert()
rtshorthorizontal = pygame.transform.scale(rtshorthorizontal,(100,100))
curveBL = pygame.image.load("curveBL.gif").convert()
curveBL = pygame.transform.scale(curveBL,(150,150))
curveTL = pygame.image.load("curveTL.gif").convert()
curveTL = pygame.transform.scale(curveTL,(150,150))
curveBR = pygame.image.load("curveBR.gif").convert()
curveBR = pygame.transform.scale(curveBR,(150,150))
rtcurveBL = pygame.image.load("rtrackcurveBL.gif").convert()
rtcurveBL = pygame.transform.scale(rtcurveBL,(150,150))
rtcurveTL = pygame.image.load("rtrackcurveTL.gif").convert()
rtcurveTL = pygame.transform.scale(rtcurveTL,(150,150))
rtcurveBR = pygame.image.load("rtrackcurveBR.gif").convert()
rtcurveBR = pygame.transform.scale(rtcurveBR,(150,150))
rtcurveTR = pygame.image.load("rtrackcurveTR.gif").convert()
rtcurveTR = pygame.transform.scale(rtcurveTR,(150,150))
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
tree4 = pygame.transform.scale(tree4,(10,10))
background = pygame.image.load("grass.gif").convert()
background = pygame.transform.scale(background,(width,height))
trackimage = pygame.image.load("trackimage2.gif").convert()
trackimage = pygame.transform.scale(trackimage,(300,180))
trackimage_rect = trackimage.get_rect()
trackimage2 = pygame.image.load("trackimage.gif").convert()
trackimage2 = pygame.transform.scale(trackimage2,(300,180))
trackimage2_rect = trackimage2.get_rect()
trackimage3 = pygame.image.load("trackimage3.gif").convert()
trackimage3 = pygame.transform.scale(trackimage3,(300,180))
trackimage3_rect = trackimage3.get_rect()

font1 = pygame.font.Font(None, 32)
font2 = pygame.font.Font(None, 64)

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
choose_track_text = font2.render('Choose Track', True, (0,0,0))
choose_track_textRect = choose_track_text.get_rect()
loading_text = font1.render('Loading...', True, (0,0,0))
loading_textRect = loading_text.get_rect()

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
global game_stage
game_stage = "main menu"
global createdTrack
createdTrack = False
global selectedTrack
selectedTrack = 0
global drawBridge
drawBridge = True
global timePenalty
timePenalty = False


global collisionnumber
collisionnumber = 0

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

class RShortVerticalTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = rtshortvertical
        self.image = rtshortvertical
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = rtshortvertical.get_rect(center=(
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

class RShortHorizontalTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = rtshorthorizontal
        self.image = rtshorthorizontal
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = rtshorthorizontal.get_rect(center=(
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
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = longvertical.get_rect(center=(
                300,
                300,
            ))


class RLongVerticalTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = rtlongvertical
        self.image = rtlongvertical
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = rtlongvertical.get_rect(center=(
                300,
                300,
            ))

class LongHorizontalTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = longhorizontal
        self.image = longhorizontal
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = longhorizontal.get_rect(center=(
                300,
                300,
            ))

class RLongHorizontalTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = rtlonghorizontal
        self.image = rtlonghorizontal
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = rtlonghorizontal.get_rect(center=(
                300,
                300,
            ))

class BridgeHorizontalTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = bridgehorizontal
        self.image = bridgehorizontal
      
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = bridgehorizontal.get_rect(center=(
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

class RCurveBLTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = rtcurveBL
        self.image = rtcurveBL
        
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = rtcurveBL.get_rect(center=(
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

class RCurveTRTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = rtcurveTR
        self.image = rtcurveTR
        
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = rtcurveTR.get_rect(center=(
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

class RCurveBRTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = rtcurveBR
        self.image = rtcurveBR
        
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = rtcurveBR.get_rect(center=(
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

class RCurveTLTrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = rtcurveTL
        self.image = rtcurveTL
        
        self.image.set_colorkey((0, 0,0), RLEACCEL)
        self.rect = rtcurveTL.get_rect(center=(
                300,
                300,
            ))




# create track number 2
def createTrack3():

    # create a list of the checkpoints on the track that need to be completed for a lap to be successful
    global checkpoints, createdTrack, bridge
    checkpoints = []
    # set checkpoint default as not completed
    completed = False

    track = RShortVerticalTrack()
    track.rect.topleft = (40,200)
    TrackPieces.add(track)
    track = ShortVerticalTrack()
    track.rect.topleft = (40,200)
    RTrackPieces.add(track)

    track = RLongVerticalTrack()
    track.rect.topleft = (40,310)
    TrackPieces.add(track)
    track = LongVerticalTrack()
    track.rect.topleft = (40,310)
    RTrackPieces.add(track)

    track = RLongVerticalTrack()
    track.rect.topleft = (40,520)
    TrackPieces.add(track)
    track = LongVerticalTrack()
    track.rect.topleft = (40,520)
    RTrackPieces.add(track)


    track = RCurveBLTrack()
    track.rect.topleft = (40,730)
    checkpoints.append([14, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)
    track = CurveBLTrack()
    track.rect.topleft = (40,730)
    RTrackPieces.add(track)

    track = RLongHorizontalTrack()
    track.rect.topleft = (190,780)
    TrackPieces.add(track)
    track = LongHorizontalTrack()
    track.rect.topleft = (190,780)
    RTrackPieces.add(track)

    track = RLongHorizontalTrack()
    track.rect.topleft = (395,780)
    TrackPieces.add(track)
    track = LongHorizontalTrack()
    track.rect.topleft = (395,780)
    RTrackPieces.add(track)

    track = RCurveBRTrack()
    track.rect.topleft = (600,730)
    checkpoints.append([13, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)
    track = CurveBRTrack()
    track.rect.topleft = (600,730)
    RTrackPieces.add(track)

    track = LongVerticalTrack()
    track.rect.topleft = (650,530)
    TrackPieces.add(track)

    track = LongVerticalTrack()
    track.rect.topleft = (650,330)
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (1000,380)
    TrackPieces.add(track)

    track = RLongHorizontalTrack()
    track.rect.topleft = (1200,380)
    TrackPieces.add(track)
    track = LongHorizontalTrack()
    track.rect.topleft = (1200,380)
    RTrackPieces.add(track)

    track = RCurveTRTrack()
    track.rect.topleft = (1400,380)
    checkpoints.append([8, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)
    track = CurveTRTrack()
    track.rect.topleft = (1400,380)
    RTrackPieces.add(track)

    track = RLongVerticalTrack()
    track.rect.topleft = (1450,530)
    TrackPieces.add(track)
    track = LongVerticalTrack()
    track.rect.topleft = (1450,530)
    RTrackPieces.add(track)

    track = RCurveBRTrack()
    track.rect.topleft = (1400,730)
    TrackPieces.add(track)
    track = CurveBRTrack()
    track.rect.topleft = (1400,730)
    checkpoints.append([7, track.rect.center, completed, track.rect.width, track.rect.height])
    RTrackPieces.add(track)

    track = RLongHorizontalTrack()
    track.rect.topleft = (1195,780)
    TrackPieces.add(track)
    track = LongHorizontalTrack()
    track.rect.topleft = (1195,780)
    RTrackPieces.add(track)

    track = RLongHorizontalTrack()
    track.rect.topleft = (990,780)
    TrackPieces.add(track)
    track = LongHorizontalTrack()
    track.rect.topleft = (990,780)
    RTrackPieces.add(track)

    track = RCurveBLTrack()
    track.rect.topleft = (838,730)
    checkpoints.append([6, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)
    track = CurveBLTrack()
    track.rect.topleft = (838,730)
    RTrackPieces.add(track)

    track = LongVerticalTrack()
    track.rect.topleft = (838,530)
    checkpoints.append([5, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = LongVerticalTrack()
    track.rect.topleft = (838,400)
    TrackPieces.add(track)



    track = CurveTLTrack()
    track.rect.topleft = (838,250)
    checkpoints.append([4, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (988,250)
    checkpoints.append([3, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = CurveBRTrack()
    track.rect.topleft = (1188,200)
    TrackPieces.add(track)

    track = CurveTRTrack()
    track.rect.topleft = (1188,50)
    checkpoints.append([2, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (988,50)
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (788,50)
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (588,50)
    checkpoints.append([1, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (388,50)
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (188,50)
    TrackPieces.add(track)

    track = CurveTLTrack()
    track.rect.topleft = (40,50)
    checkpoints.append([15, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)


    bridge = BridgeHorizontalTrack()
    bridge.rect.topleft = (600,375)
    checkpoints.append([9, bridge.rect.center, completed, bridge.rect.width, bridge.rect.height])
    TrackPieces.add(bridge)
    Bridge.add(bridge)

    bridgestructure = LongHorizontalTrack()
    bridgestructure.image = pygame.transform.scale(longhorizontal,(60,10))
    bridgestructure.rect.topleft = (600,375)
    BridgeStructure.add(bridgestructure)
    bridgestructure = LongHorizontalTrack()
    bridgestructure.image = pygame.transform.scale(longhorizontal,(60,10))
    bridgestructure.rect.topleft = (600,475)
    BridgeStructure.add(bridgestructure)
    bridgestructure = LongHorizontalTrack()
    bridgestructure.image = pygame.transform.scale(longhorizontal,(70,10))
    bridgestructure.rect.topleft = (765,375)
    BridgeStructure.add(bridgestructure)
    bridgestructure = LongHorizontalTrack()
    bridgestructure.image = pygame.transform.scale(longhorizontal,(70,10))
    bridgestructure.rect.topleft = (765,475)
    BridgeStructure.add(bridgestructure)
    bridgestructure = LongHorizontalTrack()
    bridgestructure.image = pygame.transform.scale(longhorizontal,(60,10))
    bridgestructure.rect.topleft = (940,375)
    BridgeStructure.add(bridgestructure)
    bridgestructure = LongHorizontalTrack()
    bridgestructure.image = pygame.transform.scale(longhorizontal,(60,10))
    bridgestructure.rect.topleft = (940,475)
    BridgeStructure.add(bridgestructure)
    
    bridgestructure = LongHorizontalTrack()
    bridgestructure.image = pygame.transform.scale(longhorizontal,(56,110))
    bridgestructure.rect.width = 56
    bridgestructure.rect.height = 110
    bridgestructure.image = pygame.Surface([56, 110])
    pygame.draw.rect(bridgestructure.image,(45,45,45),pygame.Rect(0,0, 56, 110))
    bridgestructure.rect.topleft = (600,375)
    BridgeWalls.add(bridgestructure)
    
    bridgestructure = LongHorizontalTrack()
    bridgestructure.image = pygame.transform.scale(longhorizontal,(70,110))
    bridgestructure.rect.width = 70
    bridgestructure.rect.height = 110
    bridgestructure.image = pygame.Surface([70, 110])
    pygame.draw.rect(bridgestructure.image,(45,45,45),pygame.Rect(0,0, 70, 110))
    bridgestructure.rect.topleft = (761,375)
    BridgeWalls.add(bridgestructure)

    bridgestructure = LongHorizontalTrack()
    bridgestructure.image = pygame.transform.scale(longhorizontal,(56,110))
    bridgestructure.rect.width = 56
    bridgestructure.rect.height = 110
    bridgestructure.image = pygame.Surface([56, 110])
    pygame.draw.rect(bridgestructure.image,(45,45,45),pygame.Rect(0,0, 56, 110))
    bridgestructure.rect.topleft = (942,375)
    BridgeWalls.add(bridgestructure)

    bridgestructure = LongHorizontalTrack()
    bridgestructure.image = pygame.transform.scale(longhorizontal,(398,5))
    bridgestructure.rect.width = 398
    bridgestructure.rect.height = 5
    bridgestructure.image = pygame.Surface([398, 5])
    pygame.draw.rect(bridgestructure.image,(0,0,100),pygame.Rect(0,0, 398, 5))
    bridgestructure.rect.topleft = (600,380)
    BridgeBarriers.add(bridgestructure)

    bridgestructure = LongHorizontalTrack()
    bridgestructure.image = pygame.transform.scale(longhorizontal,(398,5))
    bridgestructure.rect.width = 398
    bridgestructure.rect.height = 5
    bridgestructure.image = pygame.Surface([398, 5])
    pygame.draw.rect(bridgestructure.image,(0,0,100),pygame.Rect(0,0, 398, 5))
    bridgestructure.rect.topleft = (600,475)
    BridgeBarriers.add(bridgestructure)


    track = LongHorizontalTrack()
    track.rect.topleft = (400,380)
    TrackPieces.add(track)

    track = CurveBLTrack()
    track.rect.topleft = (250,330)
    checkpoints.append([10, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = CurveTLTrack()
    track.rect.topleft = (250,180)
    checkpoints.append([11, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = LongHorizontalTrack()
    track.rect.topleft = (400,180)
    TrackPieces.add(track)

    track = CurveTRTrack()
    track.rect.topleft = (600,180)
    checkpoints.append([12, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)

    track = StartHorizontalTrack()
    track.rect.topleft = (350,50)
    checkpoints.append([16, track.rect.center, completed, track.rect.width, track.rect.height])
    TrackPieces.add(track)



# create track number 2
def createTrack2():

    # create a list of the checkpoints on the track that need to be completed for a lap to be successful
    global checkpoints, createdTrack
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

    createdTrack = True

def createOvalTrack():

    global checkpoints, createdTrack
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

    createdTrack = True

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
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery>treetrunk.rect.centery-10: 
                  
                    canReverse = True
                    canAccelerate = False
                
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery<=treetrunk.rect.centery-10: 
                  
                    canReverse = False
                    canAccelerate = True
            
                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery<treetrunk.rect.centery+10:
                 
                    canReverse = False
                    canAccelerate = True

                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery>=treetrunk.rect.centery+10:
               
                    canReverse = True
                    canAccelerate = False

            if car.orientation == 3:
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery<treetrunk.rect.centery+10: 
                
                    canReverse = True
                    canAccelerate = False
                
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery>=treetrunk.rect.centery+10: 
                   
                    canReverse = False
                    canAccelerate = True
            
                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery>treetrunk.rect.centery-10:
                    
                    canReverse = False
                    canAccelerate = True

                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery<=treetrunk.rect.centery-10:
                    
                    canReverse = True
                    canAccelerate = False
                    if car.previousangle<20:
                        canReverse = False
                        canAccelerate = True
            
            if car.orientation == 1:
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery<treetrunk.rect.centery+10: 
                  
                    canReverse = False
                    canAccelerate = True
                
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery>=treetrunk.rect.centery+10: 
                  
                    canReverse = True
                    canAccelerate = False
            
                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery>treetrunk.rect.centery-10:
                 
                    canReverse = True
                    canAccelerate = False

                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery<=treetrunk.rect.centery-10:
               
                    canReverse = False
                    canAccelerate = True

            if car.orientation == 2:
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery>treetrunk.rect.centery-10: 
                
                    canReverse = False
                    canAccelerate = True
                
                if car.rect.centerx<treetrunk.rect.centerx and car.rect.centery<=treetrunk.rect.centery-10: 
                   
                    canReverse = True
                    canAccelerate = False
                    if car.previousangle<20:
                        canReverse = False
                        canAccelerate = True
            
                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery<treetrunk.rect.centery+10:
                    
                    canReverse = True
                    canAccelerate = False

                if car.rect.centerx>treetrunk.rect.centerx and car.rect.centery>=treetrunk.rect.centery+10:
                    
                    canReverse = False
                    canAccelerate = True
           
            
            

            #if the car has just collided with a tree, change car to opposite direction and slow down the car
            if justCollided == False:
                car.speed = car.speed *0.4
                if car.speed < 1.5:
                    car.speed = 1.5
                if car.reversing == True:
                    car.reversing = False
                    car.reverse = False
                    
            
                else:
                    car.reversing = True
                    car.accelerate = False
                # set justCollided to true and set timer to wait for half a second before continuing to check for future collisions
                justCollided = True
                pygame.time.set_timer(COLLISION, 400)
            
            # if the car somehow gets stuck in between two trees, let the car move forward!
            if canReverse == False and canAccelerate == False:
                canAccelerate = True


def bridgeBarriersCollisionCheck(car, BridgeBarriers):
    global justCollided, drawBridge
    global canReverse, canAccelerate, collisionnumber

    
    for bridgestructure in BridgeBarriers:
        collided = pygame.sprite.collide_mask(car,bridgestructure)
        if collided:

            collidepoint = collided



            if car.rect.centerx<bridgestructure.rect.left:
                car.rect.centerx -=  car.xspeed

                if car.xspeed <= 1:
                    car.rect.centerx -= (car.rect.width - collidepoint[0])

            if car.rect.centerx>bridgestructure.rect.right:
                car.rect.centerx -=  car.xspeed
    
                if car.xspeed <= 1:
                    car.rect.centerx += collidepoint[0]+1

            if car.rect.centery<bridgestructure.rect.centery-5 and car.rect.centerx<bridgestructure.rect.right+car.rect.width/2 and car.rect.centerx>bridgestructure.rect.left-car.rect.width/2:
                car.rect.centery -= car.yspeed
                if car.yspeed <= 1:
                    car.rect.centery -= (car.rect.height - collidepoint[1])

            if car.rect.centery>bridgestructure.rect.centery+5 and car.rect.centerx<bridgestructure.rect.right+car.rect.width/2 and car.rect.centerx>bridgestructure.rect.left-car.rect.width/2:
                car.rect.centery -= car.yspeed
                if car.yspeed <= 1:
                    car.rect.centery += collidepoint[1]+1

            if justCollided == True:
                car.speed *=0.5
            #check whether the car can go forward or backward based on its relative position to the tree it has collided with
                if car.onBridge == False or car.onBridge == True:
                    if car.orientation == 0:
                    
                        if car.rect.centery>bridgestructure.rect.bottom:
                       
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
                        
                    
                        if car.rect.centery<bridgestructure.rect.top:
                    
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True

                        if car.rect.centerx>bridgestructure.rect.right:
                       
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True
                        
                    
                        if car.rect.centerx<bridgestructure.rect.left:
                    
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
                
                    if car.orientation == 3:
                    
                        if car.rect.centery>bridgestructure.rect.bottom:
                       
                        
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True
                        
                    
                        if car.rect.centery<bridgestructure.rect.top:
                    
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
            
                        if car.rect.centerx>bridgestructure.rect.right:
                       
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True
                    
                        if car.rect.centerx<bridgestructure.rect.left:
                    
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False

                    if car.orientation == 1:
                    
            
                        if car.rect.centery>bridgestructure.rect.bottom:
                       
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
                        
                    
                        if car.rect.centery<bridgestructure.rect.top:
                    
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True

                        if car.rect.centerx>bridgestructure.rect.left:
                       
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
                    
                        if car.rect.centerx<bridgestructure.rect.left:
                    
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True
                
                    if car.orientation == 2:
                    
                        if car.rect.centery>bridgestructure.rect.bottom:
                       
                        
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True
                        
                    
                        if car.rect.centery<bridgestructure.rect.top:
                    
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
            
                        if car.rect.centerx>bridgestructure.rect.left:
                        
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
                    
                        if car.rect.centerx<bridgestructure.rect.left:
                    
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True
            
            if canAccelerate == False and canReverse == False:
                canAccelerate = True

           

            if justCollided == False and car.previousangle <=30 and car.onBridge == True:
          
                car.speed = car.speed *0.7
                car.angle = 1
                car.previousangle = 1
                if car.orientation == 0:
                    car.direction =  1
                    car.rect.centerx+=2
                if car.orientation == 1:
                    car.direction =  179
                    car.rect.centerx+=2
                if car.orientation == 2:
                    car.direction =  181
                    car.rect.centerx-=2
                if car.orientation == 3:
                    car.direction =  359
                    car.rect.centerx-=2


                # set justCollided to true and set timer to wait for half a second before continuing to check for future collisions
                justCollided = True
                pygame.time.set_timer(COLLISION, 200)
            
            if justCollided == False:
                justCollided = True
                pygame.time.set_timer(COLLISION, 200)


def bridgeWallsCollisionCheck(car, BridgeWalls):
    global justCollided, drawBridge
    global canReverse, canAccelerate, collisionnumber

    
    for bridgestructure in BridgeWalls:
        collided = pygame.sprite.collide_mask(car,bridgestructure)
        if collided:
            
            collidepoint = collided


            if car.onBridge == False:
                if car.rect.centery<485 and car.rect.centery>375:
                    if car.speed < 10:
                        drawBridge=False

            if car.rect.centerx<bridgestructure.rect.centerx and car.rect.centery<bridgestructure.rect.bottom and car.rect.centery>bridgestructure.rect.top:
                car.rect.centerx -=  car.xspeed
               
                if car.speed == 0:
                    car.rect.centerx -= (car.rect.width - collidepoint[0])
            if car.rect.centerx>bridgestructure.rect.centerx and car.rect.centery<bridgestructure.rect.bottom and car.rect.centery>bridgestructure.rect.top:
                car.rect.centerx -=  car.xspeed
    
                if car.speed == 0:
                    car.rect.centerx += collidepoint[0]+1

            if car.rect.centery<bridgestructure.rect.centery and car.rect.centerx<bridgestructure.rect.right+car.rect.width/2 and car.rect.centerx>bridgestructure.rect.left-car.rect.width/2:
                car.rect.centery -= car.yspeed
                if car.speed == 0:
                    car.rect.centery -= (car.rect.height - collidepoint[1])
            if car.rect.centery>bridgestructure.rect.centery and car.rect.centerx<bridgestructure.rect.right+car.rect.width/2 and car.rect.centerx>bridgestructure.rect.left-car.rect.width/2:
                car.rect.centery -= car.yspeed
                if car.speed == 0:
                    car.rect.centery += collidepoint[1]+1

            if justCollided == True:
                car.speed *=0.5
            #check whether the car can go forward or backward based on its relative position to the tree it has collided with
                if car.onBridge == False:
                    if car.orientation == 0:
                    
                        if car.rect.centery>bridgestructure.rect.bottom:
                       
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
                        
                    
                        if car.rect.centery<bridgestructure.rect.top:
                    
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True

                        if car.rect.centerx>bridgestructure.rect.right:
                       
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True
                        
                    
                        if car.rect.centerx<bridgestructure.rect.left:
                    
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
                
                    if car.orientation == 3:
                    
                        if car.rect.centery>bridgestructure.rect.bottom:
                       
                        
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True
                        
                    
                        if car.rect.centery<bridgestructure.rect.top:
                    
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
            
                        if car.rect.centerx>bridgestructure.rect.right:
                       
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True
                    
                        if car.rect.centerx<bridgestructure.rect.left:
                    
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False

                    if car.orientation == 1:
                    
            
                        if car.rect.centery>bridgestructure.rect.bottom:
                       
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
                        
                    
                        if car.rect.centery<bridgestructure.rect.top:
                    
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True

                        if car.rect.centerx>bridgestructure.rect.left:
                       
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
                    
                        if car.rect.centerx<bridgestructure.rect.left:
                    
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True
                
                    if car.orientation == 2:
                    
                        if car.rect.centery>bridgestructure.rect.bottom:
                       
                        
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True
                        
                    
                        if car.rect.centery<bridgestructure.rect.top:
                    
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
            
                        if car.rect.centerx>bridgestructure.rect.left:
                        
                            canReverse = True
                            canAccelerate = False
                            car.accelerate = False
                    
                        if car.rect.centerx<bridgestructure.rect.left:
                    
                            canReverse = False
                            car.reversing = False
                            car.reverse = False
                            car.acclerate = False
                            canAccelerate = True
            
            if canAccelerate == False and canReverse == False:
                canAccelerate = True

           

            if justCollided == False and car.previousangle >=60 and car.rect.centery<485 and car.rect.centery>375:

                car.speed = car.speed *0.9
                car.angle = 89
                car.previousangle = 89
                if car.orientation == 0:
                    car.direction =  89
                if car.orientation == 1:
                    car.direction =  91
                if car.orientation == 2:
                    car.direction =  269
                if car.orientation == 3:
                    car.direction =  271

                # set justCollided to true and set timer to wait for half a second before continuing to check for future collisions
                justCollided = True
                pygame.time.set_timer(COLLISION, 200)

            if justCollided == False and car.previousangle <=30 and (car.rect.centery>485 or car.rect.centery<375):

                car.speed = car.speed *0.9
                car.angle = 1
                car.previousangle = 1
                if car.orientation == 0:
                    car.direction =  1
                if car.orientation == 1:
                    car.direction =  179
                if car.orientation == 2:
                    car.direction =  181
                if car.orientation == 3:
                    car.direction =  359


                # set justCollided to true and set timer to wait for half a second before continuing to check for future collisions
                justCollided = True
                pygame.time.set_timer(COLLISION, 200)
            
            if justCollided == False:
                justCollided = True
                pygame.time.set_timer(COLLISION, 200)


    
# function to check if the car is completing the necessary checkpoints in order to have a successfully completed lap
# function also records successful lap times and best lap times
# function is given the car object and the checkpoints list for the track
def checkpointsCheck (car, checkpoints):
    global lap_time
    global best_lap
    global previous_lap, best_lap, bestLapSeconds
    global race_length
    length = len(checkpoints)

    #for i in range(length):
     #   print(checkpoints[i][0],checkpoints[i][2])

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
                        if car.rect.centerx > checkpoints[x][1][0]-100 and car.rect.centerx < checkpoints[x][1][0]+100 and car.rect.centery > checkpoints[x][1][1]-100 and car.rect.centery < checkpoints[x][1][1]+100:
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
        seconds = round(lap_time - (60*minutes),3)
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

    for track in RTrackPieces:
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


def checkCarIsOnSCreen():
    global timePenalty
    trackpiecenumber = 0
    closesttracknumber = 0
    if car1.rect.centerx>width+30 or car1.rect.centerx<-30 or car1.rect.centery > height+30 or car1.rect.centery<20:
        closestDistance = 10000
        for trackpiece in TrackPieces:
            trackpiecenumber+=1
            distanceFromTrack = math.sqrt(abs(trackpiece.rect.centerx - car1.rect.centerx)*abs(trackpiece.rect.centerx - car1.rect.centerx)+abs(trackpiece.rect.centery - car1.rect.centery)*abs(trackpiece.rect.centery - car1.rect.centery))
            if distanceFromTrack < closestDistance:
                closestDistance = distanceFromTrack
                closesttracknumber = trackpiecenumber
        trackpiecenumber = 0
        for trackpiece in TrackPieces:
            trackpiecenumber +=1
            if closesttracknumber == trackpiecenumber:
                car1.rect.center = trackpiece.rect.center
                car1.speed = 0
                car1.accelerate = False
                car1.reverse = False

        timePenalty = True
        pygame.time.set_timer(TIMEPENALTY, 2000)


        
           
      



def selectTrack(track_number):
    global createdTrack
    if createdTrack == False:
        if track_number == 1:
            car1.rect.topleft = (600,600)
            createOvalTrack()
            # create a number of trees to be displayed on the screen
            setTrees(250)
        if track_number == 2:
            car1.rect.topleft = (500,800)
            createTrack2()
            setTrees(200)
        if track_number == 3:
            car1.rect.topleft = (300,100)
            createTrack3()
            setTrees(150)

TrackPieces = pygame.sprite.Group()

BridgeStructure = pygame.sprite.Group()
BridgeWalls = pygame.sprite.Group()
BridgeBarriers = pygame.sprite.Group()
RTrackPieces = pygame.sprite.Group()
Trees = pygame.sprite.Group()
Treetrunks = pygame.sprite.Group()


car1 = Car()


timer = 0
race_countdown = 3
race_time = 0
seconds = 0
minutes = 0
race_length = 10
started_timer = False

laptimes = []
raceStarted = False

# set the timer to record lap times and race time
RACESTART = pygame.USEREVENT + 1
TIMEPENALTY = pygame.USEREVENT +3
COLLISION = pygame.USEREVENT +2


running = True
while running:
    window.fill((200,200,200))

    canAccelerate = True
    canReverse = True
    

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    
        

    # checks if the user has pressed down and/or released the mouse and calls functions accordingly
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
       
        # check which directional keys the user is pressing
        if event.type == pygame.KEYDOWN:
            if game_stage == "race":
                if event.key == pygame.K_UP and justCollided == False and timePenalty == False:
                    car1.accelerate = True

                if event.key == pygame.K_UP and justCollided == True  and canAccelerate == True:
                    car1.accelerate = True
                
                if event.key == pygame.K_DOWN and justCollided == False and timePenalty == False:
                    car1.reverse = True
            
                if event.key == pygame.K_DOWN and justCollided == True and canReverse == True:
                    car1.reverse = True

                if event.key == pygame.K_LEFT and justCollided == False:
                    car1.turnleft = True

                if event.key == pygame.K_RIGHT and justCollided == False:
                    car1.turnright = True


        
        if event.type == pygame.KEYUP:
            if game_stage == "race":
                if event.key == pygame.K_UP:
                    car1.accelerate = False

                if event.key == pygame.K_DOWN:
                    car1.reverse = False
            
                if event.key == pygame.K_LEFT:
                    car1.turnleft = False
                
                if event.key == pygame.K_RIGHT:
                    car1.turnright = False

        if event.type == pygame.MOUSEBUTTONDOWN and game_stage == "main menu":
            x, y = event.pos
            if trackimage_rect.collidepoint(x, y):
                selectTrack(1)
                selectedTrack = 1
                game_stage = "race"
            if trackimage2_rect.collidepoint(x, y):
                selectTrack(2)
                selectedTrack = 2
                game_stage = "race"
            if trackimage3_rect.collidepoint(x, y):
                selectTrack(3)
                selectedTrack = 3
                game_stage = "race"
        
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
                    car_kmh = int(car1.speed*6)
                lap_time +=0.00125
                if seconds >= 60:
                    seconds = 0
                    minutes+=1

        if event.type == COLLISION:
            justCollided = False

            pygame.time.set_timer(COLLISION, 0)

        if event.type == TIMEPENALTY :
            timePenalty = False

            pygame.time.set_timer(TIMEPENALTY, 0)


    if game_stage == "main menu":
        choose_track_textRect.center = (width *0.5, 200)
        window.blit(choose_track_text, choose_track_textRect)
        window.blit(trackimage, (width*0.4,height*0.5))
        trackimage_rect.topleft = (width*0.4,height*0.5)
        window.blit(trackimage2, (width*0.2,height*0.5))
        trackimage2_rect.topleft = (width*0.2,height*0.5)
        window.blit(trackimage3, (width*0.6,height*0.5))
        trackimage3_rect.topleft = (width*0.6,height*0.5)




    if game_stage == "race":

        window.blit(background, (0,0))

        #start countdown for start of race
        if started_timer == False:
            pygame.time.set_timer(RACESTART, 1)
            started_timer = True
        

        # check if the car has collided with a tree (this function needs some work)
        treeCollisionCheck(car1, Treetrunks)

        # check if the car has collided with the bridge structure (if the track has a bridge)
        if selectedTrack == 3:

            if car1.onBridge == False and ((car1.rect.centerx>600 and car1.rect.centerx<1000) or (car1.rect.centery<375 or car1.rect.centery>485)):
                bridgeWallsCollisionCheck(car1, BridgeWalls)
            if car1.onBridge == True or (car1.rect.centerx<650 or car1.rect.centerx>950):
                bridgeBarriersCollisionCheck(car1, BridgeBarriers)
        if selectedTrack == 3:
            car1.onBridge = car1.onBridgeCheck(Bridge)

        # check if the user has completed the required number of laps. If so, then stop the race
        if car1.lapsCompleted == race_length:
            raceStarted = False
            countdown_text = font1.render("Race Finished!", True, (0,0,0))



        # check if the car is currently on the track
        car1.onTrack = False
        car1.onRallyTrack = False
        for track in TrackPieces:
            carOnTrack = pygame.sprite.collide_mask(car1,track)
            if carOnTrack:
                car1.onTrack = True
        for track in RTrackPieces:
            carOnTrack = pygame.sprite.collide_mask(car1,track)
            if carOnTrack:
                car1.onTrack = True
                car1.onRallyTrack = True


        # allow the car to move once the race has started
        if raceStarted == True:
            car1.update()

        checkCarIsOnSCreen()


        if car1.speed >=10 or car1.rect.centery>485 or car1.rect.centery<375:
            drawBridge = True

        # draw track pieces, car, and trees on the display (don't draw tree trunks)
        if selectedTrack == 3:
            for trackpiece in TrackPieces:
                for bridge in Bridge:
                    if trackpiece.rect.topleft != bridge.rect.topleft:
                        window.blit(trackpiece.image, trackpiece.rect.topleft)
                    if trackpiece.rect.topleft == bridge.rect.topleft and drawBridge == True:
                        window.blit(trackpiece.image, trackpiece.rect.topleft)
        else:
            TrackPieces.draw(window)
        

        window.blit(car1.Rotated_image, car1.rect.topleft)

        BridgeWalls.draw(window)
        if drawBridge == True:
           Bridge.draw(window)
        Trees.draw(window)
        if car1.onBridge == True:
            window.blit(car1.Rotated_image, car1.rect.topleft)
        BridgeBarriers.draw(window)
        #BridgeStructure.draw(window)
        
        #draw bar at top of the sreen for displaying text on
        pygame.draw.rect(window,(240,240,240),pygame.Rect(0,0,width,40))

        # edit text values and display at the top of the screen
        laps_completed_text = font1.render('Laps completed: '+str(car1.lapsCompleted) +"/"+str(race_length), True, (0,0,0))
        laps_completed_textRect.center = (width *0.45, 20)
        window.blit(laps_completed_text, laps_completed_textRect)
        if race_countdown > 0:
            countdown_text = font1.render(str(race_countdown), True, (0,0,0))
        else:
            if raceStarted == True:
                countdown_text = font1.render("Start!", True, (0,0,0))
        countdown_textRect.center = (width *0.575, 20)
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