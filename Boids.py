import pygame as pg
import random
import math
import numpy as np

radius=40
popsize=100
maxspeed=5.0

def norm(v):
    sum = np.zeros(1).astype('float128')
    for i in range(len(v)):
        sum += v[i]**2
    return sum**0.5
        

pg.init()
screen = pg.display.set_mode((800,600))
pg.display.set_caption("Boids Simulation")
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
        # 定位
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        print('dx:',self.dx)
        print('dy:',self.dy)
        self.neighbors = []
        
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
        self.neighbors.clear()
        for o in other:
            if o!=self:
                if math.dist([self.x,self.y],[o.x,o.y]) < radius:
                    self.neighbors.append(o)
                    
    def cohension(self):
        cV = np.zeros(2).astype('float128')
        print('type', type(cV[0]))
        if not self.neighbors:
            return cV
        for n in self.neighbors:
            cV[0]+=n.x
            cV[1]+=n.y
        cV/=len(self.neighbors)
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
        if not self.neighbors:
            return sV
        for n in self.neighbors:
            sV[0]+=self.x-n.x
            sV[1]+=self.y-n.y
        sV/=len(self.neighbors)
        
        uu = np.linalg.norm(sV)
        if uu==0:
            uu=0.1
                
        sV = (sV/uu)*maxspeed
        
        #sV = (sV/np.linalg.norm(sV))*maxspeed
        #sV = (sV/norm(sV))*maxspeed
        return sV
        
    def alignment(self):
        aV = np.zeros(2).astype('float128')
        if not self.neighbors:
            return aV
        for n in self.neighbors:
            aV[0]+=n.dx
            aV[1]+=n.dy
        aV/=len(self.neighbors)
        
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



numbers = list(range(-15,-1)) + list(range(1,15))

birds = [Bird(random.randint(40,1360),random.choice(numbers),random.randint(40,860),random.choice(numbers)) for i in range(popsize)]

boids = pg.sprite.Group()
#print(type(boids))

for bird in birds:
    boids.add(bird)
    print(bird)

clock = pg.time.Clock()

running = True
while running:
    clock.tick(40)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
    screen.blit(background,(0,0))
    for bird in birds:
        #print('hi')
        bird.draw()

    for bird in birds:
        bird.update_direction(birds)
    boids.draw(screen)
    pg.display.update()
pg.quit()
