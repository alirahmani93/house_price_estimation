# -*- coding: utf-8 -*-
"""KeyWord-parnian.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16BM27qSidOptvi1C1FA5t6Z6TZCVkBoG

### **Look for keywords**
"""

df['Contains_teras'] = df['title'].str.contains('تراس|بالکن', regex=True)
df['Contains_komod'] = df['title'].str.contains('کمد')
df['Contains_master'] = df['title'].str.contains('مستر')
df['Contains_kabinet'] = df['title'].str.contains('کابینت')
df['Contains_metro'] = df['title'].str.contains('مترو')
df['Contains_vam'] = df['title'].str.contains('وام')
df['Contains_moshaat'] = df['title'].str.contains('مشاعات')
df['Contains_vahedi'] = df['title'].str.contains('واحدی')
df['Contains_sanad'] = df['title'].str.contains('سند')
df['Contains_noor'] = df['title'].str.contains('نور')
df['Contains_salon'] = df['title'].str.contains('سالن')
df['Contains_labi'] = df['title'].str.contains('لابی')
df['Contains_naghshe'] = df['title'].str.contains('نقشه')
df['Contains_noori'] = df['title'].str.contains('نوری')
df['Contains_material'] = df['title'].str.contains('متریال')
df['Contains_noorgir'] = df['title'].str.contains('نورگیر')

"""### **[Combining the results of "balcony", "teras" into "balcony_total"]**"""

import numpy as np

df['balcony_total'] = np.where((df['balcony'] == True) & (df['Contains_teras'] == True), True,
                               np.where((df['balcony'] == True) & (df['Contains_teras'] == False), True,
                                        np.where((df['balcony'] == False) & (df['Contains_teras'] == True), True,
                                                 np.where((df['balcony'].isnull()) & (df['Contains_teras'] == True), True,
                                                          np.where((df['balcony'].isnull()) & (df['Contains_teras'] == False), False, False)))))

"""### **[Combining the results of "noor", "noori", and "noorgir" into "noor_total"]**"""

df['noor_total'] = ((df['Contains_noor'] == True) & (df['Contains_noori'] == False) & (df['Contains_noorgir'] == False))|((df['Contains_noor'] == False) & (df['Contains_noori'] == True) & (df['Contains_noorgir'] == False))|((df['Contains_noor'] == False) & (df['Contains_noori'] == False) & (df['Contains_noorgir'] == True))|((df['Contains_noor'] == True) & (df['Contains_noori'] == True) & (df['Contains_noorgir'] == False))|((df['Contains_noor'] == True) & (df['Contains_noori'] == False) & (df['Contains_noorgir'] == True))|((df['Contains_noor'] == False) & (df['Contains_noori'] == True) & (df['Contains_noorgir'] == True))|((df['Contains_noor'] == True) & (df['Contains_noori'] == True) & (df['Contains_noorgir'] == True))