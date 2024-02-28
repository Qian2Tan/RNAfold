import pandas as pd

def modify_special_case(path):
    site_data = pd.read_csv(path)

    # special case
    special_case_mask = site_data['special_check'].notna()
    site_data.loc[special_case_mask, 'sequence_modi_prune'] = 'special case'
    site_data.loc[special_case_mask, 'rnafold_modi_prune'] = 'special case'

    # no modified case
    no_modified_mask = (site_data['special_check'].isna()) & (site_data['modi_check'].isna())
    site_data.loc[no_modified_mask, 'sequence_modi_prune'] = 'no modified'
    site_data.loc[no_modified_mask, 'rnafold_modi_prune'] = 'no modified'

    return site_data


if __name__ == "__main__":
    # path = "/home/xiangwei/chien/rnafold/datacreate/own_S08_11_RNAfold_modi_prune_order.csv"
    # name = 'own_S08_11'

    # path = "/home/xiangwei/chien/rnafold/datacreate/own_S09_09_WT_RNAfold_modi_prune_order.csv"
    # name = 'own_S09_09_WT'

    # site_data = modify_special_case(path)
    # site_data.to_csv(f'{name}.csv')
    # ---------------------------------------------------------------------------------------

    path = '/home/xiangwei/chien/rnafold/datacreate/origin_add_up45down9_modi_prune_order.csv'
    name = 'up45down9'
    site_data = modify_special_case(path)

    reference_data = pd.read_excel('/home/xiangwei/chien/rnafold/datacreate/2019_Nat Microbiol_Ju_full-length RNa profiling reveals pervasive bidirectional transcription terminators in bacteria_TSS annotation.xlsx', header=1)
    print(reference_data)
    site_data['TTS_sequence(include_8nt_of_each_flank_sequence)'] = reference_data['TTS_sequence(include_8nt_of_each_flank_sequence)']
    print(site_data)
    site_data.to_csv('up45down9.csv')
