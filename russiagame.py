import sys
import pygame 
import random 
from pygame import mixer


score = 0

width =  700
height = 800
screen = pygame.display.set_mode((width, height))


pygame.display.set_caption("shooting game")
pygame.font.get_fonts()
pygame.init()
pygame.font.init()
mixer.init()
clock = pygame.time.Clock()
fps = 60
font30 = pygame.font.SysFont(None, 30)
font40 = pygame.font.SysFont(None, 80)





#true false variables
smallbullets_is_zero = False
smallrockets_is_zero = False
mediumbullets_is_zero = False

endgame = False

enemymediumsignal = False
enemysmallsignal = False
enemyrocketsignal = False

drawtextsignal = False

#colors 
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)


#enemylifes
enemysmallbullet = 3
enemymediumbullet = 2
enemyrocket = 1


#bullets how much I have
smallbullets = 500
mediumbullets = 250
rocketsbullets = 50
fireshots = 20

#text


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))




#bg
bg = pygame.image.load("bg.png")


#sounds
smallgunshot = mixer.Sound("smallshot.wav")
mixer.Sound.set_volume(smallgunshot, .8)

mediumshot = mixer.Sound("mediumshot.wav")
mixer.Sound.set_volume(mediumshot, 1)

explosion_sound = mixer.Sound("explosion.wav")
mixer.Sound.set_volume(explosion_sound, .5)


#colors
red = (255,0,0)

startenemy = False
start1v1 = False


rocket_signal = False
medium_bullet_signal = True
smallbullet_signal = False

flag = pygame.image.load("ukraine.png")



#classes
#class player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("jet.png")
        self.flag = flag
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed
        self.lastshot = pygame.time.get_ticks()

    def update(self):
        global smallbullets_is_zero,startenemy, rocket_signal, medium_bullet_signal, smallbullet_signal, start1v1, mediumbullets, smallbullets, rocketsbullets, fireshots
        cooldown_smallbullet = 150
        cooldown_mediumbullet = 300
        cooldown_rocket = 600
        cooldownfire = 100

        key = pygame.key.get_pressed()
        if key[pygame.K_a] and self.rect.x > 0 and endgame == False:
            self.rect.x -= self.speed
        if key[pygame.K_d] and self.rect.x < width - 64 and endgame == False:
            self.rect.x += self.speed

        nowtime = pygame.time.get_ticks()

        #create mediumbullet
        if key[pygame.K_SPACE] and nowtime - self.lastshot >= cooldown_mediumbullet and endgame == False and mediumbullets > 0:
            if medium_bullet_signal:
                rocket_signal = False
                smallbullet_signal = False
                bullet = Bullets(self.rect.centerx, self.rect.top)
                mediumshot.play()
                bullet_group.add(bullet)
                mediumbullets = mediumbullets - 1
                self.lastshot = nowtime
        #create rocket
        if key[pygame.K_SPACE] and nowtime - self.lastshot >= cooldown_rocket and endgame == False and rocketsbullets > 0:
            if rocket_signal:
                medium_bullet_signal = False
                smallbullet_signal = False
                rocket = Rockets(self.rect.centerx, self.rect.top)
                rocket_group.add(rocket)
                rocketsbullets = rocketsbullets - 1
                self.lastshot = nowtime

        #create smallbullet

        if key[pygame.K_SPACE] and nowtime - self.lastshot >= cooldown_smallbullet and endgame == False and smallbullets > 0:
            if smallbullet_signal:
                medium_bullet_signal = False
                rocket_signal = False

                 
                smallbullet = smallullets(self.rect.centerx, self.rect.top)
                smallbullets_group.add(smallbullet)
                smallbullets = smallbullets - 1
                self.lastshot = nowtime
                smallgunshot.play()
        
        #create fire
        if key[pygame.K_f] and nowtime - self.lastshot >= cooldownfire and endgame == False and fireshots > 0:
            flame = lasthope(self.rect.centerx, self.rect.centery)
            flame2 = lasthopend(self.rect.centerx, self.rect.centery)
            lasthope_group.add(flame)
            lasthopend_group.add(flame2)
            self.lastshot = nowtime
            fireshots -= 1

        

        #ready for enemies
        if key[pygame.K_r] and start1v1 == False:
            startenemy = True
            start1v1 = False
        
        if key[pygame.K_m] and startenemy == False:
            start1v1 = True
            startenemy = False


