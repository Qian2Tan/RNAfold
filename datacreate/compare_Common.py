import pandas as pd

# 定義一個函數來進行比較並添加 'common' 標記
def find_common(row, other_df):
    a = row['genome_site']
    direction = row['direction']

    if direction == '+':
        common = 'common' if any((a - 5) <= b <= (a + 5) for b in other_df[other_df['direction'] == '+']['genome_site']) else ''
    elif direction == '-':
        common = 'common' if any((a - 5) <= b <= (a + 5) for b in other_df[other_df['direction'] == '-']['genome_site']) else ''
    else:
        common = ''

    return common


if __name__ == "__main__":

    site_data_08 = pd.read_csv('own_S08_11_RNAfold_markregion_ver2_analysis.csv')
    site_data_09 = pd.read_csv('own_S09_09_WT_RNAfold_markregion_ver2_analysis.csv')

    # 在 df1 上應用函數並將結果添加到新列 'common'
    site_data_08['common'] = site_data_08.apply(find_common, args=(site_data_09,), axis=1)
    # 在 df2 上應用函數並將結果添加到新列 'common'
    site_data_09['common'] = site_data_09.apply(find_common, args=(site_data_08,), axis=1)

    # 將 df1 中 'common' 列中值為空格的改為 'df1_only'
    site_data_08.loc[site_data_08['common'] == '', 'common'] = 's08_only'
    site_data_09.loc[site_data_09['common'] == '', 'common'] = 's09_only'

    print(site_data_08)
    print(site_data_09)
    site_data_08.to_csv('S08_11_common.csv')
    site_data_09.to_csv('S09_09_WT_common.csv')

    # 計算 'common' 列中包含 'common' 的行數
    total_common1 = (site_data_08['common'] == 'common').sum()
    print('s08 common= ',total_common1)
    total_s08 = (site_data_08['common'] == 's08_only').sum()
    print('s08 only= ',total_s08)

    # 計算 'common' 列中包含 'common' 的行數
    total_common2 = (site_data_09['common'] == 'common').sum()
    print('s09 common= ',total_common2)
    total_s09 = (site_data_09['common'] == 's09_only').sum()
    print('s09 only= ',total_s09)