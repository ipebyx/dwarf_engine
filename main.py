import pygame
from threading import Thread
import unicodedata
import pygame.camera
import sys as r
import os



def rcc(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")
############################################# fonts
FONT_SIZE=20
pygame.font.init()
font = pygame.font.SysFont('consolas', FONT_SIZE,True)
titlefont = pygame.font.SysFont('Consolas', 30)
menufont = pygame.font.SysFont('Consolas', 24)
mainfont = pygame.font.SysFont('Arial', 24)
class InputField():
    def __init__(self,screen: pygame.display) -> None:
        self.fields=dict()
        self.screen = screen
    def addField(self,field: pygame.Rect, iid: int):
        self.fields[iid]={"field":field,"input":"","active":False}
    def displayField(self,iid: int, color: tuple, seccolor=(0,0,0)):
        f = self.fields[iid]['field']
        s = self.fields[iid]['input']
        if s=="":
            s = "empty"
            seccolor=(seccolor[0]+80,seccolor[1]+80,seccolor[2]+80)
        nacolor = (color[0]-40,color[0]-40,color[0]-40)
        if self.fields[iid]['active']: pygame.draw.rect(self.screen,color,f)
        else: pygame.draw.rect(self.screen,nacolor,f)
        text_surface = mainfont.render(s, True, seccolor)
        screen.blit(text_surface,f)
    def addChrToField(self,iid: int,s: str):
        if self.fields[iid]['active']: self.fields[iid]['input']+=s
        else: print(f"tried to add a char to non-active field, see {self.fields[iid]}",1)
    def delChrFromField(self,iid: int):
        if self.fields[iid]['active']: self.fields[iid]['input']=self.fields[iid]['input'][:-1]
        else: print(f"tried to del a char to non-active field, see {self.fields[iid]}",1)
    def getInputFromField(self,iid: int):
        return self.fields[iid]['input']
    def setActiveField(self,iid: int): # only one field could be active
        for field in self.fields:
            if iid!=field: self.fields[field]["active"]=False
        self.fields[iid]['active']^=1
    def deActivateField(self,iid: int):
        self.fields[iid]['active']=False



pygame.init()
screen = pygame.display.set_mode((800, 550),pygame.ASYNCBLIT)
commands=InputField(screen)

clock = pygame.time.Clock()
FPS = 60
version = [1,2]
strv='.'.join(list(map(str,version)))
running = True


cursor=pygame.image.load('engine/decals/dwarf_cursor.png')

print("@ipebyx и @prostopelmenhto представляют")
print(f"БЕГИ ЗА АНАНАСОМ!, v{strv}")
name = 'Беги за ананасом!'
pygame.display.set_caption(name)
pygame.display.set_icon(pygame.image.load("engine/decals/dwarf_missing.png"))
g=9.81
creatorMode=False

modesforreal=['decal','hitbox','leveltrigger']
modesforcounter=1
modes='hitbox'


def resetgamestates():
    global mc
    mc=[]
    global debugRectInfo
    debugRectInfo=[]
    global debugTexInfo
    debugTexInfo=[]
    global debilsize
    debilsize=[25,25]
    global debilspid
    debilspid=[0,0]
    global remove
    remove=False
    global removeDecals
    removeDecals=False
    global camsomewhere
    camsomewhere=[]
    global platformo
    platformo=[]
    global debilcoords
    debilcoords=[0,0]
    global cameraposition
    cameraposition=[0,0]
    global decals
    decals=[]
    global textures
    textures=[]
    global levelplatformo
    levelplatformo=[]
    global author
    author=""
    global description
    description=""
    global title
    title=""
    global fillercolor
    fillercolor=(0,0,0)
    
    




def ImageInit():
    global decals
    global textures
    
    for dec in decals:
        try:
            image = pygame.image.load(dec[0])
        except:
            print(f'ТЕКСТУРА "{dec[0]}" НЕ НАЙДЕНА')
            #raise FileNotFoundError(f'ТЕКСТУРА "{dec[0]}" НЕ НАЙДЕНА')
            image = pygame.image.load('engine/decals/dwarf_missing.png')
        image = image.convert_alpha()
        transparency= int(dec[2])
        image.set_alpha(transparency)
        position=dec[1]
        textures.append({"image":image,"transparency":transparency,"position":position,"name":dec[0]})
        #print({"image":image,"transparency":transparency,"position":position,"name":dec[0]})
def load_level(name):
    resetgamestates()
    
    global version
    global debilcoords
    global cameraposition
    global decals
    global platformo
    global textures
    global version
    global strv
    global fi
    global levelplatformo
    global author
    global description
    global title
    global fillercolor
    fi=f"maps/{name}/main"
    try:
        f = open(fi,'r')
        oldksfgjoijr=f.read()
        print(oldksfgjoijr)
        try:
            h=eval(oldksfgjoijr)
        except Exception as EEEEEEEEEEEEEEE:
            print(f"Файл повреждён/несовместим с {strv}, ошибка дана тут: ",end="")
            print(*EEEEEEEEEEEEEEE.args)
            os.system('pause>nil')
            exit()
        f.close()
        debilcoords=h["startpos"] 
        cameraposition=h["sco"] # на самом деле это оффсет хотя кого это волнует
        platformo=h["level"]

        try:
            version=h["dwarfversion"]
        except:
            version=strv='<1.0'
        try:
            decals=h["images"] # decals=/=textures
        except:
            print('Early version (<<1.0) detected, images not included')
            version=strv='<<1.0'
        try:
            levelplatformo=h["mapswitchtriggers"]
        except:
            print("no triggers found ;(")
            version=strv='1.1'
            levelplatformo=[]
        try:
            author=h['author']
            description=h['desc']
        except:
            author="unknown"
            description="unknown"
        try:
            title=h["title"]
        except:
            title="unknown"
        try:
            fillercolor=h["fillercolor"]
        except:
            fillercolor=(0,0,0)
    except Exception as e:
        print(e)
        print(f"Уровень не найден, создаю новый, {e}")
        os.mkdir(f'maps/{name}')
        f = open(fi,'w')
        title=''
        platformo=[pygame.Rect(-1000,50,2000,50)]
        debilcoords=[0,0]
        cameraposition=[0,0]
        fillercolor=(0,0,0)
        decals=[]
        textures=[]
        version=strv="1.2baseplate"



    #decals=['jhkjh']
    #textures=[]
    #print(decals)
    
    #images=[]
    ImageInit()



def displaytext(text,pos,transparency=127,color=(0,0,1)): ## DEBUGG
    font = pygame.font.SysFont("Monospace",FONT_SIZE)
    if color==(0,0,1):
        color=(255-color[0],255-color[1],255-color[2])
    text = font.render(text, True, color).convert_alpha()
    text.set_alpha(transparency)
    screen.blit(text,pos)

"""
try:
    basename=r.argv[1]
except:
    basename=input("karta name? ")
"""
commands.addField(pygame.Rect(10,10,780,32),2) ## map name
commands.setActiveField(2)
basename=""
n=os.listdir("maps/")
import datetime
def size_dir(d):
    file_walker = (
        os.path.join(root, f)
        for root, _, files in os.walk(d)
        for f in files
    )
    return sum(os.path.getsize(f) for f in file_walker)

def check_things():
    CHECKINGDIR=True
    while CHECKINGDIR:
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if commands.fields[2]['active'] and event.type == pygame.KEYDOWN:
                kp = pygame.key.name(event.key)
                kp=rcc(kp)
                if kp=="backspace":
                    commands.delChrFromField(2)
                elif not kp=="return" and not kp=="left ctrl" and not kp=="right ctrl" and not kp=="escape":
                    commands.addChrToField(2,event.unicode.replace(chr(127),""))
                elif kp=="return":
                    basename=commands.fields[2]["input"]
                    commands.deActivateField(2)
                    CHECKINGDIR^=1
        screen.fill((0,0,0))
        pygame.draw.rect(screen,(32,32,32),pygame.Rect(10,50,780,800))
        co=0
        for l in n:
            displaytext("Name",[20,60],255,color=(0,255,255))
            displaytext("Size",[150,60],255,color=(0,255,255))
            displaytext("Created at",[300,60],255,color=(0,255,255))
            displaytext("Changed at",[450,60],255,color=(0,255,255))
            
            size=size_dir("maps/"+l)
            try:
                date=os.stat("maps/"+l+"/main").st_ctime
                date2=os.stat("maps/"+l+"/main").st_mtime
            except:
                date=0
                date2=0
            if commands.fields[2]["input"]==l:
                displaytext(l[0:10],[20,90+co*FONT_SIZE],255,color=(0,255,0))
                displaytext(f"{size} bytes",[150,90+co*FONT_SIZE],255,color=(128,255,128))
                if date!=0:
                    displaytext(f"{datetime.date.fromtimestamp(date)}",[300,90+co*FONT_SIZE],255,color=(128,255,128))
                    displaytext(f"{datetime.date.fromtimestamp(date2)}",[450,90+co*FONT_SIZE],255,color=(128,255,128))
                else:
                    displaytext(f"{datetime.date.fromtimestamp(date)}",[300,90+co*FONT_SIZE],255,color=(128,255,128))
                    displaytext(f"{datetime.date.fromtimestamp(date2)}",[450,90+co*FONT_SIZE],255,color=(128,255,128))
                co+=1
            elif commands.fields[2]["input"] in l:
                displaytext(l[0:10],[20,90+co*FONT_SIZE],255,color=(255,255,255))
                displaytext(f"{size} bytes",[150,90+co*FONT_SIZE],255,color=(200,200,200))
                if date!=0:
                    displaytext(f"{datetime.date.fromtimestamp(date)}",[300,90+co*FONT_SIZE],255,color=(200,200,200))
                    displaytext(f"{datetime.date.fromtimestamp(date2)}",[450,90+co*FONT_SIZE],255,color=(200,200,200))
                else:
                    displaytext(f"No main file",[300,90+co*FONT_SIZE],255,color=(200,200,200))
                    displaytext(f"No main file",[450,90+co*FONT_SIZE],255,color=(200,200,200))
                co+=1

                
        commands.displayField(2,(40,255,255))
        pygame.display.flip()



    load_level(basename)


check_things()
commands.addField(pygame.Rect(10,550-FONT_SIZE*3,400,32),1)


print(platformo)
def DebugCircle(pos,r):
    if creatorMode: pygame.draw.circle(screen,(255,255,255),[pos[0]+cameraposition[0],pos[1]+cameraposition[1]],r)
    

def DebuggerConsole():
    print('Dwarf Engine, made by @ipebyx & @prostopelmenhto')
    while True:
        f = input('in  >>> ')
        k = None
        try:
            try:
                k = eval(f)
            except:
                k = exec(f)
        except Exception as e:
            print('err <<<', e)
        print("out <<<",k)

#Thread(target=DebuggerConsole).start()


def draw_rect_alpha(surface, color, rect): # some code stolen from sof
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def floorcheck():
    a=False
    for k in platformo:
        for m in range(debilcoords[0],debilcoords[0]+debilsize[0]+1):
            if k.collidepoint(m,debilcoords[1]+debilsize[1]): # проверка пола
                debilspid[1]=0
                debilcoords[1]=k.topleft[1]-debilsize[1]
                a=True
                DebugCircle((m,debilcoords[1]+debilsize[1]),5)
        for m in range(debilcoords[0],debilcoords[0]+debilsize[0]+1):
            if k.collidepoint(m,debilcoords[1]+debilsize[1]-15): # проверка пола
                debilspid[1]=0
                debilcoords[1]=k.topleft[1]-debilsize[1]
                a=True
                DebugCircle((m,debilcoords[1]+debilsize[1]-15),5)
    return a
        
def physicscheck():
    
    for k in platformo:
        if k.collidepoint(debilcoords[0]+debilsize[0]+7,debilcoords[1]+debilsize[1]/2) or \
           k.collidepoint(debilcoords[0]-7,             debilcoords[1]+debilsize[1]/2) or \
           k.collidepoint(debilcoords[0]+debilsize[0]+7,debilcoords[1]+debilsize[1]-3) or \
           k.collidepoint(debilcoords[0]-7,             debilcoords[1]+debilsize[1]-3) or \
           k.collidepoint(debilcoords[0]+debilsize[0]+7,debilcoords[1]) or \
           k.collidepoint(debilcoords[0]-7,             debilcoords[1]): # проверка стен
            debilspid[0]=0

        if k.collidepoint(debilcoords[0]+debilsize[0]/2,             debilcoords[1]-5) or \
           k.collidepoint(debilcoords[0],       debilcoords[1]-5) or \
           k.collidepoint(debilcoords[0]+debilsize[0],               debilcoords[1]-5): # проверка крыши
            debilspid[1]=0
            debilcoords[1]=k.bottom+5
        #k.x=k.x+cameraposition[0]
        #k.y=k.y+cameraposition[1]
        mp=list(pygame.mouse.get_pos())
        mp[0]-=cameraposition[0]
        mp[1]-=cameraposition[1]
        

           


        if k.collidepoint(mp) and creatorMode and modes=='hitbox':
            draw_rect_alpha(screen,(255,32,32,196),pygame.Rect(k.x+cameraposition[0],k.y+cameraposition[1],k.w,k.h))
            if remove:
                platformo.remove(k)
                print(platformo)
                break
        elif creatorMode:
            draw_rect_alpha(screen,(255,32,32,128),pygame.Rect(k.x+cameraposition[0],k.y+cameraposition[1],k.w,k.h))

        if k.collidepoint(mp):
            debugRectInfo.append(f"x:{k.x},y:{k.y},w:{k.w},h:{k.h}")

        if len(textures)==0:
            draw_rect_alpha(screen,(128,128,128),pygame.Rect(k.x+cameraposition[0],k.y+cameraposition[1],k.w,k.h))
        #k.x=k.x-cameraposition[0]
        #k.y=k.y-cameraposition[1]

def debugCheckWallsOnRight():
    # короче эта хрень возвращает значение можно ли двигатся в right
    ch = False
    for k in platformo:
        ch |= k.collidepoint([debilcoords[0]+debilsize[0]+5,debilcoords[1]+debilsize[1]/2-3]) or \
              k.collidepoint([debilcoords[0]+debilsize[0]+5,debilcoords[1]+debilsize[1]-3]) or \
              k.collidepoint([debilcoords[0]+debilsize[0]+5,debilcoords[1]-3]               )
    return not ch

def DRAWTRIGGERSPLEASE():
    for i in levelplatformo:
        rect = i[0]
        kuda = i[1]
        if creatorMode: draw_rect_alpha(screen,(255,255,0,127),pygame.Rect(rect.x+cameraposition[0],rect.y+cameraposition[1],rect.w,rect.h))

        print([debilcoords[0]+debilsize[0]/2,debilcoords[1]+debilsize[1]/2],rect)
        if rect.collidepoint([debilcoords[0]+debilsize[0]/2,debilcoords[1]+debilsize[1]/2]):
            load_level(kuda)
        mp=list(pygame.mouse.get_pos())
        mp=[mp[0]-cameraposition[0],mp[1]-cameraposition[1]]
        if rect.collidepoint(mp) and creatorMode and modes=='leveltrigger' and remove:
            levelplatformo.remove(i)
def debugCheckWallsOnLeft():
    ch = False
    # короче эта хрень возвращает значение можно ли двигатся в left
    for k in platformo:
        ch |= k.collidepoint([debilcoords[0]-5,             debilcoords[1]+debilsize[1]/2-3]) or \
              k.collidepoint([debilcoords[0]-5,             debilcoords[1]+debilsize[1]-3]) or \
              k.collidepoint([debilcoords[0]-5,             debilcoords[1]-3]               )
    return not ch
"""
def displayImages():
    for i in images:
        #print(i)
        rct=i[2]
        img=i[1]
        screen.blit(img,pygame.Rect(rct[0]+cameraposition[0],rct[1]+cameraposition[1],rct.w,rct.h))
        """

def getGlobalMouseCoords(withSnap):
    gp=list(pygame.mouse.get_pos())
    if withSnap:
        gp[0]=(gp[0]-cameraposition[0])//SNAP*SNAP
        gp[1]=(gp[1]-cameraposition[1])//SNAP*SNAP
    else:
        gp[0]=gp[0]-cameraposition[0]
        gp[1]=gp[1]-cameraposition[1]
    return gp

def displayTextures():
    disp=0
    for l in textures:
        img=l["image"]
        rct=l["position"]
        imgrect=img.get_rect()
        reeeeeeeeeeect=pygame.Rect(rct[0]+cameraposition[0],rct[1]+cameraposition[1],imgrect.w,imgrect.h)
        #if pygame.Rect(0,0,880,550).collidepoint(reeeeeeeeeeect.topleft) or\
        #    pygame.Rect(0,0,880,550).collidepoint(reeeeeeeeeeect.topright) or\
        #    pygame.Rect(0,0,880,550).collidepoint(reeeeeeeeeeect.bottomleft) or\
        #    pygame.Rect(0,0,880,550).collidepoint(reeeeeeeeeeect.bottomright):
        screen.blit(img,pygame.Rect(rct[0]+cameraposition[0],rct[1]+cameraposition[1],0,0))
        disp+=1
        mp=list(pygame.mouse.get_pos())
        if reeeeeeeeeeect.collidepoint(mp) and creatorMode and modes=='decal':
            draw_rect_alpha(screen,(0,0,255,127),reeeeeeeeeeect)

            if remove and removeDecals:
                #print(decals,textures)
                for dec in decals:
                    print('dec',dec)
                    print('l',l)
                    
                    if dec[0]==l["name"] and dec[1]==l["position"]:
                        decals.remove(dec)
                        break
                    print(dec[0],l["name"])
                    print(l["position"],[imgrect.x,imgrect.y])
                #print(decals,textures)
                textures.remove(l)
                #print(decals,textures)
        if reeeeeeeeeeect.collidepoint(mp):
            debugTexInfo.append(f"x:{rct[0]},y:{rct[1]},w:{imgrect.w},h:{imgrect.h}")
        elif creatorMode:
            draw_rect_alpha(screen,(127,127,255,127),reeeeeeeeeeect)
        """
        mp=list(pygame.mouse.get_pos())
        mp[0]-=cameraposition[0]
        mp[1]-=cameraposition[1]
        k=img.get_rect()
        pos=pygame.Rect(rct[0]+cameraposition[0],rct[1]+cameraposition[1],0,0)
        draw_rect_alpha(screen,(0,0,255,128),k)
        
        if k.collidepoint(mp) and creatorMode:
            
            pygame.draw.rect(screen,(196,196,196),pygame.Rect(pos.x,pos.y,k.w,k.h))
            print(f'hovering on {id(img)}, {img}')
            if remove:
                textures.remove(l)"""
    return disp
#textures.append({"image":image,"transparency":transparency,"position":position})
holdingLeft=False
holdingRight=False
holdingKeyLeft=False
holdingKeyRight=False

#ImageInit()

print(textures)

SNAP=15
 
def savelevel():
    global mc
    level=f"{str(platformo).replace('<','').replace('>','').replace('rect','pygame.Rect')}"
    total=f"'title':'{title}','fillercolor':{fillercolor},'level':{level},'images':{decals},'startpos':{debilcoords},'sco':{cameraposition},'dwarfversion':'{strv}','mapswitchtriggers':{str(levelplatformo).replace('<','').replace('>','').replace('rect','pygame.Rect')},'author':'{author}','desc':'{description}'"
    f=open(fi,mode="w")
    f.write("{"+total+"}")
    f.close()
    #print(fi)
    mc=[]

del commands.fields[2]

while running:############################################################################################################
    
    try:
        screen.fill(fillercolor)
    except:
        screen.fill(eval(fillercolor))
    

    DebugCircle([debilcoords[0]+debilsize[0]+5,debilcoords[1]+debilsize[1]/2-3],5) # справа коллизия стен (я свм нифига не понимаю)
    DebugCircle([debilcoords[0]+debilsize[0]+5,debilcoords[1]+debilsize[1]-3],5) # справа
    DebugCircle([debilcoords[0]+debilsize[0]+5,debilcoords[1]-3],               5) # справа
    DebugCircle([debilcoords[0]-5,             debilcoords[1]+debilsize[1]/2-3],5) # слево
    DebugCircle([debilcoords[0]-5,             debilcoords[1]+debilsize[1]-3],5) # слево
    DebugCircle([debilcoords[0]-5,             debilcoords[1]-3],               5) # слево
    DebugCircle([debilcoords[0]+debilsize[0]/2,             debilcoords[1]-5],5)
    DebugCircle([debilcoords[0],       debilcoords[1]-5],5)
    DebugCircle([debilcoords[0]+debilsize[0],               debilcoords[1]-5],5)
    k=displayTextures()
    #print(f'displayed {k} textures')
    floorcheck()
    physicscheck()
    DRAWTRIGGERSPLEASE()
    remove=False
    for event in pygame.event.get():
        if event.type==pygame.QUIT:pygame.quit();exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:holdingLeft=True;holdingKeyLeft=True
            if event.key==pygame.K_RIGHT:holdingRight=True;holdingKeyRight=True
            if event.key==pygame.K_UP and debilspid[1]==0:debilcoords[1]=debilcoords[1]-1;debilspid[1]=-g*2
            if event.key==pygame.K_F1:creatorMode^=1
            if event.key==pygame.K_F2:removeDecals^=1
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:holdingLeft=False;holdingKeyLeft=False
            if event.key==pygame.K_RIGHT:holdingRight=False;holdingKeyRight=False
            if event.key==pygame.K_RIGHT:holdingRight=False;holdingKeyRight=False
        if creatorMode:
            #if event.type == pygame.MOUSEBUTTONDOWN and not commands.fields[1]["field"].collidepoint(event.pos)  :
            #    commands.deActivateField(1)
            #    mc=[]
            if commands.fields[1]['active'] and event.type == pygame.KEYDOWN:
                kp = pygame.key.name(event.key)
                kp=rcc(kp)
                if kp=="backspace":
                    commands.delChrFromField(1)
                elif not kp=="return" and not kp=="left ctrl" and not kp=="right ctrl" and not kp=="escape":
                    commands.addChrToField(1,event.unicode.replace(chr(127),""))
                elif kp=="return":
                    try:
                        exec(commands.getInputFromField(1))
                        commands.fields[1]['input']=f"Succsess!"
                    except Exception as EEEEEEEEEEEEEEEeee:
                        commands.fields[1]['input']=f"ERROR: s{EEEEEEEEEEEEEEEeee}"
                    commands.deActivateField(1)
                    savelevel()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and modes=='decal':
                f=input('decal name? ')
                gp=list(pygame.mouse.get_pos())
                POS=[(gp[0]-cameraposition[0])//SNAP*SNAP,(gp[1]-cameraposition[1])//SNAP*SNAP]
                decals.append([f,POS,255])
                textures.clear()
                ImageInit()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and (modes=='hitbox' or modes=="leveltrigger"):
                gp=list(pygame.mouse.get_pos())
                mc.append([(gp[0]-cameraposition[0])//SNAP*SNAP,(gp[1]-cameraposition[1])//SNAP*SNAP])
                print(mc)
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                remove=True
            if event.type == pygame.KEYDOWN and event.key==105 and not commands.fields[1]['active']:
                modesforcounter=(modesforcounter+1)%len(modesforreal)
                modes=modesforreal[modesforcounter]
                print(modes,", MODENAME")

            

            if event.type == pygame.MOUSEBUTTONDOWN and commands.fields[1]["field"].collidepoint(event.pos)  :
                commands.fields[1]['input']=f""
                print('something happened')
                commands.setActiveField(1)
                
                mc=[]


            #if event.type == pygame.MOUSEBUTTONDOWN and commands.fields[1]['active'] and commands.fields[1]["field"].collidepoint(event.pos)  :
            #    commands.fields[1]['input']=f""
            #    commands.deActivateField(1)

            
            
            

        else: #tODO: GAME LOGIK
            pass
    
    cameraposition=[-debilcoords[0]+320-debilsize[0],-debilcoords[1]+240-debilsize[1]]
    camsomewhere.append(cameraposition)
    if len(camsomewhere)>60:
        del camsomewhere[0]
    sumcamx=0
    sumcamy=0
    for m in camsomewhere:
        sumcamx+=m[0]
    for m in camsomewhere:
        sumcamy+=m[1]
    cameraposition=[sumcamx/60,sumcamy/60]
    if debugCheckWallsOnLeft() and holdingKeyLeft:
        debilspid[0]=-5
    elif debugCheckWallsOnRight() and holdingKeyRight:
        debilspid[0]=5
    else:
        debilspid[0]=0
    if creatorMode:
        if len(mc)==2:
            if modes=='leveltrigger':
                scanx=mc[0][0]
                scany=mc[0][1]
                scanw=abs(mc[1][0]-mc[0][0])
                scanh=abs(mc[1][1]-mc[0][1])
                h=input("rederict to map? ")
                levelplatformo.append([pygame.Rect([scanx,scany],[scanw,scanh]),h])
                print('trigger plac')
                for j in levelplatformo:
                    if j.w==0 and j.h==0 or\
                    j.w==0 or  j.h==0:
                        print("null hitbox, deleting")
                        platformo.remove(j)
                savelevel()
            elif modes=='hitbox':
                scanx=mc[0][0]
                scany=mc[0][1]
                scanw=abs(mc[1][0]-mc[0][0])
                scanh=abs(mc[1][1]-mc[0][1])
                platformo.append(pygame.Rect([scanx,scany],[scanw,scanh]))
                print('platform plac')
                for j in platformo:
                    if j.w==0 and j.h==0 or\
                    j.w==0 or  j.h==0:
                        print("null hitbox, deleting")
                        platformo.remove(j)
                savelevel()
        if len(mc)==1:
            scanx=mc[0][0]
            scany=mc[0][1]
            k=pygame.mouse.get_pos()
            scanw=abs(k[0]-mc[0][0]-cameraposition[0])
            scanh=abs(k[1]-mc[0][1]-cameraposition[1])
            pygame.draw.rect(screen,(64,64,64),pygame.Rect((scanx//SNAP*SNAP+cameraposition[0]),(scany//SNAP*SNAP+cameraposition[1]),scanw//SNAP*SNAP,scanh//SNAP*SNAP))
    
    debilcoords[0]+=debilspid[0]
    debilcoords[1]+=debilspid[1]
    if not floorcheck(): debilspid[1]+=g/10


    pygame.draw.rect(screen,(255,255,255),pygame.Rect([debilcoords[0]+cameraposition[0],debilcoords[1]+cameraposition[1]]
            ,debilsize))
    a=clock.get_fps()
    if creatorMode:
        
        displaytext(f'Affecting filter: {modes}',[400,0])

        displaytext(f'camera pos   : {list(map(round,cameraposition))}',[0,0])
        displaytext(f'snap         : {SNAP}',[0,FONT_SIZE])
        displaytext(f'FPS          : {round(a)}',[0,FONT_SIZE*2])
        displaytext(f'target FPS   : {round(FPS)}',[0,FONT_SIZE*3])
        #displaytext(f'del dec/hitb : {"deleting decals|textures"*removeDecals+"deleting hitboxes"*(1-removeDecals)}',[0,FONT_SIZE*4])
        displaytext(f'player pos   : {list(map(round,debilcoords))}',[0,FONT_SIZE*4])
        displaytext(f'decals num   : {len(decals)}',[0,FONT_SIZE*5])
        displaytext(f'textures num : {len(textures)}',[0,FONT_SIZE*6])
        displaytext(f'disp.tex.num : {k}',[0,FONT_SIZE*7])
        displaytext(f'tex==dec?    : {len(decals)==len(textures)}',[0,FONT_SIZE*8])
        displaytext(f'debugRectInfo: {debugRectInfo}',[0,FONT_SIZE*9])
        displaytext(f'debugTexInfo : {debugTexInfo}',[0,FONT_SIZE*10])
        displaytext(f'global m.pos : {list(map(round,getGlobalMouseCoords(False)))}',[0,FONT_SIZE*11])
        displaytext(f'map version  : {strv}',[0,FONT_SIZE*12])
        displaytext(f'map name     : "{fi}"',[0,FONT_SIZE*13])

        displaytext(f'--------------',[0,FONT_SIZE*14])
        displaytext(f'debug mode. to turn it off, press f12',[0,FONT_SIZE*15])


        displaytext(f'author: "{author}"',[0,550-FONT_SIZE])
        displaytext(f'description: "{description}"',[400,550-FONT_SIZE])

        commands.displayField(1,(200,200,200))
        
        debugRectInfo=[]
        debugTexInfo=[]

        
    gp=list(pygame.mouse.get_pos())
    POS=[(gp[0]-cameraposition[0])//SNAP*SNAP,(gp[1]-cameraposition[1])//SNAP*SNAP]
    POS[0]+=cameraposition[0]
    POS[1]+=cameraposition[1]

    if creatorMode: screen.blit(cursor,POS)
    ksc=screen.convert_alpha()
    ksc.set_alpha(5)

    ksc.blit(screen,pygame.Rect(0,0,ksc.get_rect().w,ksc.get_rect().h))
    
        
    pygame.display.flip()
    

    #print(debilspid)
    

    #print(f'FPS: {a}')
    clock.tick(FPS)
