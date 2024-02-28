import pandas as pd
import warnings
from subprocess import PIPE, Popen
import os
from tqdm import trange

def RNAfold(site_data_name, site_data, index_col, sequence_col):
    command = "RNAfold < 'tmp.fa'"
    output_list = []
    output_energy = []

    # 创建与 site_data 名称相关的文件夹
    folder_name = f"{site_data_name}_pictures"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for i in trange(len(site_data)):
        with open("tmp.fa", 'w') as file:
            file.write(f">{site_data[index_col][i]}\n{site_data[sequence_col][i]}")
        with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
            output = process.communicate()[0].decode("utf-8")
            output = output.split('\n')
            output_sequence_energy = output[2].split(' (')
            output_list.append(output_sequence_energy[0].split(' ')[0])
            output_energy.append(output_sequence_energy[1].strip(')'))
        try:
            # 将文件移动到 'pictures' 文件夹
            os.rename(f"{site_data[index_col][i]}_ss.ps", f"{folder_name}/{site_data[index_col][i]}_ss.ps")
            # os.remove(f"{site_data[index_col][i]}_ss.ps")
        except FileNotFoundError:
            pass  # 处理文件不存在的情况
    return output_list, output_energy

if __name__ == '__main__':
     ###
    # doing the RNAfold for given dataframe by own data
#     site_data_name_11 = "own_S08_11_original"
#     site_data_11 = pd.read_csv("own_S08_11_original.csv",index_col=[0])
#     site_data_11.reset_index(inplace=True)
#     output_list_11,output_energy_11 = RNAfold(site_data_name_11, site_data_11,'index','sequence')

#     site_data_11['RNAfold'] = output_list_11
#     site_data_11['RNAfold_energy'] = output_energy_11
#     site_data_11.to_csv("own_S08_11.csv")
# # ---------------------------------------------------------------------------------------------------------
#     site_data_name_09_wt = "own_S09_09_WT_original"
#     site_data_09_wt = pd.read_csv("own_S09_09_WT_original.csv",index_col=[0])
#     site_data_09_wt.reset_index(inplace=True)
#     output_list_09_wt, output_energy_09_wt = RNAfold(site_data_name_09_wt, site_data_09_wt,'index','sequence')

#     site_data_09_wt['RNAfold'] = output_list_09_wt
#     site_data_09_wt['RNAfold_energy'] = output_energy_09_wt
#     site_data_09_wt.to_csv("own_S09_09_WT.csv")

#--------------------------------------------------------------------------------------------------------------
    site_data_name_up45down9 = "up45down9"
    site_data_up45down9 = pd.read_csv("origin_add_up45down9_modi_prune_order.csv", index_col=[0])
    site_data_up45down9.reset_index(inplace=True)
    output_list_up45down9, output_energy_up45down9 = RNAfold(site_data_name_up45down9, site_data_up45down9,'index','upstream_45_downstream_9')

    # site_data_up45down9['RNAfold'] = output_list_up45down9
    # site_data_up45down9['RNAfold_energy'] = output_energy_up45down9
    # site_data_up45down9.to_csv("add_up45down9.csv")