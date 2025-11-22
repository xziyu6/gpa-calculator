#function to input and standardize score
def stdScr(scr):
    if scr>=92.5:
        return 1
    elif scr>=87.5:
        return 2
    elif scr>=82.5:
        return 3
    elif scr>=77.5:
        return 4
    elif scr>=72.5:
        return 5
    elif scr>=67.5:
        return 6
    elif scr>=59.5:
        return 7
    else:
        return 8

#function to input and standardize level
def stdLv(lv):
    if lv=="HLM" or lv=="素养班":
        return "H"
    if lv=="II":
        lv="I"
    elif lv=="IV":
        lv="III"
    elif lv=="V" or lv=="VI" or lv=="VII":
        lv="S"
    return lv.upper()

#find subject GPA in dictionary
def findGpa(sbj,lv,scr):
    if sbj=="Chinese":
        return chineseGpa[lv][scr]
    elif sbj=="English":
        return englishGpa[lv][scr]
    else:
        return nonLanguageGpa[lv][scr]
    
#create subject dictionaries and list
level={}
score={}
credit={}
gpa={}
sbjList=[]

#subject GPA dictionaries
chineseGpa={"H":{1:4.3, 2:4.0, 3:3.7, 4:3.4, 5:3.1, 6:2.8, 7:2.4, 8:0},
         "S":{1:4.2, 2:3.9, 3:3.6, 4:3.3, 5:3.0, 6:2.7, 7:2.3, 8:0},
         "III":{1:4.1, 2:3.8, 3:3.5, 4:3.2, 5:2.9, 6:2.6, 7:2.2, 8:0},
         "I":{1:4.0, 2:3.7, 3:3.4, 4:3.1, 5:2.8, 6:2.5, 7:2.1, 8:0}}

englishGpa={"H+":{1:4.4, 2:4.1, 3:3.8, 4:3.5, 5:3.2, 6:2.9, 7:2.5, 8:0},
         "H":{1:4.3, 2:4.0, 3:3.7, 4:3.4, 5:3.1, 6:2.8, 7:2.4, 8:0},
         "S+":{1:4.1, 2:3.8, 3:3.5, 4:3.2, 5:2.9, 6:2.6, 7:2.2, 8:0},
         "S":{1:4.0, 2:3.7, 3:3.4, 4:3.1, 5:2.8, 6:2.5, 7:2.1, 8:0}}

nonLanguageGpa={"H":{1:4.3, 2:4.0, 3:3.7, 4:3.4, 5:3.1, 6:2.8, 7:2.4, 8:0},
             "S+":{1:4.15, 2:3.85, 3:3.55, 4:3.25, 5:2.95, 6:2.65, 7:2.25, 8:0},
             "S":{1:4.0, 2:3.7, 3:3.4, 4:3.1, 5:2.8, 6:2.5, 7:2.1, 8:0}}

#read info file
file=open("GPA info.txt","r")
info=file.readlines()
file.close()
for sbjNum in range(7):
    info[sbjNum]=info[sbjNum].split("\t")
    if info[sbjNum][3]=="":
        del info[sbjNum][3]
    for infoNum in range(4):
        info[sbjNum][infoNum]=info[sbjNum][infoNum].split()[1]

#input info into dictionary
for i in range(len(info)):
    sbjList.append(info[i][0])
    level[sbjList[i]],score[sbjList[i]],credit[sbjList[i]]=info[i][1],float(info[i][2]),float(info[i][3])

#standardize level
for i in range(len(sbjList)):
    level[sbjList[i]]=stdLv(level[sbjList[i]])

#standardize score
for i in range(len(sbjList)):
    score[sbjList[i]]=stdScr(score[sbjList[i]])

#find GPA for each subject
for i in range(len(sbjList)):
    gpa[sbjList[i]]=findGpa(sbjList[i],level[sbjList[i]],score[sbjList[i]])

#final result
gpaSum=0
creditSum=0
for i in range(len(sbjList)):
    gpaSum+=gpa[sbjList[i]]*credit[sbjList[i]]
for i in range(len(sbjList)):
    creditSum+=credit[sbjList[i]]
gpa=gpaSum/creditSum
gpa=int(gpa*1000)/1000
print("Your GPA: "+str(gpa))

#put GPA in file
file=open("GPA result.txt","w")
file.write("GPA: "+str(gpa))
file.close()
