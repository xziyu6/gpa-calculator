#function to input and standardize score
def stdScr(sbj,scr):
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

#function to input and standardize level
def stdLv(sbj,lv):
    if lv=="HLM" or lv=="素养班":
        return "H"
    if lv=="II":
        lv="I"
    elif lv=="IV":
        lv="III"
    elif lv=="V" or lv=="VI" or lv=="VII":
        lv="S"
    return lv.upper()

#create subject dictionaries
chinese={}
math={}
english={}
history={}
physics={}
chemistry={}
elective={}

#subject GPA dictionaries
chineseGPA={"H":{1:4.3,2:4.0,3:3.7,4:3.4,5:3.1,6:2.8,7:2.4,8:0},
         "S":{1:4.2,2:3.9,3:3.6,4:3.3,5:3.0,6:2.7,7:2.3,8:0},
         "III":{1:4.1,2:3.8,3:3.5,4:3.2,5:2.9,6:2.6,7:2.2,8:0},
         "I":{1:4.0,2:3.7,3:3.4,4:3.1,5:2.8,6:2.5,7:2.1,8:0}}

englishGPA={"H+":{1:4.4,2:4.1,3:3.8,4:3.5,5:3.2,6:2.9,7:2.5,8:0},
         "H":{1:4.3,2:4.0,3:3.7,4:3.4,5:3.1,6:2.8,7:2.4,8:0},
         "S+":{1:4.1,2:3.8,3:3.5,4:3.2,5:2.9,6:2.6,7:2.2,8:0},
         "S":{1:4.0,2:3.7,3:3.4,4:3.1,5:2.8,6:2.5,7:2.1,8:0}}

nonLanguageGPA={"H":{1:4.3,2:4.0,3:3.7,4:3.4,5:3.1,6:2.8,7:2.4,8:0},
             "S+":{1:4.15,2:3.85,3:3.55,4:3.25,5:2.95,6:2.65,7:2.25,8:0},
             "S":{1:4.0,2:3.7,3:3.4,4:3.1,5:2.8,6:2.5,7:2.1,8:0}}

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

#standardize score
chinese["score"]=stdScr("Chinese",chinese["score"])
math["score"]=stdScr("Math",math["score"])
english["score"]=stdScr("English",english["score"])
history["score"]=stdScr("History",history["score"])
physics["score"]=stdScr("Physics",physics["score"])
chemistry["score"]=stdScr("Chemistry",chemistry["score"])
elective["score"]=stdScr("Elective",elective["score"])

#find GPA for each subject
chinese["gpa"]=chineseGPA[chinese["level"]][chinese["score"]]
math["gpa"]=nonLanguageGPA[math["level"]][math["score"]]
english["gpa"]=englishGPA[english["level"]][english["score"]]
history["gpa"]=nonLanguageGPA[history["level"]][history["score"]]
physics["gpa"]=nonLanguageGPA[physics["level"]][physics["score"]]
chemistry["gpa"]=nonLanguageGPA[chemistry["level"]][chemistry["score"]]
elective["gpa"]=nonLanguageGPA[elective["level"]][elective["score"]]

#final result
gpa=chinese["gpa"]*chinese["classTime"]+math["gpa"]*math["classTime"]+english["gpa"]*english["classTime"]+history["gpa"]*history["classTime"]+physics["gpa"]*physics["classTime"]+chemistry["gpa"]*chemistry["classTime"]+elective["gpa"]*elective["classTime"]
gpa=gpa/(chinese["classTime"]+math["classTime"]+english["classTime"]+history["classTime"]+physics["classTime"]+chemistry["classTime"]+elective["classTime"])
gpa=int(gpa*1000)/1000
print("Your GPA: "+str(gpa))

#put GPA in file
file=open("GPA result.txt","w")
file.write("GPA: "+str(gpa))
file.close()
