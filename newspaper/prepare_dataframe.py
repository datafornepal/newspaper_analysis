import glob, os
import pandas as pd
from newspaper.levels import level1_count,level_2_3_count,level_2_3_filter,level_len, data_level2,data_level3

# TODO
# Change 6 dataframes to 1 dataframes
# This will replace 12 dataframes to 2 dataframes
# Some other type of analysis like bucket analysis will be possible

df_HT = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/HT', "*.csv"))),sort=False).drop_duplicates(['url'], 'first').dropna()
df_OK = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/OK', "*.csv"))),sort=False).drop_duplicates(['url'], 'first').dropna()
df_NT = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/NT', "*.csv"))),sort=False).drop_duplicates(['url'], 'first').dropna()
df_TN = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/TN', "*.csv"))),sort=False).drop_duplicates(['url'], 'first').dropna()
df_KT = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/KT', "*.csv"))),sort=False).drop_duplicates(['url'], 'first').dropna()
df_LK = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/LK', "*.csv"))),sort=False).drop_duplicates(['url'], 'first').dropna()

# Run this once in a while to optimize speed and space
# df_HT.to_csv('newspaper/static/datasets/ht_jan_21.csv', index=False)
# df_OK.to_csv('newspaper/static/datasets/ok_jan_21.csv', index=False)
# df_NT.to_csv('newspaper/static/datasets/nt_jan_21.csv', index=False)
# df_TN.to_csv('newspaper/static/datasets/tn_jan_21.csv', index=False)
# df_KT.to_csv('newspaper/static/datasets/kt_jan_21.csv', index=False)
# df_LK.to_csv('newspaper/static/datasets/lk_jan_21.csv', index=False)


df_HT['level1'] = df_HT['content'].apply(level1_count)
df_OK['level1'] = df_OK['content'].apply(level1_count)
df_NT['level1'] = df_NT['content'].apply(level1_count)
df_TN['level1'] = df_TN['content'].apply(level1_count)
df_KT['level1'] = df_KT['content'].apply(level1_count)
df_LK['level1'] = df_LK['content'].apply(level1_count)

df_HT['level_len'] = df_HT['level1'].apply(level_len)
df_OK['level_len'] = df_OK['level1'].apply(level_len)
df_NT['level_len'] = df_NT['level1'].apply(level_len)
df_TN['level_len'] = df_TN['level1'].apply(level_len)
df_KT['level_len'] = df_KT['level1'].apply(level_len)
df_LK['level_len'] = df_LK['level1'].apply(level_len)

df_HT['level_2_3_valid'] = df_HT['content'].apply(level_2_3_filter)
df_HT_level_2_3 = df_HT[df_HT['level_2_3_valid']==1].reset_index(drop=True)
df_OK['level_2_3_valid'] = df_OK['content'].apply(level_2_3_filter)
df_OK_level_2_3 = df_OK[df_OK['level_2_3_valid']==1].reset_index(drop=True)
df_NT['level_2_3_valid'] = df_NT['content'].apply(level_2_3_filter)
df_NT_level_2_3 = df_NT[df_NT['level_2_3_valid']==1].reset_index(drop=True)
df_TN['level_2_3_valid'] = df_TN['content'].apply(level_2_3_filter)
df_TN_level_2_3 = df_TN[df_TN['level_2_3_valid']==1].reset_index(drop=True)
df_KT['level_2_3_valid'] = df_KT['content'].apply(level_2_3_filter)
df_KT_level_2_3 = df_KT[df_KT['level_2_3_valid']==1].reset_index(drop=True)
df_LK['level_2_3_valid'] = df_LK['content'].apply(level_2_3_filter)
df_LK_level_2_3 = df_LK[df_LK['level_2_3_valid']==1].reset_index(drop=True)


df_HT_level_2_3['level2'] = df_HT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
df_OK_level_2_3['level2'] = df_OK_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
df_NT_level_2_3['level2'] = df_NT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
df_TN_level_2_3['level2'] = df_TN_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
df_KT_level_2_3['level2'] = df_KT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
df_LK_level_2_3['level2'] = df_LK_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))

df_HT_level_2_3['level2_len'] = df_HT_level_2_3.level2.apply(level_len)
df_OK_level_2_3['level2_len'] = df_OK_level_2_3.level2.apply(level_len)
df_NT_level_2_3['level2_len'] = df_NT_level_2_3.level2.apply(level_len)
df_TN_level_2_3['level2_len'] = df_TN_level_2_3.level2.apply(level_len)
df_KT_level_2_3['level2_len'] = df_KT_level_2_3.level2.apply(level_len)
df_LK_level_2_3['level2_len'] = df_LK_level_2_3.level2.apply(level_len)

df_HT_level_2_3['level3'] = df_HT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
df_OK_level_2_3['level3'] = df_OK_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
df_NT_level_2_3['level3'] = df_NT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
df_TN_level_2_3['level3'] = df_TN_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
df_KT_level_2_3['level3'] = df_KT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
df_LK_level_2_3['level3'] = df_LK_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))

df_HT_level_2_3['level3_len'] = df_HT_level_2_3['level3'].apply(level_len)
df_OK_level_2_3['level3_len'] = df_OK_level_2_3['level3'].apply(level_len)
df_NT_level_2_3['level3_len'] = df_NT_level_2_3['level3'].apply(level_len)
df_TN_level_2_3['level3_len'] = df_TN_level_2_3['level3'].apply(level_len)
df_KT_level_2_3['level3_len'] = df_KT_level_2_3['level3'].apply(level_len)
df_LK_level_2_3['level3_len'] = df_LK_level_2_3['level3'].apply(level_len)

data1 = [
['The Himalayan Times', df_HT.level_len.sum(), df_HT.shape[0]],
['Online Khabar', df_OK.level_len.sum(), df_OK.shape[0]],
['Nepali Times', df_NT.level_len.sum(), df_NT.shape[0]],
['Telegraph Nepal', df_TN.level_len.sum(), df_TN.shape[0]],
['Katmandu Tribune', df_KT.level_len.sum(), df_KT.shape[0]],
['Lokaantar', df_LK.level_len.sum(), df_LK.shape[0]]
] 

data2 = [
['The Himalayan Times', df_HT_level_2_3.level2_len.sum(), df_HT_level_2_3.shape[0]],
['Online Khabar', df_OK_level_2_3.level2_len.sum(), df_OK_level_2_3.shape[0]],
['Nepali Times', df_NT_level_2_3.level2_len.sum(), df_NT_level_2_3.shape[0]],
['Telegraph Nepal', df_TN_level_2_3.level2_len.sum(), df_TN_level_2_3.shape[0]],
['Katmandu Tribune', df_KT_level_2_3.level2_len.sum(), df_KT_level_2_3.shape[0]],
['Lokaantar', df_LK_level_2_3.level2_len.sum(), df_LK_level_2_3.shape[0]]
] 


data3 = [
['The Himalayan Times', df_HT_level_2_3.level3_len.sum(), df_HT_level_2_3.shape[0]],
['Online Khabar', df_OK_level_2_3.level3_len.sum(), df_OK_level_2_3.shape[0]],
['Nepali Times', df_NT_level_2_3.level3_len.sum(), df_NT_level_2_3.shape[0]],
['Telegraph Nepal', df_TN_level_2_3.level3_len.sum(), df_TN_level_2_3.shape[0]],
['Katmandu Tribune', df_KT_level_2_3.level3_len.sum(), df_KT_level_2_3.shape[0]],
['Lokaantar', df_LK_level_2_3.level3_len.sum(), df_LK_level_2_3.shape[0]]
] 