class lasthope(pygame.sprite.Sprite):
    def __init__(self, x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("flame.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        global score

        self.rect.x -= 10
        if pygame.sprite.spritecollide(self, enemy_group, True):

            self.kill()
            Explosion = explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(Explosion)
            score = score + 1
class lasthopend(pygame.sprite.Sprite):
    def __init__(self, x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("flame.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        global score
        self.rect.x += 10
        if pygame.sprite.spritecollide(self, enemy_group, True):
            self.kill()
            Explosion = explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(Explosion)
            score = score + 1
        


#bullets rockets and small bullets
class Rockets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bomb (2).png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        global score
        self.rect.y -= 8
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, enemy_group, True):
            self.kill()
            Explosion = explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(Explosion)
            score = score + 1
            explosion_sound.play()
            

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet (2).png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        global enemymediumbullet, enemymediumsignal, score
        self.rect.y -= 8
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, enemy_group, False):
            enemymediumbullet = enemymediumbullet -1
            if enemymediumbullet <= 0:
                enemymediumsignal = True
            self.kill()
        if pygame.sprite.spritecollide(self, enemy_group, enemymediumsignal) and enemymediumbullet <= 0:
            enemymediumsignal = False
            enemymediumbullet = 2

            self.kill()

            Explosion = explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(Explosion)
            score = score + 1
         

class smallullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("smallbullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        global enemysmallsignal, enemysmallbullet, score
        self.rect.y -= 8
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, enemy_group, False):
            self.kill()
            enemysmallbullet = enemysmallbullet - 1
            if enemysmallbullet <= 0:
                enemysmallsignal = True

        if pygame.sprite.spritecollide(self, enemy_group, enemysmallsignal) and enemysmallbullet <= 0:
            enemysmallsignal = False
            enemysmallbullet = 3

            self.kill()

            Explosion = explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(Explosion)
            score = score + 1



#enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("russia.png")#("alien" + str(random.randint(1,5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.lastenemy = pygame.time.get_ticks()


    def update(self):
        self.rect.y += 2
        
#exp 
class explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f"exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20,20))
            if size == 2:
                img = pygame.transform.scale(img, (60,60))
            if size == 3:
                img = pygame.transform.scale(img, (200,200))
            #add image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.counter = 0

    def update(self):
        explosion_speed = 3

        #update animation
        self.counter += 1
        
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        #if complete then kill
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()



#CLASSES END


#create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
rocket_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
smallbullets_group = pygame.sprite.Group()
lasthope_group = pygame.sprite.Group()
lasthopend_group = pygame.sprite.Group()



ukraine = pygame.image.load("ukraine.png")

player = Player((width / 2), height - 150, 10)
spaceship_group.add(player)

enemy = Enemy(random.randint(100,500), -50)

delay = 800
#MAINLOOP
run = True
while run:
    
    #bullets check
    if smallbullets <= 0:
        smallbullets_is_zero = True
    if smallbullets_is_zero:
        draw_text("not enough bullets", font40, white, int(width / 2 - 150), (height / 2))
    


    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                rocket_signal = True
                medium_bullet_signal = False
                smallbullet_signal = False
                
            if event.key == pygame.K_2:
                medium_bullet_signal = True
                rocket_signal = False
                smallbullet_signal = False

            if event.key == pygame.K_1:
                smallbullet_signal = True
                rocket_signal = False
                medium_bullet_signal = False
            


    #enemy settings
    
    
    time_now = pygame.time.get_ticks()
    
    if time_now - enemy.lastenemy >= delay and startenemy:
        enemy = Enemy(random.randint(100,500), -50)
        enemy_group.add(enemy)
        #enemy.update()
        enemy.lastenemy = time_now
        

        


    screen.fill((0,0,50))
    bg.blit(screen, (0,0))
    
    #update spaceship
    player.update()

    #update sprite groups
    bullet_group.update()
    enemy_group.update()
    rocket_group.update()
    explosion_group.update()
    smallbullets_group.update()
    lasthope_group.update()
    lasthopend_group.update()


    #draw sprite group
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    enemy_group.draw(screen)
    rocket_group.draw(screen)
    explosion_group.draw(screen)
    smallbullets_group.draw(screen)
    lasthope_group.draw(screen)
    lasthopend_group.draw(screen)


    screen.blit(ukraine, (player.rect.x +20, player.rect.y + 20))

    
    draw_text("score: " + str(score), font30, white, 0, 0)

    draw_text("smallbullets: " + str(smallbullets), font30, white, 0, 50)
    draw_text("mediumbullets: " + str(mediumbullets), font30, white, 0, 70)
    draw_text("rockets: " + str(rocketsbullets), font30, white, 0, 90)
    draw_text("fireshots: " + str(fireshots), font30, white, 0, 110)
    

    if drawtextsignal:
        draw_text("YOU LOST", font40, white, int(width / 2 - 150), (height / 2))
        draw_text("your score is: " + str(score), font30, white, int(width / 2 - 70), (height / 2 + 60))
    for somenemy in enemy_group:
        if somenemy.rect.y > 800:
            drawtextsignal = True
            for i in enemy_group:
                i.kill()
                endgame = True
                delay = 999999999999999999
    
    
    pygame.display.update()


pygame.quit()
quit()

