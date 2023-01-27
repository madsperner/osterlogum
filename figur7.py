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

#som udgangspunkt er der ingen migranter ind eller ud i vores regnestykke
d['migr_in'] = 0
d['migr_out'] = 0

""" ESTIMATET """

def pop_est_village_migr(frame,ipop=11021):
    
    df_popest = pd.DataFrame()
    for v in set(frame['village']):
        f = frame
        f = f[f['village'] == v]
        f = f.set_index('index')
        pop = pop_dict[v]
    
        for i in range(0,f.shape[0]):
            if i < ipop:
                f.loc[f.index[i],'pop_est'] = pop - f.loc[i:ipop]['bir'].sum() - f.loc[i:ipop]['migr_in'].sum() + f.loc[i:ipop]['bur'].sum() + f.loc[i:ipop]['migr_out'].sum()
                f.loc[f.index[i],'pop_est_index'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[0],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1631'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[4019],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1643'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[8402],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1657'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[13516],'pop_est'] * 100
            elif i == ipop:
                f.loc[f.index[i],'pop_est'] = pop
                f.loc[f.index[i],'pop_est_index'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[0],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1631'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[4019],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1643'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[8402],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1657'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[13516],'pop_est'] * 100
            else:
                f.loc[f.index[i],'pop_est'] = pop + f.loc[ipop:i]['bir'].sum() - f.loc[ipop:i]['bur'].sum()
                f.loc[f.index[i],'pop_est_index'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[0],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1631'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[4019],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1643'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[8402],'pop_est'] * 100
                f.loc[f.index[i],'pop_est_index_1657'] = f.loc[f.index[i],'pop_est'] / f.loc[f.index[13516],'pop_est'] * 100
        
        df_popest = pd.concat([df_popest,f],axis=0)
    
    return df_popest

#Her laves det oprindelige estimat - ingen migration
pop = pop_est_village_migr(d)



""" scenarie 1 - gårde, som ikke besattes lokalt, overtages 50*% af folk fra andre landsbyer, 50% udensogns """

#når nogen overtager en gård og derfor migrerer ind eller ud af landsbyen, tager de et antal personer, p, med
#her er det sat til 4 i gennemsnit
d1 = d
p = 5

#her tilføjer vi p personer per tomme gård SOM IKKE BESATTES AF FOLK FRA LANDSBYEN
d1.loc[(d1.village=='lø')&(d1.date=='1629-08-01'),'migr_in'] = 2*p
d1.loc[(d1.village=='ru')&(d1.date=='1629-08-01'),'migr_in'] = 5*p
d1.loc[(d1.village=='ja')&(d1.date=='1629-08-01'),'migr_in'] = 3*p
d1.loc[(d1.village=='ho')&(d1.date=='1629-08-01'),'migr_in'] = 3*p
d1.loc[(d1.village=='ge')&(d1.date=='1629-08-01'),'migr_in'] = 0*p
d1.loc[(d1.village=='øl')&(d1.date=='1629-08-01'),'migr_in'] = 7*p

#her fjerner vi personer fra landsbyerne, som i et hypotetisk scenarie har overtaget andre gårde
d1.loc[(d1.village=='lø')&(d1.date=='1629-08-01'),'migr_out'] = 1*p
d1.loc[(d1.village=='ru')&(d1.date=='1629-08-01'),'migr_out'] = 0*p
d1.loc[(d1.village=='ja')&(d1.date=='1629-08-01'),'migr_out'] = 1*p
d1.loc[(d1.village=='ho')&(d1.date=='1629-08-01'),'migr_out'] = 2*p
d1.loc[(d1.village=='ge')&(d1.date=='1629-08-01'),'migr_out'] = 3*p

pop1 = pop_est_village_migr(d1)

""" scenarie 2 - gårde, som ikke besattes lokalt, overtages 100% af folk fra andre landsbyer, 0% udensogns """

d2 = d
p = 5

#her tilføjer vi p personer per tomme gård SOM IKKE BESATTES AF FOLK FRA LANDSBYEN
d2.loc[(d2.village=='lø')&(d2.date=='1629-08-01'),'migr_in'] = 2*p
d2.loc[(d2.village=='ru')&(d2.date=='1629-08-01'),'migr_in'] = 5*p
d2.loc[(d2.village=='ja')&(d2.date=='1629-08-01'),'migr_in'] = 3*p
d2.loc[(d2.village=='ho')&(d2.date=='1629-08-01'),'migr_in'] = 3*p
d2.loc[(d2.village=='ge')&(d2.date=='1629-08-01'),'migr_in'] = 0*p
d2.loc[(d2.village=='øl')&(d2.date=='1629-08-01'),'migr_in'] = 0*p

#her fjerner vi personer fra landsbyerne, som i et hypotetisk scenarie har overtaget andre gårde
d2.loc[(d2.village=='lø')&(d2.date=='1629-08-01'),'migr_out'] = 2*p
d2.loc[(d2.village=='ru')&(d2.date=='1629-08-01'),'migr_out'] = 0*p
d2.loc[(d2.village=='ja')&(d2.date=='1629-08-01'),'migr_out'] = 2*p
d2.loc[(d2.village=='ho')&(d2.date=='1629-08-01'),'migr_out'] = 4*p
d2.loc[(d2.village=='ge')&(d2.date=='1629-08-01'),'migr_out'] = 5*p

pop2 = pop_est_village_migr(d2)

""" scenarie 3 - gårde, som ikke besattes lokalt, overtages 100% af folk fra andre sogne """

d3 = d
p = 5

#her tilføjer vi p personer per tomme gård SOM IKKE BESATTES AF FOLK FRA LANDSBYEN
d3.loc[(d3.village=='lø')&(d3.date=='1629-08-01'),'migr_in'] = 2*p
d3.loc[(d3.village=='ru')&(d3.date=='1629-08-01'),'migr_in'] = 5*p
d3.loc[(d3.village=='ja')&(d3.date=='1629-08-01'),'migr_in'] = 3*p
d3.loc[(d3.village=='ho')&(d3.date=='1629-08-01'),'migr_in'] = 3*p
d3.loc[(d3.village=='ge')&(d3.date=='1629-08-01'),'migr_in'] = 0*p
d3.loc[(d3.village=='øl')&(d3.date=='1629-08-01'),'migr_in'] = 13*p

#her fjerner vi personer fra landsbyerne, som i et hypotetisk scenarie har overtaget andre gårde
d3.loc[(d3.village=='lø')&(d3.date=='1629-08-01'),'migr_out'] = 0*p
d3.loc[(d3.village=='ru')&(d3.date=='1629-08-01'),'migr_out'] = 0*p
d3.loc[(d3.village=='ja')&(d3.date=='1629-08-01'),'migr_out'] = 0*p
d3.loc[(d3.village=='ho')&(d3.date=='1629-08-01'),'migr_out'] = 0*p
d3.loc[(d3.village=='ge')&(d3.date=='1629-08-01'),'migr_out'] = 0*p

pop3 = pop_est_village_migr(d3)


""" Figur 7a """

custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)
plt.rcParams["font.family"] = "serif"

toplot = pop1.groupby(['village','year']).pop_est_index.mean()
toplot = toplot.reset_index()

f,ax = plt.subplots(figsize=(7,4))
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

g1.set_ylim(30,200)
ax.set_ylabel('Estimeret folketal (Indeks=1620)')
ax.set_xlabel('')
ax.fill_between(['1627','1629'],[190,190],color='lightgrey')
ax.text('1625',190,'Kejserkrigen',backgroundcolor='white',size=9)
ax.fill_between(['1644','1645'],[190,190],color='lightgrey')
ax.text('1640',190,'Torstenssonkrigen',backgroundcolor='white',size=9)
ax.fill_between(['1657','1660'],[190,190],color='lightgrey')
ax.text('1653',190,'Karl Gustav-krigene',backgroundcolor='white',size=9)


lab1 = Line2D([0], [0], color='black', linestyle='-', label='Genner')
lab2 = Line2D([0], [0], color='black', linestyle=':', label='Hovslund')
lab3 = Line2D([0], [0], color='black', linestyle='--', label='Løgum')
lab4 = Line2D([0], [0], color='grey', linestyle='-', label='Rugbjerg')
lab5 = Line2D([0], [0], color='grey', linestyle=':', label='Jarup')
lab6 = Line2D([0], [0], color='grey', linestyle='--', label='Lerskov')

plt.figlegend(handles=[lab1,lab2,lab3,lab4,lab5,lab6],loc='lower center',bbox_to_anchor=(0.5,-.17),
              edgecolor='none',prop={"size":10},ncol=2)

f.tight_layout()
f.savefig('pop_est_village_index_1620-1660.png', format='png', dpi=600,bbox_inches='tight')


""" Figur 7b """

custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)
plt.rcParams["font.family"] = "serif"

