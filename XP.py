#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd
import numpy as np


# In[51]:


df = pd.read_excel(r'C:\Users\Lucas\Downloads\FundosXP.xlsx')


# In[53]:


for col in range(0,len(df.columns)):
    for row in range(0,len(df)):
        if df.iloc[row,col] == '-':
            df.iloc[row,col] = np.nan     


# In[99]:


for col in range(0,len(df.columns)):
    for row in range(0,len(df)):
        if df.iloc[row,col] == 'N/D':
            df.iloc[row,col] = np.nan     


# In[74]:


df['cot_resgate'] = [s.replace('\n\n',' ') for s in df['cot_resgate']]
df['liq_resgate'] = [s.replace('\n\n',' ') for s in df['liq_resgate']]


# In[122]:


df['taxa_adm'] = df['taxa_adm'].astype(float)
df['taxa_risco'] = df['taxa_risco'].astype(int)
df['rent_12_meses'] = df['rent_12_meses'].astype(float)
df['rent_24_meses'] = df['rent_24_meses'].astype(float)
df['rent_36_meses'] = df['rent_36_meses'].astype(float)
df['taxa_performance'] = df['taxa_performance'].astype(float)
df['data_inicio'] = pd.to_datetime(df['data_inicio'])


# In[123]:


df.info()


# In[127]:


df.to_excel('FundosXPv2.xlsx', index=False)


# In[ ]:




