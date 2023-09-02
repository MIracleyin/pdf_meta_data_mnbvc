#%%
import pikepdf
import sys
from pathlib import Path
import jsonlines
from tqdm import tqdm
import pandas as pd

#%%
df = pd.read_json('pdf_meta_info.jsonl', orient='records', lines=True)

#%%
non_null_count = df.count()
ratio = non_null_count / len(df)
#%%
import matplotlib.pyplot as plt
# plt.bar(ratio.index, ratio.values)
ratio[ratio > 0.7].plot.bar()
# plt.show()
plt.xlabel('Columns')
plt.show()
#%%
df['/Producer'].count()
# %%
producer_null_count = df['/Producer'].value_counts()
ratio = producer_null_count / df['/Producer'].count()
ratio[ratio > 0.05].plot.bar()
plt.xlabel('/Producer')
plt.show()
# %%
