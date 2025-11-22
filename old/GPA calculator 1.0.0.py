chiScr=int(input("Chinese score:"))
mScr=int(input("Math score:"))
eScr=int(input("English score:"))
hScr=int(input("History score:"))
pScr=int(input("Physics score:"))
cheScr=int(input("Chemistry score:"))
oScr=int(input("IT/Bio/Geo score:"))
chiLv=input("Chinese level:(enter H/S/non-native)")
mLv=input("Math level:(enter HLM/H/S+/S)")
eLv=input("English level:(enter H+/H/S+/S)")
hLv=input("History level:(enter H/S+/S)")
pLv=input("Physics level:(enter H/S+/S)")
cheLv=input("Chemistry level:(enter H/S+/S)")
oLv=input("IT/Bio/Geo level:(enter H/S)")
chiClsTime=3
mClsTime=6
eClsTime=6.5
hClsTime=4
pClsTime=3
cheClsTime=3
oClsTime=2
if chiScr>=93:
    chiScr=-1
elif 88<=chiScr<93:
    chiScr=-2
elif 83<=chiScr<88:
    chiScr=-3
elif 78<=chiScr<83:
    chiScr=-4
elif 73<=chiScr<78:
    chiScr=-5
elif 68<=chiScr<73:
    chiScr=-6
elif 60<=chiScr<68:
    chiScr=-7
else:
    chiScr=-8
if mScr>=93:
    mScr=-1
elif 88<=mScr<93:
    mScr=-2
elif 83<=mScr<88:
    mScr=-3
elif 78<=mScr<83:
    mScr=-4
elif 73<=mScr<78:
    mScr=-5
elif 68<=mScr<73:
    mScr=-6
elif 60<=mScr<68:
    mScr=-7
else:
    mScr=-8
if eScr>=93:
    eScr=-1
elif 88<=eScr<93:
    eScr=-2
elif 83<=eScr<88:
    eScr=-3
elif 78<=eScr<83:
    eScr=-4
elif 73<=eScr<78:
    eScr=-5
elif 68<=eScr<73:
    eScr=-6
elif 60<=eScr<68:
    eScr=-7
else:
    eScr=-8
if hScr>=93:
    hScr=-1
elif 88<=hScr<93:
    hScr=-2
elif 83<=hScr<88:
    hScr=-3
elif 78<=hScr<83:
    hScr=-4
elif 73<=hScr<78:
    hScr=-5
elif 68<=hScr<73:
    hScr=-6
elif 60<=hScr<68:
    hScr=-7
else:
    hScr=-8
if pScr>=93:
    pScr=-1
elif 88<=pScr<93:
    pScr=-2
elif 83<=pScr<88:
    pScr=-3
elif 78<=pScr<83:
    pScr=-4
elif 73<=pScr<78:
    pScr=-5
elif 68<=pScr<73:
    pScr=-6
elif 60<=pScr<68:
    pScr=-7
else:
    pScr=-8
if cheScr>=93:
    cheScr=-1
elif 88<=cheScr<93:
    cheScr=-2
elif 83<=cheScr<88:
    cheScr=-3
elif 78<=cheScr<83:
    cheScr=-4
elif 73<=cheScr<78:
    cheScr=-5
elif 68<=cheScr<73:
    cheScr=-6
elif 60<=cheScr<68:
    cheScr=-7
else:
    cheScr=-8
if oScr>=93:
    oScr=-1
elif 88<=oScr<93:
    oScr=-2
elif 83<=oScr<88:
    oScr=-3
elif 78<=oScr<83:
    oScr=-4
elif 73<=oScr<78:
    oScr=-5
elif 68<=oScr<73:
    oScr=-6
elif 60<=oScr<68:
    oScr=-7
else:
    oScr=-8
if chiLv=="H":
    chiLv=0
else:
    chiLv=-1
if mLv=="H" or mLv=="HLM":
    mLv=0
elif mLv=="S+":
    mLv=-1
else:
    mLv=-2
if eLv=="H+":
    eLv=0
elif eLv=="H":
    eLv=-1
elif eLv=="S+":
    eLv=-2
else:
    eLv=-3
if hLv=="H":
    hLv=0
elif hLv=="S+":
    hLv=-1
else:
    hLv=-2
if pLv=="H":
    pLv=0
elif pLv=="S+":
    pLv=-1
else:
    pLv=-2
if cheLv=="H":
    cheLv=0
elif cheLv=="S+":
    cheLv=-1
else:
    cheLv=-2
if oLv=="H":
    oLv=0
elif oLv=="S":
    oLv=-1
if chiScr==-8:
    chiGpa=0
else:
    chiGpa=4.3+0.1*chiLv+0.3*(chiScr+1)
if mScr==-8:
    mGpa=0
else:
    mGpa=4.3+0.1*mLv+0.3*(mScr+1)
if eScr==-8:
    eGpa=0
else:
    eGpa=4.3+0.1*eLv+0.3*(eScr+1)
if hScr==-8:
    hGpa=0
else:
    hGpa=4.3+0.1*hLv+0.3*(hScr+1)
if pScr==-8:
    pGpa=0
else:
    pGpa=4.3+0.1*pLv+0.3*(pScr+1)
if cheScr==-8:
    cheGpa=0
else:
    cheGpa=4.3+0.1*cheLv+0.3*(cheScr+1)
if oScr==-8:
    oGpa=0
else:
    oGpa=4.3+0.1*oLv+0.3*(oScr+1)
gpa=(chiGpa*chiClsTime+mGpa*mClsTime+eGpa*eClsTime+hGpa*hClsTime+pGpa*pClsTime+cheGpa*cheClsTime+oGpa*oClsTime)/(chiClsTime+mClsTime+eClsTime+hClsTime+pClsTime+cheClsTime+oClsTime)
gpa=int(gpa*1000)/1000
print("Your GPA is: "+str(gpa))
