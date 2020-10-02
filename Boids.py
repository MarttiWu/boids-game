import pygame as pg
import random
import math
import numpy as np

a_radius=50
s_radius=20
c_radius=40
popsize=100
maxspeed=5.0

numbers = list(range(-15,-1)) + list(range(1,15))

pg.init()
screen = pg.display.set_mode((800,600))
pg.display.set_caption("Boids Game")
background = pg.image.load('images/sky.jpg')
background.convert()
screen.blit(background,(0,0))

bdimgsize=(20,20)

img = {'Ebird':pg.transform.scale(pg.image.load('images/Ebird.png'), bdimgsize),
        'Wbird':pg.transform.scale(pg.image.load('images/Wbird.png'), bdimgsize),
        'Sbird':pg.transform.scale(pg.image.load('images/Sbird.png'), bdimgsize),
        'Nbird':pg.transform.scale(pg.image.load('images/Nbird.png'), bdimgsize),
        'NEbird':pg.transform.scale(pg.image.load('images/NEbird.png'), bdimgsize),
        'NWbird':pg.transform.scale(pg.image.load('images/NWbird.png'), bdimgsize),
        'SEbird':pg.transform.scale(pg.image.load('images/SEbird.png'), bdimgsize),
        'SWbird':pg.transform.scale(pg.image.load('images/SWbird.png'), bdimgsize)
}

class Bird(pg.sprite.Sprite):
    
    def __init__(self,x,dx,y,dy):
        super().__init__()
        self.image = img['Nbird']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        #print('dx:',self.dx)
        #print('dy:',self.dy)
        self.aneighbors = []
        self.cneighbors = []
        self.sneighbors = []
        
    def draw(self):
        
        if self.x>800:
            self.x = 0
        if self.x<0:
            self.x = 800
        if self.y>600:
            self.y = 0
        if self.y<0:
            self.y = 600
        '''
        if self.x>780 or self.x<0:
            self.dx = -self.dx
            self.x += self.dx

        if self.y>580 or self.y<0:
            self.dy = -self.dy
            self.y += self.dy
        '''
        if self.is_collided_with(obstacles):
            self.dx = -self.dx
            self.dy = -self.dy
            #self.x += self.dx/np.linalg.norm((self.dx,self.dy))*70
            #self.y += self.dy/np.linalg.norm((self.dx,self.dy))*70
            self.x += random.choice(numbers)*2
            self.x += random.choice(numbers)*2
            
        if self.dx>0 and self.dy>0:
            self.image = img['SEbird']
        elif self.dx>0 and self.dy<0:
            self.image = img['NEbird']
        elif self.dx<0 and self.dy>0:
            self.image = img['SWbird']
        elif self.dx<0 and self.dy<0:
            self.image = img['NWbird']
        elif self.dx>0 and self.dy==0:
            self.image = img['Ebird']
        elif self.dx==0 and self.dy>0:
            self.image = img['Nbird']
        elif self.dx<0 and self.dy==0:
            self.image = img['Wbird']
        elif self.dx==0 and self.dy<0:
            self.image = img['Sbird']
        
        self.rect.center = (self.x,self.y)
        self.x += self.dx
        self.y += self.dy
        
    def find_neighbors(self,other):
        self.cneighbors.clear()
        self.sneighbors.clear()
        self.aneighbors.clear()
        for o in other:
            if o!=self:
                if math.dist([self.x,self.y],[o.x,o.y]) < c_radius:
                    self.cneighbors.append(o)
                if math.dist([self.x,self.y],[o.x,o.y]) < s_radius:
                    self.sneighbors.append(o)
                if math.dist([self.x,self.y],[o.x,o.y]) < a_radius:
                    self.aneighbors.append(o)
                    
    def cohension(self):
        cV = np.zeros(2).astype('float128')
        #print('type', type(cV[0]))
        if not self.cneighbors:
            return cV
        for n in self.cneighbors:
            cV[0]+=n.x
            cV[1]+=n.y
        cV/=len(self.cneighbors)
        cV[0]-=self.x
        cV[1]-=self.y
        
        uu = np.linalg.norm(cV)
        if uu==0:
            uu=0.01
                
        cV = (cV/uu)*maxspeed
        #cV = (cV/np.linalg.norm(cV))*maxspeed
        
        #cV = (cV/norm(cV))*maxspeed
        #print(cV)
        return cV
        
    def separation(self):
        sV = np.zeros(2).astype('float128')
        if not self.sneighbors:
            return sV
        for n in self.sneighbors:
            sV[0]+=self.x-n.x
            sV[1]+=self.y-n.y
        sV/=len(self.sneighbors)
        
        uu = np.linalg.norm(sV)
        if uu==0:
            uu=0.1
                
        sV = (sV/uu)*maxspeed
        
        #sV = (sV/np.linalg.norm(sV))*maxspeed
        #sV = (sV/norm(sV))*maxspeed
        return sV
        
    def alignment(self):
        aV = np.zeros(2).astype('float128')
        if not self.aneighbors:
            return aV
        for n in self.aneighbors:
            aV[0]+=n.dx
            aV[1]+=n.dy
        aV/=len(self.aneighbors)
        
        uu = np.linalg.norm(aV)
        if uu==0:
            uu=0.1
                
        aV = (aV/uu)*maxspeed
        
        #aV = (aV/np.linalg.norm(aV))*maxspeed
        #aV = (aV/norm(aV))*maxspeed
        return aV
        
    def update_direction(self,other):
        self.find_neighbors(other)
        V = np.zeros(2).astype('float128')
        V += self.cohension()
        V += self.separation()
        V += self.alignment()
        
        uu = np.linalg.norm(V)
        if uu==0:
            uu=0.1
                
        V = (V/uu)*maxspeed
        
        #V = (V/np.linalg.norm(V))*maxspeed
        #V = (V/norm(V))*maxspeed
        
        if int(V[0]) or int(V[1]):
            self.dx = int(V[0])
            self.dy = int(V[1])
            
    def is_collided_with(self, obstacles):
        col = False
        for ob in obstacles:
            if self.rect.colliderect(ob.rect):
                col = True
        return col





