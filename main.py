import pygame,math,sys

pygame.init()
display=pygame.display.set_mode((400,400))
pygame.display.set_caption("projet")
clock=pygame.time.Clock()
fps=60

# class ---------------------------
class Block():
    def __init__(self):
        self.pos=(0,0)
        self.mass=1
        self.vx=0
        self.dt=1
        self.width,self.height=int(10*math.log10(self.mass)),int(10*math.log10(self.mass))
    def draw(self):
        self.width,self.height=int(20*math.log10(self.mass)),int(20*math.log10(self.mass))
        pygame.draw.rect(display,(0,200,200),(self.pos[0],self.pos[1],self.width,self.height))
        pygame.draw.rect(display,(200,200,200),(self.pos[0],self.pos[1],self.width,self.height),1)
    def update(self):
        self.pos=(self.pos[0]+self.dt*self.vx,self.pos[1])

class Wall():
    def __init__(self):
        self.pos=(0,0)
        self.image=pygame.image.load("images/wall.png")
    def draw(self):
        display.blit(self.image,self.pos)

class Aff_col():
    def __init__(self):
        self.pos=(250,25)
        self.text='# collision: '
        self.sum_c=0
        self.font=pygame.font.Font(None,25)
    def show(self):
        self.text='# collision: '+str(self.sum_c)
        self.surface=self.font.render(self.text,True,(200,200,200))
        display.blit(self.surface,self.pos)

class p_clack():
    def __init__(self):
        self.pos=(100,100)
        self.image=pygame.image.load("images/image_clack.png")
        self.drawb=False
        self.tf=2
    def draw(self):
        if self.drawb:
            if self.tf <0:
                self.tf=2
                self.drawb=False
            display.blit(self.image,self.pos)
            self.tf-=1
# setup --------------------------
m1=Block()
m2=Block()
wall=Wall()
col=Aff_col()
pc=p_clack()

m1.pos=(100,200)
m2.pos=(200,200)
m1.mass=10
m2.mass=1000

m2.vx=-1

c_m12=False
c_wm1=False

collison_sound=pygame.mixer.Sound("sounds/clack.wav")

# loop ---------------------------
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    m1.pos=(m1.pos[0],300-m1.height)
    m2.pos=(m2.pos[0],300-m2.height)

    m2.update()
    m1.update()

    if m2.pos[0] < m1.pos[0]+m1.width :
        c_m12=True
        col.sum_c+=1
        
    if m1.pos[0] < 25:
        c_wm1=True
        col.sum_c+=1
        
    if c_wm1 or c_m12:
        collison_sound.play()
        pc.drawb=True
    if c_m12:
        pc.pos=(m1.pos[0]+m1.width-5,m1.pos[1]-5)
    if c_wm1:
        pc.pos=(25-5,280-5)
        
    if c_m12:
        c_m12=False
        old_v1=m1.vx
        old_v2=m2.vx
        M1=m1.mass
        M2=m2.mass
        m1.vx=((M1-M2)/(M1+M2))*old_v1+((2*M2)/(M1+M2))*old_v2
        m2.vx=((2*M1)/(M1+M2))*old_v1+((M2-M1)/(M1+M2))*old_v2

    if c_wm1:
        c_wm1=False
        m1.vx=-m1.vx

    # draw -----------------------
    display.fill((0,0,40))
    m1.draw()
    m2.draw()
    col.show()
    pygame.draw.line(display,(200,200,200),(23,300-1),(400,300-1),2)
    wall.draw()
    pc.draw()
    
    # update ---------------------
    pygame.display.flip()
    clock.tick(fps)
