import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

""" POP EST """

wd = "C:/Users/dwv530/OneDrive - University of Copenhagen/øster løgum/Github"
os.chdir(wd)

df = pd.read_csv('C:/Users/dwv530/OneDrive - University of Copenhagen/øster løgum/Github/ØL_register_events_by_village.csv')

df.drop(df.columns[:3], axis=1, inplace=True)
df = df.fillna(0)
#df['burials'] = df.iloc[:, [4,6,8,10,12,14,16,18,20,22]].sum(axis=1)
#df['births'] = df.iloc[:, [3,5,7,9,11,13,15,17,19,21]].sum(axis=1)
df['year'] = df['month'].str[:4]

""" calculates population for each day 1620-1660 
standard is from 1650-01-01 (ipop=11021) and HHP's
estimate of 656 (pop) """

def pop_est_parish(frame,pop=656,ipop=11021):
    for i in range(0,frame.shape[0]):
        if i < ipop:
            frame.loc[frame.index[i],'pop_est'] = pop - frame.loc[i:ipop]['øl_bir'].sum() + frame.loc[i:ipop]['øl_bur'].sum()
            frame.loc[frame.index[i],'pop_est_index'] = frame.loc[frame.index[i],'pop_est'] / frame.loc[frame.index[0],'pop_est'] * 100
        elif i == ipop:
            frame.loc[frame.index[i],'pop_est'] = pop
            frame.loc[frame.index[i],'pop_est_index'] = frame.loc[frame.index[i],'pop_est'] / frame.loc[frame.index[0],'pop_est'] * 100
        else:
            frame.loc[frame.index[i],'pop_est'] = pop + frame.loc[ipop:i]['øl_bir'].sum() - frame.loc[ipop:i]['øl_bur'].sum()
            frame.loc[frame.index[i],'pop_est_index'] = frame.loc[frame.index[i],'pop_est'] / frame.loc[frame.index[0],'pop_est'] * 100
    return frame['pop_est'], frame['pop_est_index']

df['pop_hhp'], df['pop_hhp_index'] = pop_est_parish(df)
df['pop_mlp'], df['pop_mlp_index'] = pop_est_parish(df,pop=757)
df['pop_mdh'], df['pop_mdh_index'] = pop_est_parish(df,pop=806,ipop=14308)
df['year'] = df.date.str[:4]
df = df.iloc[61:]

""" FIGUR 2 """

krigsår = ['1627','1628','1629','1643','1644','1645','1658','1659']

""" BURIALS """
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)
colors = ['#CCCCCC','#666666']
plt.rcParams["font.family"] = "serif"

bur = df.groupby('year').øl_bur.sum()
bur = bur.reset_index()
bur.columns = ['year','burials']
bur['burials_rm'] = bur['burials'].rolling(3).mean()
bur

""" BIRTHS """

bir = df.groupby('year').øl_bir.sum()
bir = bir.reset_index()
bir.columns = ['year','births']
bir['births_rm'] = bir['births'].rolling(3).mean()


""" FIGURE """
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)
plt.rcParams["font.family"] = "serif"

fig, axes = plt.subplots(3,1,figsize=(6,9))

#population estimate
g1 = sns.lineplot(data=df,x='year',y='pop_mlp',ax=axes[0],color='black')

g1.set_ylim(0,1000)
plt.setp(g1.get_xticklabels()[1::2], visible=False)
for t in g1.get_xticklabels():
    t.set_rotation(90)

axes[0].fill_between(['1627','1629'],[950,950],color='lightgrey')
axes[0].text('1624',950,'Kejserkrigen',backgroundcolor='white',size=9)
axes[0].fill_between(['1644','1645'],[950,950],color='lightgrey')
axes[0].text('1639',950,'Torstenssonfejden',backgroundcolor='white',size=9)
axes[0].fill_between(['1657','1659'],[950,950],color='lightgrey')
axes[0].text('1652',950,'Karl Gustav-krigene',backgroundcolor='white',size=9)

lab1 = Line2D([0], [0], color='black', label='Årligt gennemsnit')
axes[0].legend(handles=[lab1],loc='lower center',bbox_to_anchor=(0.5,-0.55),
              edgecolor='none',prop={"size":10})

axes[0].set_ylabel('Estimeret folketal')
axes[0].set_xlabel('')

#births
g2 = sns.barplot(data=bir,x='year',y='births',ax=axes[1],dodge=False,color='grey',linewidth=0)
g3 = sns.lineplot(data=bir,x='year',y='births_rm',ax=axes[1],color='black')
for t in g2.get_xticklabels():
    t.set_rotation(90)

g2.set_ylim(0,40)
plt.setp(g2.get_xticklabels()[1::2], visible=False)

lab1 = Line2D([0], [0], color='black', label='Tre-årigt gennemsnit')
axes[1].legend(handles=[lab1],loc='lower center',bbox_to_anchor=(0.5,-0.55),
              edgecolor='none',prop={"size":10})

axes[1].fill_between(['1627','1629'],[40,40],color='lightgrey')
axes[1].text('1624',40,'Kejserkrigen',backgroundcolor='white',size=9)
axes[1].fill_between(['1644','1645'],[40,40],color='lightgrey')
axes[1].text('1639',40,'Torstenssonfejden',backgroundcolor='white',size=9)
axes[1].fill_between(['1657','1659'],[40,40],color='lightgrey')
axes[1].text('1652',40,'Karl Gustav-krigene',backgroundcolor='white',size=9)

axes[1].set_ylabel('Antal dåb')
axes[1].set_xlabel('')

#burials
g4 = sns.barplot(data=bur,x='year',y='burials',ax=axes[2],dodge=False,color='grey',linewidth=0)
g5 = sns.lineplot(data=bur,x='year',y='burials_rm',ax=axes[2],color='black')
for t in g4.get_xticklabels():
    t.set_rotation(90)

g4.set_ylim(0,200)
plt.setp(g4.get_xticklabels()[1::2], visible=False)

lab1 = Line2D([0], [0], color='black', label='Tre-årigt gennemsnit')
axes[2].legend(handles=[lab1],loc='lower center',bbox_to_anchor=(0.5,-0.55),
              edgecolor='none',prop={"size":10})

axes[2].fill_between(['1627','1629'],[200,200],color='lightgrey')
axes[2].text('1623',205,'Kejserkrigen',backgroundcolor='white',size=9)
axes[2].fill_between(['1644','1645'],[200,200],color='lightgrey')
axes[2].text('1639',205,'Torstenssonfejden',backgroundcolor='white',size=9)
axes[2].fill_between(['1657','1659'],[200,200],color='lightgrey')
axes[2].text('1652',205,'Karl Gustav-krigene',backgroundcolor='white',size=9)

axes[2].set_ylabel('Antal begravelser')
axes[2].set_xlabel('')

axes[0].text('1620',880,'A')
axes[1].text('1620',35,'B')
axes[2].text('1620',170,'C')

fig.tight_layout()
fig.savefig('figur2.png', format='png', dpi=600,bbox_inches='tight')
