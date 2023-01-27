import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

wd = "C:/Users/dwv530/OneDrive - University of Copenhagen/øster løgum/Github"
os.chdir(wd)

df = pd.read_csv('ØL_register_events_by_village.csv')
df.rename(columns={ df.columns[0]: "index" }, inplace = True)
df['year'] = df['month'].str[:4]

df = df[df.year.isin(['1620','1621','1622','1623','1624','1625','1626','1627','1628','1629','1630',
                                  '1631','1632','1633','1634','1635','1636','1637','1638','1639','1640','1641','1642'])]

#window size of rolling mean
r = 3

#hele sognet
øl_bir = df.groupby('year').øl_bir.sum().reset_index()
øl_bir_m = df.groupby('year').øl_bir.sum().rolling(r,center=True).mean().reset_index()
øl_bur = df.groupby('year').øl_bur.sum().reset_index()
øl_bur_m = df.groupby('year').øl_bur.sum().rolling(r,center=True).mean().reset_index()

#genner
ge_bir = df.groupby('year').ge_bir.sum().reset_index()
ge_bir_m = df.groupby('year').ge_bir.sum().rolling(r,center=True).mean().reset_index()
ge_bur = df.groupby('year').ge_bur.sum().reset_index()
ge_bur_m = df.groupby('year').ge_bur.sum().rolling(r,center=True).mean().reset_index()

#hovslund
ho_bir = df.groupby('year').ho_bir.sum().reset_index()
ho_bir_m = df.groupby('year').ho_bir.sum().rolling(r,center=True).mean().reset_index()
ho_bur = df.groupby('year').ho_bur.sum().reset_index()
ho_bur_m = df.groupby('year').ho_bur.sum().rolling(r,center=True).mean().reset_index()

#løgum
lø_bir = df.groupby('year').lø_bir.sum().reset_index()
lø_bir_m = df.groupby('year').lø_bir.sum().rolling(r,center=True).mean().reset_index()
lø_bur = df.groupby('year').lø_bur.sum().reset_index()
lø_bur_m = df.groupby('year').lø_bur.sum().rolling(r,center=True).mean().reset_index()

#rugbjerg
ru_bir = df.groupby('year').ru_bir.sum().reset_index()
ru_bir_m = df.groupby('year').ru_bir.sum().rolling(r,center=True).mean().reset_index()
ru_bur = df.groupby('year').ru_bur.sum().reset_index()
ru_bur_m = df.groupby('year').ru_bur.sum().rolling(r,center=True).mean().reset_index()

#jarup
ja_bir = df.groupby('year').ja_bir.sum().reset_index()
ja_bir_m = df.groupby('year').ja_bir.sum().rolling(r,center=True).mean().reset_index()
ja_bur = df.groupby('year').ja_bur.sum().reset_index()
ja_bur_m = df.groupby('year').ja_bur.sum().rolling(r,center=True).mean().reset_index()

#lerskov
le_bir = df.groupby('year').le_bir.sum().reset_index()
le_bir_m = df.groupby('year').le_bir.sum().rolling(r,center=True).mean().reset_index()
le_bur = df.groupby('year').le_bur.sum().reset_index()
le_bur_m = df.groupby('year').le_bur.sum().rolling(r,center=True).mean().reset_index()

""" FIGUR 3 """
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)
plt.rcParams["font.family"] = "serif"

fig, ax = plt.subplots(figsize=(6,4))
g1 = sns.lineplot(data=ge_bur_m,x='year',y='ge_bur',ax=ax,color='black',linestyle='-')
g2 = sns.lineplot(data=ho_bur_m,x='year',y='ho_bur',ax=ax,color='black',linestyle=':')
g3 = sns.lineplot(data=lø_bur_m,x='year',y='lø_bur',ax=ax,color='black',linestyle='--')
g4 = sns.lineplot(data=ru_bur_m,x='year',y='ru_bur',ax=ax,color='grey',linestyle='-')
g5 = sns.lineplot(data=ja_bur_m,x='year',y='ja_bur',ax=ax,color='grey',linestyle=':')
g6 = sns.lineplot(data=le_bur_m,x='year',y='le_bur',ax=ax,color='grey',linestyle='--')

for t in g1.get_xticklabels():
    t.set_rotation(90)
plt.setp(g1.get_xticklabels()[1::2], visible=False)

ax.set_ylabel('Begravelser (treårigt gennemsnit)')
ax.set_xlabel('')

ax.set_ylim(0,24)

fig.tight_layout()

lab1 = Line2D([0], [0], color='black', linestyle='-', label='Genner')
lab2 = Line2D([0], [0], color='black', linestyle=':', label='Hovslund')
lab3 = Line2D([0], [0], color='black', linestyle='--', label='Løgum')
lab4 = Line2D([0], [0], color='grey', linestyle='-', label='Rugbjerg')
lab5 = Line2D([0], [0], color='grey', linestyle=':', label='Jarup')
lab6 = Line2D([0], [0], color='grey', linestyle='--', label='Lerskov')

plt.figlegend(handles=[lab1,lab2,lab3,lab4,lab5,lab6],loc='lower center',bbox_to_anchor=(0.5,-.17),
              edgecolor='none',prop={"size":10},ncol=2)

fig.tight_layout()
fig.savefig('burials_1620-42_rolling.png', format='png', dpi=600,bbox_inches='tight')





















