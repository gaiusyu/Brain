import pandas as pd

df_example = pd.read_csv('../logs/Android/Andriod_2k.log_templates.csv',
                         encoding='UTF-8', header=0)
structured = df_example['EventTemplate']

lines = open('../Parseresult/Androidresult.csv')
line = lines.read()
print()