toplot = pop.groupby(['village','year']).pop_est_index_1631.mean()
toplot = toplot.reset_index()
toplot = toplot[~toplot.year.isin(['1626','1627','1628','1629','1630'])]

f,ax = plt.subplots(figsize=(7,4))
g1 = sns.lineplot(data=toplot[toplot.village=='ge'],x='year',y='pop_est_index_1631',linestyle='-',color='black',
             linewidth='2',ax=ax)
g2 = sns.lineplot(data=toplot[toplot.village=='ho'],x='year',y='pop_est_index_1631',linestyle=':',color='black',
             linewidth='2',ax=ax)
g3 = sns.lineplot(data=toplot[toplot.village=='lø'],x='year',y='pop_est_index_1631',linestyle='--',color='black',
             linewidth='2',ax=ax)
g4 = sns.lineplot(data=toplot[toplot.village=='ru'],x='year',y='pop_est_index_1631',linestyle='-',color='grey',
             linewidth='2',ax=ax)
g5 = sns.lineplot(data=toplot[toplot.village=='ja'],x='year',y='pop_est_index_1631',linestyle=':',color='grey',
             linewidth='2',ax=ax)
g6 = sns.lineplot(data=toplot[toplot.village=='le'],x='year',y='pop_est_index_1631',linestyle='--',color='grey',
             linewidth='2',ax=ax)