def init_boids():
    birds = [Bird(random.randint(40,1360),random.choice(numbers),random.randint(40,860),random.choice(numbers)) for i in range(popsize)]

    boids = pg.sprite.Group()

    for bird in birds:
        boids.add(bird)
        
    return birds,boids

clock = pg.time.Clock()



obimgsize = (30,30)
obimg = pg.transform.scale(pg.image.load('images/block.png'), obimgsize)



obstacles = []

OBSTACLE = pg.sprite.Group()
class Obstacle(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = obimg
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
    def draw(self):
        self.rect.center = (self.x,self.y)


'''
def drawob():
    mouses = pg.mouse.get_pos()

    size=(50,50)
    ob = pg.Surface(size)
    ob.fill((255,255,255))
    pg.draw.rect(ob, (255,0,0), ob.get_rect())
    rect = ob.get_rect()
    ob.fill((255,255,255))
    #rect.center = (mouses[0],mouses[1])
    
    rect.centerx = mouses[0]
    rect.centery = mouses[1]
'''






#############
color = (255,255,255)

color_light = (170,170,170)
  
color_dark = (100,100,100)
  
smallfont = pg.font.SysFont('Arial',20)

###############


birds,boids = init_boids()
running = True
START=False
OBon=False
while running:
    clock.tick(40)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
            
        #print('OBon',OBon)
        if e.type == pg.MOUSEBUTTONDOWN and OBon:
            #if 100 <= mouse[0] <= 700 and 100 <= mouse[1] <= 500:
            #print('Hiiiiiiiiiii')
            pos = pg.mouse.get_pos()
            if 0 <= pos[1] <= 540:
                ob = Obstacle(pos[0],pos[1])
                obstacles.append(ob)
                OBSTACLE.add(ob)
            
        if e.type == pg.MOUSEBUTTONDOWN:
            if 600 <= mouse[0] <= 700 and 560 <= mouse[1] <= 580:
                pg.quit()
            if 100 <= mouse[0] <= 200 and 560 <= mouse[1] <= 580:
                START=True
                
            if 250 <= mouse[0] <= 350 and 560 <= mouse[1] <= 580:
                birds,boids = init_boids()
                obstacles.clear()
                OBSTACLE.empty()
                START=True
                OBon=False
                
            if 450 <= mouse[0] <= 550 and 560 <= mouse[1] <= 580:
                OBon=True
                #print('hi')
            
            '''
            if 250 <= mouse[0] <= 350 and 560 <= mouse[1] <= 580:
                OBon=True
                print('Obon',OBon)
            '''
    
    
    
    
    #buttons = pg.mouse.get_pressed()
    #if buttons[0]:
    #    drawob()
            
            
    screen.blit(background,(0,0))
    
    if START:
    
        for ob in obstacles:
            ob.draw()
            #print('x:',ob.x)
            #print('y:',ob.y)
        
        OBSTACLE.draw(screen)
        
        
        for bird in birds:
            bird.draw()

        for bird in birds:
            bird.update_direction(birds)

        boids.draw(screen)
    
    
    
    mouse = pg.mouse.get_pos()
    ####
    if 600 <= mouse[0] <= 700 and 560 <= mouse[1] <= 580:
        pg.draw.rect(screen,color_light,[600,560,100,20])
    else:
        pg.draw.rect(screen,color_dark,[600,560,100,20])
    screen.blit(smallfont.render('Quit' , True , color) , (600+35,560+3))
    
    if 100 <= mouse[0] <= 200 and 560 <= mouse[1] <= 580:
        pg.draw.rect(screen,color_light,[100,560,100,20])
    else:
        pg.draw.rect(screen,color_dark,[100,560,100,20])
    screen.blit(smallfont.render('Start' , True , color) , (100+30,560+3))
    
    if 250 <= mouse[0] <= 350 and 560 <= mouse[1] <= 580:
        pg.draw.rect(screen,color_light,[250,560,100,20])
    else:
        pg.draw.rect(screen,color_dark,[250,560,100,20])
    screen.blit(smallfont.render('Restart' , True , color) , (250+30,560+3))
    
    if 450 <= mouse[0] <= 550 and 560 <= mouse[1] <= 580:
        pg.draw.rect(screen,color_light,[450,560,100,20])
    else:
        pg.draw.rect(screen,color_dark,[450,560,100,20])
    screen.blit(smallfont.render('Obstacle' , True , color) , (450+20,560+3))
    #####
    
    
    pg.display.update()
pg.quit()
