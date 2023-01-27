import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.lines import Line2D

wd = "C:/Users/dwv530/OneDrive - University of Copenhagen/øster løgum/Github"
os.chdir(wd)

df = pd.read_csv('C:/Users/dwv530/OneDrive - University of Copenhagen/øster løgum/Github/ØL_register_events_by_village.csv')
df.drop(df.columns[:2], axis=1, inplace=True)
df['year'] = df['month'].str[:4]
df = df.iloc[61:]

l = list(df.columns)
n = []
for s in l:
    if '_' in s:
        s = s.split('_')[1]+'_'+s.split('_')[0]
    n.append(s)

df.columns = n
d = pd.wide_to_long(df,stubnames=['bir','bur','mar'],j='village',i=['index'],sep='_',suffix=r'\w+')
d = d.reset_index()
d[d.year.str.contains('1657')]
pop_dict = dict([('an', 6),('ge', 260),('he', 5),('ho', 155),('ja', 64),('ko', 9),
                 ('le', 35),('lø', 116),('ru', 89),('ty', 12),('øl', 757),('få', 6)])

def pop_est_village(frame,ipop=11021):
    
    df_popest = pd.DataFrame()
    for v in set(frame['village']):
        f = frame
        f = f[f['village'] == v]
        f = f.set_index('index')
        pop = pop_dict[v]
    
        for i in range(0,f.shape[0]):
            if i < ipop:
                f.loc[f.index[i],'pop_est'] = pop - f.loc[i:ipop]['bir'].sum() + f.loc[i:ipop]['bur'].sum()
                f.loc[f.index[i],'pop_est_index'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[0],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1643'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[8402],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1657'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[13516],'pop_est'] * 100
            elif i == ipop:
                f.loc[f.index[i],'pop_est'] = pop
                f.loc[f.index[i],'pop_est_index'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[0],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1643'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[8402],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1657'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[13516],'pop_est'] * 100
            else:
                f.loc[f.index[i],'pop_est'] = pop + f.loc[ipop:i]['bir'].sum() - f.loc[ipop:i]['bur'].sum()
                f.loc[f.index[i],'pop_est_index'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[0],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1643'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[8402],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1657'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[13516],'pop_est'] * 100
        
        df_popest = pd.concat([df_popest,f],axis=0)
    
    return df_popest

pop = pop_est_village(d)


""" Figur 4 """

custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)
plt.rcParams["font.family"] = "serif"

toplot = pop.groupby(['village','year']).pop_est_index.mean()
toplot = toplot.reset_index()
toplot = toplot[toplot.year.isin(['1620','1621','1622','1623','1624','1625','1626','1627','1628','1629','1630',
                                  '1631','1632','1633','1634','1635','1636','1637','1638','1639','1640','1641','1642'])]

f,ax = plt.subplots(figsize=(6,4))
g1 = sns.lineplot(data=toplot[toplot.village=='ge'],x='year',y='pop_est_index',linestyle='-',color='black',
             linewidth='2',ax=ax)
g2 = sns.lineplot(data=toplot[toplot.village=='ho'],x='year',y='pop_est_index',linestyle=':',color='black',
             linewidth='2',ax=ax)
g3 = sns.lineplot(data=toplot[toplot.village=='lø'],x='year',y='pop_est_index',linestyle='--',color='black',
             linewidth='2',ax=ax)
g4 = sns.lineplot(data=toplot[toplot.village=='ru'],x='year',y='pop_est_index',linestyle='-',color='grey',
             linewidth='2',ax=ax)
g5 = sns.lineplot(data=toplot[toplot.village=='ja'],x='year',y='pop_est_index',linestyle=':',color='grey',
             linewidth='2',ax=ax)
g6 = sns.lineplot(data=toplot[toplot.village=='le'],x='year',y='pop_est_index',linestyle='--',color='grey',
             linewidth='2',ax=ax)

plt.setp(g1.get_xticklabels()[1::2], visible=False)
for t in g1.get_xticklabels():
    t.set_rotation(90)

g1.set_ylim(30,140)
ax.set_ylabel('Estimeret folketal (indeks=1620)')
ax.set_xlabel('')
ax.fill_between(['1627','1629'],[135,135],color='lightgrey')
ax.text('1626',135,'Kejserkrigen',backgroundcolor='white',size=9)

lab1 = Line2D([0], [0], color='black', linestyle='-', label='Genner')
lab2 = Line2D([0], [0], color='black', linestyle=':', label='Hovslund')
lab3 = Line2D([0], [0], color='black', linestyle='--', label='Løgum')
lab4 = Line2D([0], [0], color='grey', linestyle='-', label='Rugbjerg')
lab5 = Line2D([0], [0], color='grey', linestyle=':', label='Jarup')
lab6 = Line2D([0], [0], color='grey', linestyle='--', label='Lerskov')

plt.figlegend(handles=[lab1,lab2,lab3,lab4,lab5,lab6],loc='lower center',bbox_to_anchor=(0.5,-.17),
              edgecolor='none',prop={"size":9},ncol=2)

f.tight_layout()
f.savefig('pop_est_village_index_1620-1642.png', format='png', dpi=600,bbox_inches='tight')


""" Figur 5 """

toplot = pop.groupby(['village','year']).pop_est_index_1643.mean()
toplot = toplot.reset_index()
toplot = toplot[toplot.year.isin(['1643','1644','1645','1646','1647','1648','1649','1650','1651','1652',
                                  '1653','1654','1655','1656'])]

