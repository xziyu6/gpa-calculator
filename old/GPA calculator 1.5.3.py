import os
import pandas as pd
import tkinter as tk
import numpy as np
from tkinter import filedialog
from tkinter import ttk
import time


class InputError(Exception):
    def __init__(self, position, value):
        self.position = position
        self.value = value

    def __str__(self):
        return "{0}: {1} is invalid input".format(str(self.position), repr(self.value))


def digitize_score(scr, sbj):
    if 92.5 <= scr <= 100:
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
    elif 0 <= scr < 59.5:
        return 8
    else:
        raise InputError(sbj + ' ' + 'score', scr)


def standardize_level(lv, sbj):
    if sbj == 'Math' and (lv == 'HLM' or lv == '素养班'):
        return 'H'
    elif sbj == 'Chinese' and lv in chinese_sbj_list.keys():
        return chinese_sbj_list[lv]

    if sbj == 'Chinese' and lv not in chinese_gpa_df.keys():
        raise InputError('Chinese level', lv)
    elif sbj == 'English' and lv not in english_gpa_df.keys():
        raise InputError('English level', lv)
    elif sbj != 'Chinese' and sbj != 'English' and lv not in non_language_gpa_df.keys():
        raise InputError(sbj + ' ' + 'level', lv)

    return lv


def find_gpa(sbj, lv, scr):
    if sbj == 'Chinese':
        return chinese_gpa_df[lv][scr]
    elif sbj == 'English':
        return english_gpa_df[lv][scr]
    else:
        return non_language_gpa_df[lv][scr]


def open_input_file():
    path = filedialog.askopenfilename(title='Select an Excel file',
                                      filetypes=(('Microsoft Excel', '*.xlsx'),
                                                 ('all files', '*.*')),
                                      defaultextension='.xlsx')
    input_filename_label.config(text='File opened: ' + path)
    # noinspection PyArgumentList
    info = pd.read_excel(path, index_col=0)
    for sbj in sbj_list:
        for attr in attr_list:
            if attr == 'level':
                input_group.loc[sbj, attr].set(info.loc[sbj, attr].upper())
            else:
                input_group.loc[sbj, attr].delete(0, len(input_group.loc[sbj, attr].get()))
                input_group.loc[sbj, attr].insert(0, info.loc[sbj, attr])


def is_decimal(string):
    if '.' in string:
        if string.replace('.', '').isdigit():
            return True
    elif string.isdigit():
        return True
    return False


def apply_for_element(func, array, *args, dtype=None, **kwargs):
    result_array = np.array([], dtype=dtype)
    df = pd.DataFrame(args).T
    for i in range(len(array)):
        if len(df.index) != 0:
            current_args = tuple(df.iloc[i].values)
            result_array = np.append(result_array, func(array[i], *current_args, **kwargs))
        else:
            result_array = np.append(result_array, func(array[i], *args, **kwargs))
    return result_array


def get_input():
    info = pd.DataFrame({}, index=sbj_list, columns=attr_list)

    for sbj in sbj_list:
        for attr in attr_list:
            info.loc[sbj, attr] = input_group.loc[sbj, attr].get()

    return info


def calculate_gpa_command():
    info = get_input()

    gpa_array = np.array([], dtype=float)
    try:
        level_array = np.array(info.loc[:, 'level'])
        score_array = np.array(info.loc[:, 'score'])
        credit_array = np.array(info.loc[:, 'credit'])

        apply_for_element(standardize_level, level_array, sbj_list)

        if np.all(apply_for_element(is_decimal, score_array)):
            score_array = np.array(score_array, dtype=float)
            score_array = apply_for_element(digitize_score, score_array, sbj_list)
        else:
            first_wrong_index = np.where(~ apply_for_element(is_decimal, score_array, dtype=bool))[0][0]
            raise InputError(sbj_list[first_wrong_index] + ' ' + 'score', score_array[first_wrong_index])

        if np.all(apply_for_element(is_decimal, credit_array)):
            credit_array = np.array(credit_array, dtype=float)
        else:
            first_wrong_index = np.where(~ apply_for_element(is_decimal, credit_array, dtype=bool))[0][0]
            raise InputError(sbj_list[first_wrong_index] + ' ' + 'credit', credit_array[first_wrong_index])

        gpa_array = apply_for_element(find_gpa, sbj_list, level_array, score_array)

        gpa = np.round((np.dot(gpa_array, credit_array[:, np.newaxis]) / np.sum(credit_array))[0], 3)
        output_label.config(text='Your GPA: ' + str(gpa), foreground='black')

    except InputError as error:
        output_label.config(text=str(error), foreground='red')


def save_input_command():
    info = get_input()
    path = filedialog.asksaveasfilename(title='Save as Excel file',
                                        filetypes=(('Microsoft Excel', '*.xlsx'),
                                                   ('all files', '*.*')),
                                        defaultextension='.xlsx')
    info.to_excel(path)
    save_input_label.config(text='Input saved at: ' + os.path.abspath(path))


def save_gpa_command():
    gpa = output_label['text'].split(': ')[1]
    t = time.strftime('%Y-%m-%d')
    content = t + ' GPA: ' + gpa
    with open('GPA output.txt', 'r') as fout:
        current_content = fout.read()
    with open('GPA output.txt', 'w') as fout:
        fout.write(current_content + '\n' + content)
    save_gpa_label.config(text='GPA saved at: ' + os.path.abspath('GPA output.txt'))


