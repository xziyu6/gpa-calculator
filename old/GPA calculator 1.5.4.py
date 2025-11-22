import os
import pandas as pd
import tkinter as tk
import numpy as np
from tkinter import filedialog
from tkinter import ttk
import time

# TODO add comments
# TODO extend to multi-grade
# TODO find accurate class credits

class InputError(Exception):
    def __init__(self, position, value):
        self.position = position
        self.value = value

    def __str__(self):
        return "{0} at position {1} is invalid input".format(repr(self.value), str(self.position))


def letter_grade(scr: int | float | str, sbj: str) -> str:
    if 95.5 <= scr <= 100:
        return 'A+'
    elif scr >= 92.5:
        return 'A'
    elif scr >= 87.5:
        return 'A-'
    elif scr >= 82.5:
        return 'B+'
    elif scr >= 77.5:
        return 'B'
    elif scr >= 72.5:
        return 'B-'
    elif scr >= 67.5:
        return 'C+'
    elif scr >= 61.5:
        return 'C'
    elif scr >= 59.5:
        return 'C-'
    elif scr >= 0:
        return 'F'
    elif scr in non_language_gpa_table.index:
        return scr
    else:
        raise InputError(f'{sbj} score', scr)


def check_level(lv: str, sbj: str):
    if sbj == 'Chinese' and lv not in chinese_gpa_table.keys():
        raise InputError('Chinese level', lv)
    elif sbj == 'English' and lv not in english_gpa_table.keys():
        raise InputError('English level', lv)
    elif sbj != 'Chinese' and sbj != 'English' and lv not in non_language_gpa_table.keys():
        raise InputError(sbj + ' level', lv)


def find_subject_gpa(sbj, lv, scr):
    if sbj == 'Chinese':
        return chinese_gpa_table[lv][scr]
    elif sbj == 'English':
        return english_gpa_table[lv][scr]
    else:
        return non_language_gpa_table[lv][scr]


def open_input_file():
    path = filedialog.askopenfilename(title='Select an Excel file',
                                      filetypes=(('Microsoft Excel', '*.xlsx'),
                                                 ('all files', '*.*')),
                                      defaultextension='.xlsx')
    input_filename_label.config(text='File opened: ' + path)
    info = pd.read_excel(path, index_col=0)
    for sbj in subjects:
        for attr in attributes:
            if attr == 'level':
                input_group.loc[sbj, attr].set(info.loc[sbj, attr].upper())
            else:
                input_group.loc[sbj, attr].delete(0, len(input_group.loc[sbj, attr].get()))
                input_group.loc[sbj, attr].insert(0, info.loc[sbj, attr])


def get_input():
    info = pd.DataFrame({}, index=subjects, columns=attributes)

    for sbj in subjects:
        for attr in attributes:
            info.loc[sbj, attr] = input_group.loc[sbj, attr].get()

    return info


def calculate_gpa():
    info = get_input()

    try:
        levels = np.array(info.loc[:, 'level'])
        scores = np.array(info.loc[:, 'score'])
        credit_weights = np.array(info.loc[:, 'credit'])

        for i in range(len(subjects)):
            check_level(levels[i], subjects[i])

        try:
            scores = np.array(scores, dtype=float)
            scores = np.array([letter_grade(scores[i], subjects[i]) for i in range(len(scores))])

        except ValueError:
            position = 0
            for position in range(len(scores)):
                if type(position) is not int and type(position) is not float:
                    continue
            raise InputError(f'{subjects[position]} score', scores[position])

        try:
            credit_weights = np.array(credit_weights, dtype=float)

        except ValueError:
            position = 0
            for position in range(len(scores)):
                if type(position) is not int and type(position) is not float:
                    continue
            raise InputError(f'{subjects[position]} credit', scores[position])

        subject_gpa = np.array([find_subject_gpa(subjects[i], levels[i], scores[i])
                                for i in range(len(subjects))])

        gpa = np.round(sum(subject_gpa * credit_weights) / sum(credit_weights), 3)
        output_label.config(text='Your GPA: ' + str(gpa), foreground='black')

    except InputError as error:
        output_label.config(text=str(error), foreground='red')


def save_input():
    info = get_input()
    path = filedialog.asksaveasfilename(title='Save as Excel file',
                                        filetypes=(('Microsoft Excel', '*.xlsx'),
                                                   ('all files', '*.*')),
                                        defaultextension='.xlsx')
    info.to_excel(path)
    save_input_label.config(text='Input saved at: ' + os.path.abspath(path))


