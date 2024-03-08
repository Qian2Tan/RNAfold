import pandas as pd

path = "up45down9"
site_data = pd.read_csv(f"{path}.csv")
site_data.fillna('', inplace=True)

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
            print(char)
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


# 將 find_countinuous 函數應用於每一行
site_data = site_data.apply(find_countinuous, axis=1)

site_data.drop(columns=["5'"], inplace=True)
site_data.drop(columns=["loop"], inplace=True)
site_data.drop(columns=["3'"], inplace=True)

column_list = ["index", "genome_site", "direction", "TTS_intensity", "TTS_upstream_RNA_coverage", "TTS_downstream_RNA_coverage",
               "source", "start_site", "end_site", "squence", "RNAfold", "RNAfold_energy", "mark_region (1 based)", "5' A", "3' U", "pairing_count"]
site_data.to_csv(f"{path}_count.csv")