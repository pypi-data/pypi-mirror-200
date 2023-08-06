import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate as interp
import os
import random
import re

def getSavePath(flie_name):
    save_path = os.path.abspath(".") + "\\" + flie_name
    print("Save to: " + save_path)
    return save_path

def ALGO_QSortPart(arr, start_idx, end_idx):
    i = start_idx - 1
    pivot = arr[end_idx]
    for j in range(start_idx, end_idx): 
        if arr[j] <= pivot: 
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[end_idx] = arr[end_idx], arr[i + 1] 
    return (i + 1)
    
def ALGO_QSort(arr, start_idx, end_idx): 
    if start_idx >= end_idx:
        return arr
    arr_temp = arr.copy()
    pivot_idx = random.randint(start_idx, end_idx)
    arr_temp[pivot_idx], arr_temp[end_idx] = arr_temp[end_idx], arr_temp[pivot_idx]
    pi = ALGO_QSortPart(arr_temp, start_idx, end_idx)
    arr_temp = ALGO_QSort(arr_temp, start_idx, pi - 1)
    arr_temp = ALGO_QSort(arr_temp, pi + 1, end_idx)
    return arr_temp

def genTempArr(start_temp = 0, end_temp = 50, step = 10, addition = np.array([25])):
    temp_arr = np.arange(start_temp, end_temp + step, step)
    temp_arr = np.concatenate((temp_arr, addition))
    temp_arr = ALGO_QSort(temp_arr, 0, len(temp_arr) - 1) * 1.0
    return temp_arr

def genSheetNameArr(start_temp = 0, end_temp = 50, step = 10, addition = np.array([25]), direct = "both"):
    assert(direct == "both" or direct == "fore" or direct == "back" or direct == "none"), \
            "direct should be \"both\", \"fore\", \"back\" or \"none\""
    temp_arr = genTempArr(start_temp, end_temp, step, addition)
    temp_arr_str = temp_arr.round(2).astype(str)
    temp_arr_str = np.char.replace(temp_arr_str, ".", "C")
    if direct == "none":
        sheet_name_arr = temp_arr_str
    elif direct == "fore" or direct == "back":
        sheet_name_arr = np.char.add(temp_arr_str, "_" + direct)
    else:
        sheet_name_arr_fore = np.char.add(temp_arr_str, "_+0+fore")
        sheet_name_arr_back = np.char.add(temp_arr_str, "_+1+back")
        sheet_name_arr = np.concatenate((sheet_name_arr_fore, sheet_name_arr_back))
        sheet_name_arr = ALGO_QSort(sheet_name_arr, 0, len(sheet_name_arr) - 1)
        sheet_name_arr = np.char.replace(sheet_name_arr, "+0+", "")
        sheet_name_arr = np.char.replace(sheet_name_arr, "+1+", "")
    return sheet_name_arr

def genExpDataExcel(file_name, sheet_name_arr, \
                    x_label = "Velocity", y_label = "DVout"):
    assert(not os.path.exists(file_name + ".xlsx")), file_name + ".xlsx exists, please rename or delete it"
    exp_blank_sheet = pd.DataFrame(columns = [x_label, y_label])
    with pd.ExcelWriter(file_name + ".xlsx") as writer:
        for sheet_name in sheet_name_arr:
            exp_blank_sheet.to_excel(writer, sheet_name, index = False)
    save_path = getSavePath(file_name + ".xlsx")
    return save_path

def modifyColName(input_file_name, output_file_name, \
                  search_str = r",(?=[^\(]+\))", replace_str = " "):
    assert(os.path.exists(input_file_name)), input_file_name + " does not exist, please check it"
    assert(input_file_name != output_file_name), "You cannot modify the input file"
    assert(not os.path.exists(output_file_name)), output_file_name + " exists, please rename or delete it"
    with open(input_file_name, "r") as read_file, open(output_file_name, "w") as write_file:
        line_col_name = False
        for line in read_file:
            if not line_col_name:
                line_col_name = True
                line_new = re.sub(search_str, replace_str, line)
                write_file.write(line_new)
            else:
                write_file.write(line)
    save_path = getSavePath(output_file_name)
    return save_path