def save_gpa():
    gpa = output_label['text'].split(': ')[1]
    t = time.strftime('%Y-%m-%d')
    content = t + ' GPA: ' + gpa
    with open('GPA output.txt', 'r') as fout:
        current_content = fout.read()
    with open('GPA output.txt', 'w') as fout:
        fout.write(current_content + '\n' + content)
    save_gpa_label.config(text='GPA saved at: ' + os.path.abspath('GPA output.txt'))


def complete_gpa_table(gpa_table):
    digit_grade = {'A+': 0, 'A': 0, 'A-': 1, 'B+': 2, 'B': 3, 'B-': 4, 'C+': 5}
    for grade in digit_grade.keys():
        gpa_table.loc[grade] = gpa_table.iloc[0] - 0.3 * digit_grade[grade]
    gpa_table.loc['C'] = gpa_table.loc['C-'] = gpa_table.iloc[0] - 1.9
    gpa_table.loc['F'] = 0

    return gpa_table


chinese_gpa_table = complete_gpa_table(pd.DataFrame(
    {'IB': 4.5, 'H+': 4.4, 'H': 4.3, 'S': 4.2, 'AP': 4.2, 'VII': 4.2, 'VI': 4.2, 'V': 4.2,
     'IV': 4.1, 'III': 4.1, 'II': 4.0, 'I': 4.0}, index=['A+']))

english_gpa_table = complete_gpa_table(pd.DataFrame(
    {'IB': 4.5, 'AP': 4.5, 'H+': 4.4, 'H': 4.3, 'S+': 4.1, 'S': 4.0}, index=['A+']))

non_language_gpa_table = complete_gpa_table(pd.DataFrame(
    {'IB': 4.5, 'AP': 4.5, 'A-level': 4.5, 'H': 4.3, 'S+': 4.15, 'S': 4.0}, index=['A+']))

subjects = ['Chinese', 'Math', 'English', 'History', 'Physics', 'Chemistry', 'Elective1',
            'Elective2']

attributes = ['level', 'score', 'credit']

root = tk.Tk()
root.geometry('590x400')
root.title('GPA calculator')

sbj_label_group = {}
attr_label_group = {}
input_group = pd.DataFrame({}, index=subjects,
                           columns=attributes)

for i in range(len(attributes)):
    attr_label_group[attributes[i]] = ttk.Label(root, text=attributes[i])
    attr_label_group[attributes[i]].grid(row=0, column=i + 1, padx=5)

for i in range(len(subjects)):
    sbj_label_group[subjects[i]] = ttk.Label(text=subjects[i])
    sbj_label_group[subjects[i]].grid(row=i + 1, column=0)
    for j in range(len(attributes)):
        if attributes[j] == 'level':
            if subjects[i] == 'Chinese':
                input_group.loc['Chinese', 'level'] = ttk.Combobox(root, values=list(
                    chinese_gpa_table.columns))
            elif subjects[i] == 'English':
                input_group.loc['English', 'level'] = ttk.Combobox(root, values=list(
                    english_gpa_table.columns))
            elif subjects[i] == 'Math':
                input_group.loc['Math', 'level'] = ttk.Combobox(root, values=list(
                    non_language_gpa_table.columns))
            else:
                input_group.loc[subjects[i], 'level'] = ttk.Combobox(
                    root, values=list(non_language_gpa_table.columns))
        else:
            input_group.loc[subjects[i], attributes[j]] = ttk.Entry(root)

        input_group.loc[subjects[i], attributes[j]].grid(row=i + 1, column=j + 1, padx=5, pady=2)

open_input_file_button = ttk.Button(text='Browse files', command=open_input_file)
open_input_file_button.grid(row=len(subjects)+1, column=0, padx=5, pady=2)

input_filename_label = ttk.Label(text='File opened: ')
input_filename_label.grid(row=len(subjects)+1, column=1, columnspan=10, sticky='w')

calculate_gpa_button = ttk.Button(text='calculate', command=calculate_gpa)
calculate_gpa_button.grid(row=len(subjects)+2, column=0, padx=5, pady=2)
root.bind('<Return>', lambda event: calculate_gpa())

output_label = ttk.Label(text='Your GPA:')
output_label.grid(row=len(subjects)+2, column=1, columnspan=10, sticky='w')

save_input_button = ttk.Button(text='Save input', command=save_input)
save_input_button.grid(row=len(subjects)+3, column=0, padx=5, pady=2)

save_input_label = ttk.Label(text='Input saved at: ')
save_input_label.grid(row=len(subjects)+3, column=1, columnspan=10, sticky='w')

save_gpa_button = ttk.Button(text='Save GPA', command=save_gpa)
save_gpa_button.grid(row=len(subjects)+4, column=0, padx=5, pady=2)

save_gpa_label = ttk.Label(text='GPA saved at: ')
save_gpa_label.grid(row=len(subjects)+4, column=1, columnspan=10, sticky='w')

root.mainloop()
