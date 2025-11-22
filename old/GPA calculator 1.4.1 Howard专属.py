#function to input and standardize score
def stdScr(scr):
    if scr>=93:
        return 1
    elif scr>=88:
        return 2
    elif scr>=83:
        return 3
    elif scr>=78:
        return 4
    elif scr>=73:
        return 5
    elif scr>=68:
        return 6
    elif scr>=60:
        return 7
    else:
        return 8

#find subject GPA in dictionary
def findGpa(sbj,lv,scr):
    if sbj=="chinese":
        return chineseGpa[scr]
    elif sbj=="english":
        return englishGpa[scr]
    else:
        return nonLanguageGpa[lv][scr]
    
#create subject dictionaries and list
level={"chinese":"S","math":"S+","english":"H","history":"S+","physics":"S","chemistry":"S+","elective":"H"}
score={}
classTime={}
gpa={}
sbjList=["chinese","math","english","history","physics","chemistry","elective"]

#subject GPA dictionaries
chineseGpa={1:4.2,2:3.9,3:3.6,4:3.3,5:3.0,6:2.7,7:2.3,8:0}

englishGpa={1:4.3,2:4.0,3:3.7,4:3.4,5:3.1,6:2.8,7:2.4,8:0}

nonLanguageGpa={"H":{1:4.3,2:4.0,3:3.7,4:3.4,5:3.1,6:2.8,7:2.4,8:0},
             "S+":{1:4.15,2:3.85,3:3.55,4:3.25,5:2.95,6:2.65,7:2.25,8:0},
             "S":{1:4.0,2:3.7,3:3.4,4:3.1,5:2.8,6:2.5,7:2.1,8:0}}

#read info file
file=open("GPA info Howard 专属.txt","r")
info=file.readlines()
file.close()
for sbjNum in range(7):
    info[sbjNum]=info[sbjNum].split("\t")
    if info[sbjNum][2]=="":
        del info[sbjNum][2]
    for infoNum in range(3):
        if infoNum==2:
            info[sbjNum][infoNum]=info[sbjNum][infoNum].split()[2]
        else:
            info[sbjNum][infoNum]=info[sbjNum][infoNum].split()[1]

#input info into dictionary
for i in range(len(sbjList)):
    score[sbjList[i]],classTime[sbjList[i]]=int(info[i][1]),float(info[i][2])

#standardize score
for i in range(len(sbjList)):
    score[sbjList[i]]=stdScr(score[sbjList[i]])

#find GPA for each subject
for i in range(len(sbjList)):
    gpa[sbjList[i]]=findGpa(sbjList[i],level[sbjList[i]],score[sbjList[i]])

#final result
gpaSum=0
classTimeSum=0
for i in range(len(sbjList)):
    gpaSum+=gpa[sbjList[i]]*classTime[sbjList[i]]
for i in range(len(sbjList)):
    classTimeSum+=classTime[sbjList[i]]
gpa=gpaSum/classTimeSum
gpa=int(gpa*1000)/1000
print("Your GPA: "+str(gpa))

#put GPA in file
file=open("GPA result Howard 专属.txt","w")
file.write("GPA: "+str(gpa))
file.close()
