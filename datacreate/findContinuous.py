import pandas as pd

def find_countinuous(row):
    if row['mark_region (1 based)'] == 'special case' or row['mark_region (1 based)'] == '-' or row['mark_region (1 based)'] == 'logic out case':
        row["5' A"] = "-"
        row["3' U"] = "-"
        row["pairing_count"] = "-"
        return row
    else:
        start, end = map(int, row['mark_region (1 based)'].split("-"))
        start -= 1

        # 分出三段
        sequence = row['sequence']
        row["5'"] = sequence[:start]
        row["3'"] = sequence[end:]

        rnafold = row['RNAfold']
        row["loop"] = rnafold[start:end]

        # 找出連續 A 的個數
        count_A = 0
        for char in reversed(row["5'"]):  # 倒序遍歷字串
            if char == 'A':
                count_A += 1
            else:
                break  # 當遇到不是 'A' 的字符時結束迴圈
        row["5' A"] = count_A

        # 找出連續 T 的個數
        count_U = 0
        for char in row["3'"]:  # 正序遍歷字串
            # print(char)
            if char == 'U': # paper那份要改成U
                count_U += 1
            else:
                break  # 當遇到不是 'T' 的字符時結束迴圈
        row["3' U"] = count_U

        count_pairing_start = 0
        count_pairing_last = 0
        # 檢查 loop 不以句點開頭或結尾
        if row["loop"].startswith(".") or row["loop"].endswith("."):
            row["pairing_count"] = "starts or ends with '.'"
        else:
            for char in row["loop"]:
                if char == "(" :
                    count_pairing_start += 1
                else:
                    break
            for char in reversed(row["loop"]):
                if char == ")":
                    count_pairing_last += 1
                else:
                    break

            count_pairing = min(count_pairing_start, count_pairing_last)
            row["pairing_count"] = count_pairing

        return row


def compare_continuous (df, pair_condition):
    # 將 'continue_pair' 列的值轉換為整數類型，忽略無法轉換為整數的值（例如 '-'）
    df['continue_pair'] = pd.to_numeric(df['continue_pair'], errors='coerce')
    # 將 'continue_pair' 列的值轉換為整數類型，忽略無法轉換為整數的值（例如 '-'）
    df['continue_A'] = pd.to_numeric(df['continue_A'], errors='coerce')
    # 將 'continue_pair' 列的值轉換為整數類型，忽略無法轉換為整數的值（例如 '-'）
    df['continue_U'] = pd.to_numeric(df['continue_U'], errors='coerce')

    print('pairing continue >=', pair_condition, '\n')
    condition = (df['continue_pair'] != '-') & (df['continue_pair'] >= pair_condition)
    df = df[condition]

    print("     3'U    >= 4   >= 5   >= 6\n")

    condition1 = (df['continue_A'] >= 2) & (df['continue_U'] >= 4)
    df_1 = df[condition1]
    count1 = df_1.shape[0]

    condition2 = (df['continue_A'] >= 2) & (df['continue_U'] >= 5)
    df_2 = df[condition2]
    count2 = df_2.shape[0]

    condition3 = (df['continue_A'] >= 2) & (df['continue_U'] >= 6)
    df_3 = df[condition3]
    count3 = df_3.shape[0]

    print("5'A >= 2   ", count1, "   ", count2, "   ", count3,"\n")

    condition4 = (df['continue_A'] >= 3) & (df['continue_U'] >= 4)
    df_4 = df[condition4]
    count4 = df_4.shape[0]

    condition5 = (df['continue_A'] >= 3) & (df['continue_U'] >= 5)
    df_5 = df[condition5]
    count5 = df_5.shape[0]

    condition6 = (df['continue_A'] >= 3) & (df['continue_U'] >= 6)
    df_6 = df[condition6]
    count6 = df_6.shape[0]

    print("5'A >= 3   ", count4, "   ", count5, "   ", count6,"\n")

    condition7 = (df['continue_A'] >= 4) & (df['continue_U'] >= 4)
    df_7 = df[condition7]
    count7 = df_7.shape[0]

    condition8 = (df['continue_A'] >= 4) & (df['continue_U'] >= 5)
    df_8 = df[condition8]
    count8 = df_8.shape[0]

    condition9 = (df['continue_A'] >= 4) & (df['continue_U'] >= 6)
    df_9 = df[condition9]
    count9 = df_9.shape[0]

    print("5'A >= 3   ", count7, "   ", count8, "   ", count9,"\n")


if __name__ == "__main__":
    # path = "up45down9"
    # site_data_paper = pd.read_csv(f"{path}.csv")
    # site_data_paper.fillna('', inplace=True)

    # # 將 find_countinuous 函數應用於每一行
    # site_data_paper = site_data_paper.apply(find_countinuous, axis=1)

    # site_data.drop(columns=["5'"], inplace=True)
    # site_data.drop(columns=["loop"], inplace=True)
    # site_data.drop(columns=["3'"], inplace=True)

    # column_list = ["index", "genome_site", "direction", "TTS_intensity", "TTS_upstream_RNA_coverage", "TTS_downstream_RNA_coverage",
    #             "source", "start_site", "end_site", "squence", "RNAfold", "RNAfold_energy", "mark_region (1 based)", "5' A", "3' U", "pairing_count"]
    # site_data.to_csv(f"{path}_count.csv")

    site_data_paper = pd.read_csv('origin_add_up45down9_markregion_ver2_analysis.csv')
    compare_continuous(site_data_paper, 2)
    compare_continuous(site_data_paper, 3)
    compare_continuous(site_data_paper, 4)
    print('------------------------------------------------')

    site_data_08 = pd.read_csv('own_S08_11_RNAfold_markregion_ver2_analysis.csv')
    compare_continuous(site_data_08, 2)
    compare_continuous(site_data_08, 3)
    compare_continuous(site_data_08, 4)
    print('------------------------------------------------')

    site_data_09 = pd.read_csv('own_S09_09_WT_RNAfold_markregion_ver2_analysis.csv')
    compare_continuous(site_data_09, 2)
    compare_continuous(site_data_09, 3)
    compare_continuous(site_data_09, 4)

