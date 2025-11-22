# function to input and standardize score
def inputScr(sbj):
    scr=input(sbj+" score:")
    while scr.isdigit()==False:
        scr=input("Please enter again:")
    scr=int(scr)
    if scr>=92.5:
        scr=0
    elif scr>=87.5:
        scr=-1
    elif scr>=82.5:
        scr=-2
    elif scr>=77.5:
        scr=-3
    elif scr>=72.5:
        scr=-4
    elif scr>=67.5:
        scr=-5
    elif scr>=59.5:
        scr=-6
    else:
        scr=-7
    return scr

# function to input and standardize level
def inputLv(sbj):
    lv=input(sbj+" level:")
    if lv=="H+" or lv=="h+":
        lv="H+"
    elif lv=="H" or lv=="h" or lv=="HLM" or lv=="hlm" or lv=="素养班" or lv=="素养":
        lv="H"
    elif lv=="S+" or lv=="s+":
        lv="S+"
    elif lv=="S" or lv=="s" or lv=="non-native" or lv=="nonnative" or lv=="Nonnative" or lv=="Non-native" or lv=="Non-Native":
        lv="S"
    else:
        while lv!="S" and lv!="s" and lv!="S+" and lv!="s+" and lv!="H" and lv!="h" and lv!="素养班" and lv!="素养"and lv!="HLM" and lv!="hlm" and lv!="H+" and lv!="h+" and lv!="non-native" and lv!="nonnative" and lv!="Nonnative" and lv!="Non-native" and lv!="Non-Native":
            lv=input("Please enter again:")
    return lv

#function to standardize level
def stdLv(lv):
    if lv=="H":
        return 0
    elif lv=="S+":
        return -1
    else:
        return -2
    
#calculate subject GPA
def sbjGpa(scr,lv):
    if scr==-7:
        return 0
    else:
        return 4.3+0.15*lv+0.3*scr

#input scores
chiScr=inputScr("Chinese")
mScr=inputScr("Math")
eScr=inputScr("English")
hScr=inputScr("History")
pScr=inputScr("Physics")
cheScr=inputScr("Chemistry")
elScr=inputScr("Elective")

#input levels
chiLv=inputLv("Chinese")
mLv=inputLv("Math")
eLv=inputLv("English")
hLv=inputLv("History")
pLv=inputLv("Physics")
cheLv=inputLv("Chemistry")
elLv=inputLv("Elective")

#class times
chiClsTime=3
mClsTime=6
eClsTime=6.5
hClsTime=4
pClsTime=3
cheClsTime=3
elClsTime=3

#standardize level
if chiLv=="H":
    chiLv=0
else:
    chiLv=-1

if eLv=="H+":
    eLv=1
elif eLv=="H":
    eLv=0
elif eLv=="S+":
    eLv=-1
else:
    eLv=-2

if elLv=="H":
    elLv=0
elif elLv=="S":
    elLv=-1

mLv=stdLv(mLv)
hLv=stdLv(hLv)
pLv=stdLv(pLv)
cheLv=stdLv(cheLv)

#find GPA for each subject
if chiScr==-7:
    chiGpa=0
else:
    chiGpa=4.3+0.1*chiLv+0.3*chiScr
mGpa=sbjGpa(mScr,mLv)
eGpa=sbjGpa(eScr,eLv)
hGpa=sbjGpa(hScr,hLv)
pGpa=sbjGpa(pScr,pLv)
cheGpa=sbjGpa(cheScr,cheLv)
elGpa=sbjGpa(elScr,elLv)

#final result
gpa=(chiGpa*chiClsTime+mGpa*mClsTime+eGpa*eClsTime+hGpa*hClsTime+pGpa*pClsTime+cheGpa*cheClsTime+elGpa*elClsTime)/(chiClsTime+mClsTime+eClsTime+hClsTime+pClsTime+cheClsTime+elClsTime)
gpa=int(gpa*1000)/1000
print("Your GPA is: "+str(gpa))
