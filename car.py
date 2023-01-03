from multiprocessing.connection import answer_challenge
import pygame
import onBridgeCheck



import math

from pygame.locals import *

global car1
global rotated_image
global rotated_image_rect
global rotated_image_center
width = 1600
height = 900
window = pygame.display.set_mode((width,height))
car = pygame.image.load("car.png").convert()
car = pygame.transform.scale(car,(60,30))
Bridge = pygame.sprite.Group()


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
        self.onRallyTrack = False
        self.lapsCompleted = 0
        self.reversing = False
        self.onBridge = False
        self.enteredBridge = False


    def onBridgeCheck(self,Bridge):
        
        onBridge = self.onBridge
        #600,375 (400 wide / 110 high)
       
        for bridge in Bridge:
            collided = pygame.sprite.collide_mask(self,bridge)
            if collided:
                if self.rect.left<600:
                    if self.rect.centery>385 and self.rect.centery<475:
                        self.enteredBridge = True
                if self.rect.right>1000:
                    if self.rect.centery>385 and self.rect.centery<475:
                        self.enteredBridge = True

        for bridge in Bridge:
            collided = pygame.sprite.collide_mask(self,bridge)
            if collided:
                if self.rect.centery>385 and self.rect.centery<475 and self.enteredBridge == True:
                    onBridge = True
                else:
                    onBridge = False
                    self.enteredBridge = False
            else:
                    onBridge = False
                    self.enteredBridge = False
        
        #if self.rect.centerx == 600 and self.rect.centery>385 and self.rect.centery<475:
         #   if self.xspeed > 0:
          #      onBridge = True
           # if self.xspeed < 0:
            #    onBridge = False

        return onBridge           

   


    def update(self):
    
        

        
        

       
       #Stops the car from moving backwards once it comes to a halt, and starts it moving forwards
        if self.accelerate == True and self.speed == 0:
            self.reversing = False

        #change direction of car if on track
        if self.onTrack == True:
            if self.turnleft == True and self.speed>2.5:
                self.turnspeed = (28 - self.speed) / 4
                if self.reversing == False:
                    self.direction += self.turnspeed
                else:
                    self.direction -= self.turnspeed
                if self.direction >=360:
                    self.direction = 0
            if self.turnright == True and self.speed>.5:
                self.turnspeed = (28 - self.speed) / 4
                if self.reversing == False:
                    self.direction -= self.turnspeed
                else:
                    self.direction += self.turnspeed
                if self.direction <=-360:
                    self.direction = 0

        #change direction of car if off track
        if self.onTrack == False:

            if self.turnleft == True and self.speed>1:
                self.turnspeed = (28 - self.speed) / 4
                if self.reversing == False:
                    self.direction += self.turnspeed
                else:
                    self.direction -= self.turnspeed
                if self.direction >=360:
                    self.direction = 0
            if self.turnright == True and self.speed>1:
                self.turnspeed = (28 - self.speed) / 4
                if self.reversing == False:
                    self.direction -= self.turnspeed
                else:
                    self.direction += self.turnspeed
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
                traction = 3.4
            elif self.speed <=20:
                traction = 3
            elif self.speed <=30:
                traction = 2

        if self.onRallyTrack == True:
            traction -=0.8
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
            self.speed +=0.4
         

        # slow the car down if it is off the track and going faster than 8
        if self.onTrack == False and self.speed>8:
            self.speed -=2

        if self.onRallyTrack == True and self.speed>15:
            self.speed = 15
        
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