chinese_gpa_df = pd.DataFrame({'H': {1: 4.3, 2: 4.0, 3: 3.7, 4: 3.4, 5: 3.1, 6: 2.8, 7: 2.4, 8: 0},
                               'S': {1: 4.2, 2: 3.9, 3: 3.6, 4: 3.3, 5: 3.0, 6: 2.7, 7: 2.3, 8: 0},
                               'III': {1: 4.1, 2: 3.8, 3: 3.5, 4: 3.2, 5: 2.9, 6: 2.6, 7: 2.2, 8: 0},
                               'I': {1: 4.0, 2: 3.7, 3: 3.4, 4: 3.1, 5: 2.8, 6: 2.5, 7: 2.1, 8: 0}})

english_gpa_df = pd.DataFrame({'H+': {1: 4.4, 2: 4.1, 3: 3.8, 4: 3.5, 5: 3.2, 6: 2.9, 7: 2.5, 8: 0},
                               'H': {1: 4.3, 2: 4.0, 3: 3.7, 4: 3.4, 5: 3.1, 6: 2.8, 7: 2.4, 8: 0},
                               'S+': {1: 4.1, 2: 3.8, 3: 3.5, 4: 3.2, 5: 2.9, 6: 2.6, 7: 2.2, 8: 0},
                               'S': {1: 4.0, 2: 3.7, 3: 3.4, 4: 3.1, 5: 2.8, 6: 2.5, 7: 2.1, 8: 0}})

non_language_gpa_df = pd.DataFrame({'H': {1: 4.3, 2: 4.0, 3: 3.7, 4: 3.4, 5: 3.1, 6: 2.8, 7: 2.4, 8: 0},
                                    'S+': {1: 4.15, 2: 3.85, 3: 3.55, 4: 3.25, 5: 2.95, 6: 2.65, 7: 2.25, 8: 0},
                                    'S': {1: 4.0, 2: 3.7, 3: 3.4, 4: 3.1, 5: 2.8, 6: 2.5, 7: 2.1, 8: 0}})

sbj_list = ['Chinese', 'Math', 'English', 'History', 'Physics', 'Chemistry', 'Elective']
attr_list = ['level', 'score', 'credit']
chinese_sbj_list = {'I': 'I', 'II': 'I', 'III': 'III', 'IV': 'III', 'V': 'S', 'VI': 'S', 'VII': 'S', 'S': 'S', 'H': 'H'}

root = tk.Tk()
root.geometry('590x340')
root.title('GPA calculator')

sbj_label_group = {}
attr_label_group = {}
input_group = pd.DataFrame({}, index=sbj_list,
                           columns=attr_list)

for i in range(len(attr_list)):
    attr_label_group[attr_list[i]] = ttk.Label(root, text=attr_list[i])
    attr_label_group[attr_list[i]].grid(row=0, column=i + 1, padx=5)

for i in range(len(sbj_list)):
    sbj_label_group[sbj_list[i]] = ttk.Label(text=sbj_list[i])
    sbj_label_group[sbj_list[i]].grid(row=i + 1, column=0)
    for j in range(len(attr_list)):
        if attr_list[j] == 'level':
            if sbj_list[i] == 'Chinese':
                input_group.loc['Chinese', 'level'] = ttk.Combobox(root, values=list(chinese_sbj_list.keys()))
            elif sbj_list[i] == 'English':
                input_group.loc['English', 'level'] = ttk.Combobox(root, values=list(english_gpa_df.columns))
            elif sbj_list[i] == 'Math':
                input_group.loc['Math', 'level'] = ttk.Combobox(root,
                                                                values=list(non_language_gpa_df.columns + ['HLM']))
            else:
                input_group.loc[sbj_list[i], 'level'] = ttk.Combobox(root,
                                                                     values=list(non_language_gpa_df.columns))
        else:
            input_group.loc[sbj_list[i], attr_list[j]] = ttk.Entry(root)

        input_group.loc[sbj_list[i], attr_list[j]].grid(row=i + 1, column=j + 1, padx=5, pady=2)

open_input_file_button = ttk.Button(text='Browse files', command=open_input_file)
open_input_file_button.grid(row=8, column=0, padx=5, pady=2)

input_filename_label = ttk.Label(text='File opened: ')
input_filename_label.grid(row=8, column=1, columnspan=10, sticky='w')

calculate_gpa_button = ttk.Button(text='calculate', command=calculate_gpa_command)
calculate_gpa_button.grid(row=9, column=0, padx=5, pady=2)
root.bind('<Return>', lambda event: calculate_gpa_command())

output_label = ttk.Label(text='Your GPA:')
output_label.grid(row=9, column=1, columnspan=10, sticky='w')

save_input_button = ttk.Button(text='Save input', command=save_input_command)
save_input_button.grid(row=10, column=0, padx=5, pady=2)

save_input_label = ttk.Label(text='Input saved at: ')
save_input_label.grid(row=10, column=1, columnspan=10, sticky='w')

save_gpa_button = ttk.Button(text='Save GPA', command=save_gpa_command)
save_gpa_button.grid(row=11, column=0, padx=5, pady=2)

save_gpa_label = ttk.Label(text='GPA saved at: ')
save_gpa_label.grid(row=11, column=1, columnspan=10, sticky='w')

root.mainloop()
