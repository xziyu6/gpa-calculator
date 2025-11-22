#function to input and standardize score
def stdScr(sbj,scr):
    while not str(scr).isdigit():
        scr=input("Please enter "+sbj+" score again:")
    scr=float(scr)
    if scr>=93:
        scr=0
    elif scr>=88:
        scr=-1
    elif scr>=83:
        scr=-2
    elif scr>=78:
        scr=-3
    elif scr>=73:
        scr=-4
    elif scr>=68:
        scr=-5
    elif scr>=60:
        scr=-6
    else:
        scr=-7
    return scr

#function to input and standardize level
def stdLv(sbj,lv):
    if lv=="HLM" or lv=="hlm" or lv=="素养班" or lv=="素养":
        return "H"
    return lv.upper()

#function to standardize level
def digitLv(lv):
    if lv=="S":
        return 0
    elif lv=="S+":
        return 1
    elif lv=="H":
        return 2
    
#calculate subject GPA
def sbjGpa(sbj,score,level):
    if sbj=="Chinese" or sbj=="English":
        if score==-7:
            return 0
        elif score==-6:
            return 3.9+0.1*level+0.3*score
        else:
            return 4+0.1*level+0.3*score
    else:
        if score==-7:
            return 0
        elif score==-6:
            return 3.9+0.15*level+0.3*score
        else:
            return 4+0.15*level+0.3*score

#create dictionaries
chinese={}
math={}
english={}
history={}
physics={}
chemistry={}
elective={}

#read info file
file=open("GPA info.txt","r")
info=file.readlines()
file.close()
for sbjNum in range(7):
    info[sbjNum]=info[sbjNum].split("\t")
    if info[sbjNum][3]=="":
        del info[sbjNum][3]
    for infoNum in range(4):
        if infoNum==3:
            info[sbjNum][infoNum]=info[sbjNum][infoNum].split()[2]
        else:
            info[sbjNum][infoNum]=info[sbjNum][infoNum].split()[1]

#input info into dictionary
chinese["level"],chinese["score"],chinese["classTime"]=info[0][1],int(info[0][2]),float(info[0][3])
math["level"],math["score"],math["classTime"]=info[1][1],int(info[1][2]),float(info[1][3])
english["level"],english["score"],english["classTime"]=info[2][1],int(info[2][2]),float(info[2][3])
history["level"],history["score"],history["classTime"]=info[3][1],int(info[3][2]),float(info[3][3])
physics["level"],physics["score"],physics["classTime"]=info[4][1],int(info[4][2]),float(info[4][3])
chemistry["level"],chemistry["score"],chemistry["classTime"]=info[5][1],int(info[5][2]),float(info[5][3])
elective["level"],elective["score"],elective["classTime"]=info[6][1],int(info[6][2]),float(info[6][3])

#standardize level
chinese["level"]=stdLv("Chinese",chinese["level"])
math["level"]=stdLv("Math",math["level"])
english["level"]=stdLv("English",english["level"])
history["level"]=stdLv("History",history["level"])
physics["level"]=stdLv("Physics",physics["level"])
chemistry["level"]=stdLv("Chemistry",chemistry["level"])
elective["level"]=stdLv("Elective",elective["level"])

#digitalize level
if chinese["level"]=="I" or chinese["level"]=="II":
    chinese["level"]=0
elif chinese["level"]=="III" or chinese["level"]=="IV":
    chinese["level"]=1
elif chinese["level"]=="V" or chinese["level"]=="VI" or chinese["level"]=="VII" or chinese["level"]=="S":
    chinese["level"]=2
elif chinese["level"]=="H":
    chinese["level"]=3

if english["level"]=="S":
    english["level"]=0
elif english["level"]=="S+":
    english["level"]=1
elif english["level"]=="H":
    english["level"]=3
elif english["level"]=="H+":
    chinese["level"]=4

math["level"]=digitLv(math["level"])
history["level"]=digitLv(history["level"])
physics["level"]=digitLv(physics["level"])
chemistry["level"]=digitLv(chemistry["level"])
elective["level"]=digitLv(elective["level"])
              
#standardize score
chinese["score"]=stdScr("Chinese",chinese["score"])
math["score"]=stdScr("Math",math["score"])
english["score"]=stdScr("English",english["score"])
history["score"]=stdScr("History",history["score"])
physics["score"]=stdScr("Physics",physics["score"])
chemistry["score"]=stdScr("Chemistry",chemistry["score"])
elective["score"]=stdScr("Elective",elective["score"])

#find GPA for each subject
chinese["gpa"]=sbjGpa("Chinese",chinese["score"],chinese["level"])   
math["gpa"]=sbjGpa("Math",math["score"],math["level"])
english["gpa"]=sbjGpa("English",english["score"],english["level"])
history["gpa"]=sbjGpa("History",history["score"],history["level"])
physics["gpa"]=sbjGpa("Physics",physics["score"],physics["level"])
chemistry["gpa"]=sbjGpa("Chemistry",chemistry["score"],chemistry["level"])
elective["gpa"]=sbjGpa("Elective",elective["score"],elective["level"])

#final result
gpa=chinese["gpa"]*chinese["classTime"]+math["gpa"]*math["classTime"]+english["gpa"]*english["classTime"]+history["gpa"]*history["classTime"]+physics["gpa"]*physics["classTime"]+chemistry["gpa"]*chemistry["classTime"]+elective["gpa"]*elective["classTime"]
gpa=gpa/(chinese["classTime"]+math["classTime"]+english["classTime"]+history["classTime"]+physics["classTime"]+chemistry["classTime"]+elective["classTime"])
gpa=int(gpa*1000)/1000
print("Your GPA: "+str(gpa))

#put GPA in file
file=open("GPA result.txt","w")
file.write("GPA: "+str(gpa))
file.close()