f,ax = plt.subplots(figsize=(6,4))
g1 = sns.lineplot(data=toplot[toplot.village=='ge'],x='year',y='pop_est_index_1643',linestyle='-',color='black',
             linewidth='2',ax=ax)
g2 = sns.lineplot(data=toplot[toplot.village=='ho'],x='year',y='pop_est_index_1643',linestyle=':',color='black',
             linewidth='2',ax=ax)
g3 = sns.lineplot(data=toplot[toplot.village=='lø'],x='year',y='pop_est_index_1643',linestyle='--',color='black',
             linewidth='2',ax=ax)
g4 = sns.lineplot(data=toplot[toplot.village=='ru'],x='year',y='pop_est_index_1643',linestyle='-',color='grey',
             linewidth='2',ax=ax)
g5 = sns.lineplot(data=toplot[toplot.village=='ja'],x='year',y='pop_est_index_1643',linestyle=':',color='grey',
             linewidth='2',ax=ax)
g6 = sns.lineplot(data=toplot[toplot.village=='le'],x='year',y='pop_est_index_1643',linestyle='--',color='grey',
             linewidth='2',ax=ax)

plt.setp(g1.get_xticklabels()[1::2], visible=False)
for t in g1.get_xticklabels():
    t.set_rotation(90)

g1.set_ylim(70,130)
ax.set_ylabel('Estimeret folketal (indeks=1643)')
ax.set_xlabel('')
ax.fill_between(['1644','1645'],[125,125],color='lightgrey')
ax.text('1643',125,'Torstenssonkrigen',backgroundcolor='white',size=9)

lab1 = Line2D([0], [0], color='black', linestyle='-', label='Genner')
lab2 = Line2D([0], [0], color='black', linestyle=':', label='Hovslund')
lab3 = Line2D([0], [0], color='black', linestyle='--', label='Løgum')
lab4 = Line2D([0], [0], color='grey', linestyle='-', label='Rugbjerg')
lab5 = Line2D([0], [0], color='grey', linestyle=':', label='Jarup')
lab6 = Line2D([0], [0], color='grey', linestyle='--', label='Lerskov')

plt.figlegend(handles=[lab1,lab2,lab3,lab4,lab5,lab6],loc='lower center',bbox_to_anchor=(0.5,-.17),
              edgecolor='none',prop={"size":9},ncol=2)

f.tight_layout()
f.savefig('pop_est_village_index_1643-1656.png', format='png', dpi=600,bbox_inches='tight')


""" Figur 6 """
import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 10

toplot = pop.groupby(['village','month']).pop_est_index_1657.mean()
toplot = toplot.reset_index()

months = toplot.month[-60:-12]
toplot = toplot[toplot.month.isin(months)]
toplot.month = toplot.month.str[:7]

f,ax = plt.subplots(figsize=(6,4))
g1 = sns.lineplot(data=toplot[toplot.village=='ge'],x='month',y='pop_est_index_1657',linestyle='-',color='black',
             linewidth='2',ax=ax)
g2 = sns.lineplot(data=toplot[toplot.village=='ho'],x='month',y='pop_est_index_1657',linestyle=':',color='black',
             linewidth='2',ax=ax)
g3 = sns.lineplot(data=toplot[toplot.village=='lø'],x='month',y='pop_est_index_1657',linestyle='--',color='black',
             linewidth='2',ax=ax)
g4 = sns.lineplot(data=toplot[toplot.village=='ru'],x='month',y='pop_est_index_1657',linestyle='-',color='grey',
             linewidth='2',ax=ax)
g5 = sns.lineplot(data=toplot[toplot.village=='ja'],x='month',y='pop_est_index_1657',linestyle=':',color='grey',
             linewidth='2',ax=ax)
g6 = sns.lineplot(data=toplot[toplot.village=='le'],x='month',y='pop_est_index_1657',linestyle='--',color='grey',
             linewidth='2',ax=ax)

plt.setp(g1.get_xticklabels()[1::2], visible=False)
for t in g1.get_xticklabels():
    t.set_rotation(90)

g1.set_ylim(40,120)
ax.set_ylabel('Estimeret folketal (indeks=1657-01)')
ax.set_xlabel('')
ax.fill_between(['1659-07','1660-05'],[115,115],color='white',facecolor='lightgrey',hatch='/')
ax.fill_between(['1657-08','1659-08'],[115,115],color='lightgrey')
ax.text('1657-08',117,'              Karl Gustav-krigene                  ',backgroundcolor='white',size=9)

lab1 = Line2D([0], [0], color='black', linestyle='-', label='Genner')
lab2 = Line2D([0], [0], color='black', linestyle=':', label='Hovslund')
lab3 = Line2D([0], [0], color='black', linestyle='--', label='Løgum')
lab4 = Line2D([0], [0], color='grey', linestyle='-', label='Rugbjerg')
lab5 = Line2D([0], [0], color='grey', linestyle=':', label='Jarup')
lab6 = Line2D([0], [0], color='grey', linestyle='--', label='Lerskov')

plt.figlegend(handles=[lab1,lab2,lab3,lab4,lab5,lab6],loc='lower center',bbox_to_anchor=(0.5,-.17),
              edgecolor='none',prop={"size":9},ncol=2)

f.tight_layout()
f.savefig('pop_est_village_index_1657-1660.png', format='png', dpi=600,bbox_inches='tight')