plt.setp(g1.get_xticklabels()[1::2], visible=False)
for t in g1.get_xticklabels():
    t.set_rotation(90)

g1.set_ylim(30,180)
ax.set_ylabel('Estimeret folketal (Indeks=1620)')
ax.set_xlabel('')
#ax.fill_between(['1627','1629'],[190,190],color='lightgrey')
#ax.text('1625',190,'Kejserkrigen',backgroundcolor='white',size=9)
ax.fill_between(['1644','1645'],[170,170],color='lightgrey')
ax.text('1640',170,'Torstenssonkrigen',backgroundcolor='white',size=9)
ax.fill_between(['1657','1660'],[170,170],color='lightgrey')
ax.text('1653',170,'Karl Gustav-krigene',backgroundcolor='white',size=9)


lab1 = Line2D([0], [0], color='black', linestyle='-', label='Genner')
lab2 = Line2D([0], [0], color='black', linestyle=':', label='Hovslund')
lab3 = Line2D([0], [0], color='black', linestyle='--', label='Løgum')
lab4 = Line2D([0], [0], color='grey', linestyle='-', label='Rugbjerg')
lab5 = Line2D([0], [0], color='grey', linestyle=':', label='Jarup')
lab6 = Line2D([0], [0], color='grey', linestyle='--', label='Lerskov')

plt.figlegend(handles=[lab1,lab2,lab3,lab4,lab5,lab6],loc='lower center',bbox_to_anchor=(0.5,-.17),
              edgecolor='none',prop={"size":10},ncol=2)

f.tight_layout()
f.savefig('pop_est_village_index_1620-1660_migr.png', format='png', dpi=600,bbox_inches='tight')



