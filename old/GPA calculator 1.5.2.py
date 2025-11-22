import pandas as pd
import tkinter as tk
import numpy as np
from tkinter import filedialog
import time


def standardize_score(scr):
    if scr >= 92.5:
        return 1
    elif scr >= 87.5:
        return 2
    elif scr >= 82.5:
        return 3
    elif scr >= 77.5:
        return 4
    elif scr >= 72.5:
        return 5
    elif scr >= 67.5:
        return 6
    elif scr >= 59.5:
        return 7
    else:
        return 8


def standardize_level(lv):
    if lv == "HLM" or lv == "素养班":
        return "H"
    if lv == "II":
        lv = "I"
    elif lv == "IV":
        lv = "III"
    elif lv == "V" or lv == "VI" or lv == "VII":
        lv = "S"
    return lv.upper()


def find_gpa(sbj, lv, scr):
    if sbj == "Chinese":
        return chineseGpa[lv][scr]
    elif sbj == "English":
        return englishGpa[lv][scr]
    else:
        return nonLanguageGpa[lv][scr]


def open_input_file():
    path = tk.filedialog.askopenfilename(initialfile='GPA info.xlsx',
                                         title="Select an Excel file",
                                         filetypes=(("Microsoft Excel", "*.xlsx"),
                                                    ("all files", "*.*")),
                                         defaultextension='.xlsx')
    pathLbl.config(text="File opened: " + path)
    # noinspection PyArgumentList
    info = pd.read_excel(path, index_col=0)
    for sbj in sbj_list:
        for attrs in attrs_list:
            attrs_entry_group.loc[sbj, attrs].delete(0, len(attrs_entry_group.loc[sbj, attrs].get()))
            attrs_entry_group.loc[sbj, attrs].insert(0, info.loc[sbj, attrs])


def calculate_gpa(info):
    for sbj in sbj_list:
        info.loc[sbj, "level"] = standardize_level(info.loc[sbj, "level"])
        info.loc[sbj, "score"] = standardize_score(int(info.loc[sbj, "score"]))
        info.loc[sbj, "gpa"] = find_gpa(sbj, info.loc[sbj, "level"], info.loc[sbj, "score"])
        info.loc[sbj, "credit"] = float(info.loc[sbj, "credit"])

    gpa_sum = np.sum(np.array(info["gpa"]) * np.array(info["credit"]))
    credit_sum = np.sum(info["credit"])

    return np.round(gpa_sum / credit_sum, 3)


def get_input():
    info = pd.DataFrame({}, index=sbj_list, columns=attrs_list + ['gpa'])
    for sbj in sbj_list:
        for attrs in attrs_list:
            info.loc[sbj, attrs] = attrs_entry_group.loc[sbj, attrs].get()
    return info


def calculate_gpa_command():
    info = get_input()
    gpa = calculate_gpa(info)
    output_label.config(text="Your GPA: " + str(gpa))


def save_input_command():
    info = get_input().loc[:, :'credit']
    path = tk.filedialog.asksaveasfilename(title="Save as Excel file",
                                           filetypes=(("Microsoft Excel", "*.xlsx"),
                                                      ("all files", "*.*")),
                                           defaultextension='.xlsx')
    info.to_excel(path)


def save_gpa_command():
    gpa = output_label["text"].split(": ")[1]
    fout = open("GPA output.txt", "a")
    t = time.strftime("%Y-%m-%d")
    fout.write(t + " GPA: " + gpa + "\n")
    fout.close()


chineseGpa = pd.DataFrame({"H": {1: 4.3, 2: 4.0, 3: 3.7, 4: 3.4, 5: 3.1, 6: 2.8, 7: 2.4, 8: 0},
                           "S": {1: 4.2, 2: 3.9, 3: 3.6, 4: 3.3, 5: 3.0, 6: 2.7, 7: 2.3, 8: 0},
                           "III": {1: 4.1, 2: 3.8, 3: 3.5, 4: 3.2, 5: 2.9, 6: 2.6, 7: 2.2, 8: 0},
                           "I": {1: 4.0, 2: 3.7, 3: 3.4, 4: 3.1, 5: 2.8, 6: 2.5, 7: 2.1, 8: 0}})

englishGpa = pd.DataFrame({"H+": {1: 4.4, 2: 4.1, 3: 3.8, 4: 3.5, 5: 3.2, 6: 2.9, 7: 2.5, 8: 0},
                           "H": {1: 4.3, 2: 4.0, 3: 3.7, 4: 3.4, 5: 3.1, 6: 2.8, 7: 2.4, 8: 0},
                           "S+": {1: 4.1, 2: 3.8, 3: 3.5, 4: 3.2, 5: 2.9, 6: 2.6, 7: 2.2, 8: 0},
                           "S": {1: 4.0, 2: 3.7, 3: 3.4, 4: 3.1, 5: 2.8, 6: 2.5, 7: 2.1, 8: 0}})

nonLanguageGpa = pd.DataFrame({"H": {1: 4.3, 2: 4.0, 3: 3.7, 4: 3.4, 5: 3.1, 6: 2.8, 7: 2.4, 8: 0},
                               "S+": {1: 4.15, 2: 3.85, 3: 3.55, 4: 3.25, 5: 2.95, 6: 2.65, 7: 2.25, 8: 0},
                               "S": {1: 4.0, 2: 3.7, 3: 3.4, 4: 3.1, 5: 2.8, 6: 2.5, 7: 2.1, 8: 0}})

sbj_list = ['Chinese', 'Math', 'English', 'History', 'Physics', 'Chemistry', 'Elective']
attrs_list = ["level", "score", "credit"]

root = tk.Tk()
root.geometry("700x300")
root.title("GPA calculator")

sbj_label_group = {}
attrs_entry_group = pd.DataFrame({}, index=sbj_list,
                                 columns=attrs_list)
attrs_label_group = pd.DataFrame({}, index=sbj_list,
                                 columns=attrs_list)
for i in range(len(sbj_list)):
    sbj_label_group[sbj_list[i]] = tk.Label(text=sbj_list[i] + ": ")
    sbj_label_group[sbj_list[i]].grid(row=i, column=0)
    for j in range(len(attrs_list)):
        attrs_label_group.loc[sbj_list[i], attrs_list[j]] = tk.Label(root, text=attrs_list[j] + ': ')
        attrs_label_group.loc[sbj_list[i], attrs_list[j]].grid(row=i, column=2 * j + 1, padx=5)
        attrs_entry_group.loc[sbj_list[i], attrs_list[j]] = tk.Entry(root)
        attrs_entry_group.loc[sbj_list[i], attrs_list[j]].grid(row=i, column=2 * j + 2)

fileBtn = tk.Button(text="Browse files", command=open_input_file)
fileBtn.grid(row=7, column=0, columnspan=2)

pathLbl = tk.Label(text="File opened: ")
pathLbl.grid(row=7, column=2, columnspan=10, sticky="w")

calcBtn = tk.Button(text="calculate", command=calculate_gpa_command)
calcBtn.grid(row=8, column=0, columnspan=2, pady=2)
root.bind("<Return>", lambda event: calculate_gpa_command())

output_label = tk.Label(text="Your GPA:")
output_label.grid(row=8, column=2, sticky="w")

save_input_button = tk.Button(text="Save input", command=save_input_command)
save_input_button.grid(row=9, column=2, columnspan=2, pady=2)

save_gpa_button = tk.Button(text="Save GPA", command=save_gpa_command)
save_gpa_button.grid(row=9, column=4, columnspan=2, pady=2)

root.mainloop()
