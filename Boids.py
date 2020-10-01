import pygame as pg
import random
import math
import numpy as np

radius=60


pg.init()
screen = pg.display.set_mode((800,600))
pg.display.set_caption("Boids Simulation")
background = pg.image.load('sky.jpg')
background.convert()
screen.blit(background,(0,0))

bdimgsize=(20,20)

img = {'Ebird':pg.transform.scale(pg.image.load('Ebird.png'), bdimgsize),
        'Wbird':pg.transform.scale(pg.image.load('Wbird.png'), bdimgsize),
        'Sbird':pg.transform.scale(pg.image.load('Sbird.png'), bdimgsize),
        'Nbird':pg.transform.scale(pg.image.load('Nbird.png'), bdimgsize),
        'NEbird':pg.transform.scale(pg.image.load('NEbird.png'), bdimgsize),
        'NWbird':pg.transform.scale(pg.image.load('NWbird.png'), bdimgsize),
        'SEbird':pg.transform.scale(pg.image.load('SEbird.png'), bdimgsize),
        'SWbird':pg.transform.scale(pg.image.load('SWbird.png'), bdimgsize)
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
        if self.x>1360:
            self.x -= 1360
        if self.x<40:
            self.x += 1360
        if self.y>860:
            self.y -= 860
        if self.y<40:
            self.y += 860
            
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
        
    def get_neighbors(self,other):
        self.neighbors.clear()
        for o in other:
            if o!=self:
                if math.dist([self.x,self.y],[o.x,o.y]) < radius:
                    self.neighbors.append(o)
                    
    def cohension(self):
        cV = np.zeros(2)
        if not self.neighbors:
            return cV
        for n in self.neighbors:
            cV[0]+=n.x
            cV[1]+=n.y
        cV/=len(self.neighbors)
        cV[0]-=self.x
        cV[1]-=self.y
        return cV
        
    def separation(self):
        sV = np.zeros(2)
        if not self.neighbors:
            return sV
        for n in self.neighbors:
            sV[0]+=self.x-n.x
            sV[1]+=self.y-n.y
        sV/=len(self.neighbors)
        return sV
        
    def alignment(self):
        aV = np.zeros(2)
        if not self.neighbors:
            return aV
        for n in self.neighbors:
            aV[0]+=n.dx
            aV[1]+=n.dy
        aV/=len(self.neighbors)
        return aV
        
    def update_dir(self,other):
        self.get_neighbors(other)
        V = np.zeros(2)
        V += self.cohension()
        V += self.separation()
        V += self.alignment()
        #V /= 3
        if int(V[0]) or int(V[1]):
            self.dx = int(V[0])
            self.dy = int(V[1])

popsize=100

numbers = list(range(-10,-1)) + list(range(1,10))

birds = [Bird(random.randint(40,1360),random.choice(numbers),random.randint(40,860),random.choice(numbers)) for i in range(popsize)]

boids = pg.sprite.Group()
print(type(boids))

for bird in birds:
    boids.add(bird)
    print(bird)

clock = pg.time.Clock()

running = True
while running:
    clock.tick(30)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
    screen.blit(background,(0,0))
    for bird in birds:
        #print('hi')
        bird.draw()

    for bird in birds:
        bird.update_dir(birds)
    boids.draw(screen)
    pg.display.update()
pg.quit()
