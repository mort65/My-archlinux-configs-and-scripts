#!/usr/bin/env python3
import os
import random
ImagesArray=[]
home_Dir=os.path.expanduser('~')
Wallpapers_Dir=home_Dir+'/.i3wm-Wallpapers_Dir'
clrCommand = '/usr/bin/rm -rf \'{}\'/*'.format(Wallpapers_Dir)
pictures_Dir=home_Dir+'/Pictures/Desktop/'
for root, directories, filenames in os.walk(pictures_Dir):
        for filename in filenames:
            if filename.lower().endswith(('.jpg')):
                ImagesArray.append(os.path.join(root,filename))
rnd=0
image=''
cpCommand=''
extension=''
os.system(clrCommand)
randlist=random.sample(range(len(ImagesArray)), 10)

for i in range(1,11):
    rnd=randlist[i-1]
    image=ImagesArray[rnd]
    extension=os.path.splitext(image)[1].lower()
    cpCommand='/usr/bin/cp -f \'{}\' \'{}\''.format(image,'{}/{}{}'.format(Wallpapers_Dir,str(i),extension))
    os.system(cpCommand)
