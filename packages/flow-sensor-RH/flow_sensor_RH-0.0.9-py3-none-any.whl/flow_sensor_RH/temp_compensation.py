import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate as interp
import re
import os
import statsmodels.api as sm
from . import data_process

def genSpectreDataExcel_T_TCRRC_RC0_Th(input_file_name, output_file_name, \
                                       velocity_row_num_csv = 0):
    assert(os.path.exists(input_file_name)), input_file_name + " does not exist, please check it"
    assert(input_file_name != output_file_name), "You cannot modify the input file"
    assert(not os.path.exists(output_file_name)), output_file_name + " exists, please rename or delete it"
    dataset = pd.read_csv(input_file_name)
    dataset_save = pd.DataFrame()
    dataset_col = dataset.columns
    dataset_len = int(len(dataset_col) / 2)
    val_save = np.zeros((dataset_len, 4))
    col_val_str = dataset_col[0].replace("/", "")
    col_val_arr = re.search("(?<=\().+?(?=\))", col_val_str).group().split(" ")
    col_val_str_out = re.search(".+?(?=\()", col_val_str).group().replace(" ", "")
    val_label = np.array([
        col_val_arr[0].split("=")[0],
        col_val_arr[1].split("=")[0],
        col_val_arr[2].split("=")[0],
        col_val_str_out
    ])
    if not velocity_row_num_csv:
        velocity_row_num_csv = dataset.shape[0] + 1
    velocity_row_num = velocity_row_num_csv - 2
    for i in range(dataset_len):
        col_val_str = dataset_col[int(2 * i + 1)]
        col_val_arr = re.search("(?<=\().+?(?=\))", col_val_str).group().split(" ")
        val_save[i, 0] = col_val_arr[0].split("=")[1]
        val_save[i, 1] = col_val_arr[1].split("=")[1]
        val_save[i, 2] = col_val_arr[2].split("=")[1]
        val_save[i, 3] = dataset[col_val_str][velocity_row_num]
    for i in range(len(val_label)):
        dataset_save[val_label[i]] = val_save[:, i]
    dataset_save.to_excel(output_file_name)
    save_path = data_process.getSavePath(output_file_name)
    return save_path

def OLSFitting_C_T_TCRRC_RC0_2x3__Th(file_name, \
                                     T_TCRRC_RC0_Th_col_name_arr = [ \
                                         "temp", "TCR_Rc", "Rc0", "Th" \
                                     ]):
    assert(os.path.exists(file_name)), file_name + " does not exist, please check it"
    dataset = pd.read_excel(file_name)
    dataset_col = T_TCRRC_RC0_Th_col_name_arr
    dataset_new = pd.DataFrame()
    T_name, TCRRC_name, RC0_name, Th_name = dataset_col[0], dataset_col[1], \
                                            dataset_col[2], dataset_col[3]
    dataset_new["T"]         = dataset[T_name]
    dataset_new["TCRRC"]     = dataset[TCRRC_name]
    dataset_new["RC0"]       = dataset[RC0_name]
    dataset_new["TCRRC_x_T"] = dataset_new["TCRRC"] * dataset_new["T"]
    dataset_new["Th"]        = dataset[Th_name]
    x = sm.add_constant(dataset_new.iloc[:, 0:4])
    y = dataset_new["Th"]
    model = sm.OLS(y, x)
    model.fit().summary()
    const_, T_coef, TCRRC_coef, RC0_coef, TCRRC_x_T_coef = model.fit().params
    return const_, T_coef, TCRRC_coef, RC0_coef, TCRRC_x_T_coef
