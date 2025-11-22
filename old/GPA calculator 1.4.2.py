import pandas as pd

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

#subject GPA dictionaries
chineseGpa=pd.DataFrame({"H":{1:4.3, 2:4.0, 3:3.7, 4:3.4, 5:3.1, 6:2.8, 7:2.4, 8:0},
                         "S":{1:4.2, 2:3.9, 3:3.6, 4:3.3, 5:3.0, 6:2.7, 7:2.3, 8:0},
                         "III":{1:4.1, 2:3.8, 3:3.5, 4:3.2, 5:2.9, 6:2.6, 7:2.2, 8:0},
                         "I":{1:4.0, 2:3.7, 3:3.4, 4:3.1, 5:2.8, 6:2.5, 7:2.1, 8:0}})

englishGpa=pd.DataFrame({"H+":{1:4.4, 2:4.1, 3:3.8, 4:3.5, 5:3.2, 6:2.9, 7:2.5, 8:0},
                         "H":{1:4.3, 2:4.0, 3:3.7, 4:3.4, 5:3.1, 6:2.8, 7:2.4, 8:0},
                         "S+":{1:4.1, 2:3.8, 3:3.5, 4:3.2, 5:2.9, 6:2.6, 7:2.2, 8:0},
                         "S":{1:4.0, 2:3.7, 3:3.4, 4:3.1, 5:2.8, 6:2.5, 7:2.1, 8:0}})

nonLanguageGpa=pd.DataFrame({"H":{1:4.3, 2:4.0, 3:3.7, 4:3.4, 5:3.1, 6:2.8, 7:2.4, 8:0},
                             "S+":{1:4.15, 2:3.85, 3:3.55, 4:3.25, 5:2.95, 6:2.65, 7:2.25, 8:0},
                             "S":{1:4.0, 2:3.7, 3:3.4, 4:3.1, 5:2.8, 6:2.5, 7:2.1, 8:0}})

#read info file
info=pd.read_excel("GPA info.xlsx",index_col=0)

gpa=[]      #create gpa list

#standardize level and score
for i in info.index:
    info.loc[i,"level"]=stdLv(info.loc[i,"level"])
    info.loc[i,"score"]=stdScr(info.loc[i,"score"])
    gpa.append(findGpa(i,info.loc[i,"level"],info.loc[i,"score"]))

info.loc[:,"gpa"]=gpa      #input gpa into info dataframe

#final result
gpaSum=0
creditSum=0
for i in info.index:
    gpaSum+=info.loc[i,"gpa"]*info.loc[i,"credit"]
    creditSum+=info.loc[i,"credit"]

gpa=gpaSum/creditSum
gpa=int(gpa*1000)/1000
print("Your GPA: "+str(gpa))

#put GPA in file
file=open("GPA result.txt","w")
file.write("GPA: "+str(gpa))
file.close()
