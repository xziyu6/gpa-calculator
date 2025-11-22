import pandas as pd
import tkinter as tk
from tkinter import filedialog

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

#use file dialog to get path
def getFile():
    path=tk.filedialog.askopenfilename(initialdir=".\\",
                                       title="Select an Excel file",
                                       filetypes=(("Microsoft Excel","*.xlsx"),
                                                  ("all files","*.*")))
    return path

#change entry contents
def changeEty(info):
    lst=[]
    for i in range(len(widgetGroup.columns)):
        if widgetGroup.columns[i][-3:]=="Ety":
            lst.append(i)
    for i in range(len(widgetGroup.index)):
        for j in range(len(lst)):
            widgetGroup.iloc[i,lst[j]].delete(0,len(widgetGroup.iloc[i,lst[j]].get()))
            widgetGroup.iloc[i,lst[j]].insert(0,info.iloc[i,j])

#respond to fileBtn, change the entries
def fileCom():
    path=getFile()
    pathLbl.config(text="File opened: "+path)
    info=pd.read_excel(path,index_col=0)
    changeEty(info)

#calculate GPA
def calculate(info):
    #standardize level and score,calculate subject GPA
    gpa=[]
    for i in sbjList:
        info.loc[i,"level"]=stdLv(info.loc[i,"level"])
        info.loc[i,"score"]=stdScr(int(info.loc[i,"score"]))
        gpa.append(findGpa(i,info.loc[i,"level"],info.loc[i,"score"]))
    
    info.loc[:,"gpa"]=gpa      #input gpa into info dataframe
    
    #final result
    gpaSum=0
    creditSum=0
    for i in sbjList:
        info.loc[i,"credit"]=float(info.loc[i,"credit"])
        gpaSum+=info.loc[i,"gpa"]*info.loc[i,"credit"]
        creditSum+=info.loc[i,"credit"]
    
    gpa=gpaSum/creditSum
    gpa=int(gpa*1000)/1000
    return gpa

def getInput():
    info=pd.DataFrame({},index=sbjList,columns=["level","score","credit"])
    lst=[]
    for i in range(len(widgetGroup.columns)):
        if widgetGroup.columns[i][-3:]=="Ety":
            lst.append(i)
    for i in range(len(widgetGroup.index)):
        for j in range(len(lst)):
            info.iloc[i,j]=widgetGroup.iloc[i,lst[j]].get()
    return info

#respond to calcBtn, calculate and output GPA
def calcCom():
    info=getInput()
    gpa=calculate(info)
    outLbl.config(text="Your GPA: "+str(gpa))
    
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

#list of subject names
sbjList=['Chinese', 'Math', 'English', 'History', 'Physics', 'Chemistry', 'Elective']

#create and customize window
root=tk.Tk()
root.geometry("700x250")
root.title("GPA calculator")

#info entries
widgetGroup=pd.DataFrame({},index=sbjList,columns=["sbjLbl","levelEty","scoreEty","creditEty","levelLbl","scoreLbl","creditLbl"])
for i in range(7):
    widgetGroup.loc[sbjList[i],"sbjLbl"]=tk.Label(text=sbjList[i]+": ")
    widgetGroup.loc[sbjList[i],"levelEty"]=tk.Entry(root)
    widgetGroup.loc[sbjList[i],"scoreEty"]=tk.Entry(root)
    widgetGroup.loc[sbjList[i],"creditEty"]=tk.Entry(root)

    widgetGroup.loc[sbjList[i],"levelLbl"]=tk.Label(text="level: ")
    widgetGroup.loc[sbjList[i],"scoreLbl"]=tk.Label(text="score: ")
    widgetGroup.loc[sbjList[i],"creditLbl"]=tk.Label(text="credit: ")

    widgetGroup.loc[sbjList[i],"sbjLbl"].grid(row=i,column=0)
    widgetGroup.loc[sbjList[i],"levelLbl"].grid(row=i,column=1,padx=5)
    widgetGroup.loc[sbjList[i],"levelEty"].grid(row=i,column=2)
    widgetGroup.loc[sbjList[i],"scoreLbl"].grid(row=i,column=3,padx=5)
    widgetGroup.loc[sbjList[i],"scoreEty"].grid(row=i,column=4)
    widgetGroup.loc[sbjList[i],"creditLbl"].grid(row=i,column=5,padx=5)
    widgetGroup.loc[sbjList[i],"creditEty"].grid(row=i,column=6)

#button to choose input file
fileBtn=tk.Button(text="Browse files",command=fileCom)
fileBtn.grid(row=7,column=0,columnspan=2)

#show current input file
pathLbl=tk.Label(text="")
pathLbl.grid(row=7,column=2,columnspan=10,sticky="w")

#calculate button
calcBtn=tk.Button(text="calculate",command=calcCom)
calcBtn.grid(row=8,column=0)
root.bind("<Return>",lambda event:calcCom())

#output
outLbl=tk.Label(text="Your GPA:")
outLbl.grid(row=8,column=2,sticky="w")

root.mainloop()
