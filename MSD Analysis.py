#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd


# In[8]:


ball_by_ball_comp =pd.read_csv(r'C:\Users\KUNAL\Desktop\Collearn\deliveries.csv')
matches = pd.read_csv(r'C:\Users\KUNAL\Desktop\Collearn\matches.csv')


# In[10]:


ball_by_ball_comp


# In[11]:


msd_balls = ball_by_ball_comp.loc[(ball_by_ball_comp['batsman'] == 'MS Dhoni')| (ball_by_ball_comp['non_striker'] == 'MS Dhoni')]


# In[12]:


msd_balls


# In[13]:


matches


# In[14]:


msd_ids = msd_balls['match_id'].unique().tolist()


# In[15]:


msd_ids


# In[16]:


msd_matches=[]
for match_id in msd_ids:
    df_id = matches.loc[matches['id'] == match_id]
    msd_matches.append(df_id.iloc[0])


# In[17]:


msd_matches


# In[18]:


dhoni_matches = pd.DataFrame(msd_matches)


# In[19]:


dhoni_matches


# In[20]:


len(dhoni_matches)


# In[21]:


dhoni_matches['date'] = pd.to_datetime(dhoni_matches['date'])


# In[22]:


dhoni_matches = dhoni_matches.sort_values(by = 'date')


# In[23]:


dhoni_matches


# In[24]:


msd_ids = dhoni_matches['id'].tolist()


# In[25]:


msd_ids


# In[26]:


match_details = []
for match_id in msd_ids:
    df = msd_balls[msd_balls['match_id'] == match_id]
    match_details.append(df)


# In[27]:


match_details


# In[29]:


runs = []

for match in match_details:
    runs_bat = match[match['batsman'] == 'MS Dhoni'] ['batsman_runs'].sum()
    runs.append(runs_bat)


# In[30]:


runs


# In[31]:


balls = []
for match in match_details:
        balls_faced = match[(match['batsman'] == 'MS Dhoni') & (match['wide_runs'] == 0)]
        balls.append(len(balls_faced))


# In[32]:


balls


# In[33]:


dhoni_matches['runs'] = runs
dhoni_matches['balls'] = balls


# In[34]:


dhoni_matches


# In[35]:


dhoni_matches.to_csv(r'C:\Users\KUNAL\Desktop\Collearn\dhoni_matches.csv')


# In[36]:


#Score
# 10, 10-30, 30+
# percent dots
# strike rate
#is_chasing
#is_won
# dhoni_over

#graphs


# In[37]:


teams = ['Chennai Super Kings', 'Rising Pune Supergiants', 'Rising Pune Supergiant']


# In[38]:


dhoni_team_matches = []
for msd_id in msd_ids:
    df = ball_by_ball_comp.loc[ball_by_ball_comp['match_id'] == msd_id]
    df = df.loc[df['batting_team'].isin(teams)]
    dhoni_team_matches.append(df)


# In[39]:


dhoni_team_matches


# In[40]:


score = []

for dhoni_match in dhoni_team_matches:
    score.append(dhoni_match['total_runs'].sum())


# In[41]:


score


# In[42]:


dhoni_matches['Team_score'] = score


# In[43]:


dhoni_matches


# In[44]:


Contribution = []

Contribution = round(dhoni_matches['runs']*100/dhoni_matches['Team_score'],2)


# In[45]:


Contribution


# In[46]:


dhoni_matches['Contribution%'] = Contribution


# In[47]:


dhoni_matches


# In[48]:


ball_score = []
score = []
for match in match_details:
    df = match[(match['batsman']== "MS Dhoni") & (match['wide_runs'] == 0)]
    balls_faced = len(df)
    if(balls_faced <= 10):
        score.append(df['batsman_runs'].sum()) #1element
    if((balls_faced > 10) & (balls_faced < 31)):
        score.append(df['batsman_runs'].iloc[:10].sum())
        score.append(df['batsman_runs'].iloc[10:].sum()) #2elements
    if(balls_faced > 30):
        score.append(df['batsman_runs'].iloc[:10].sum())
        score.append(df['batsman_runs'].iloc[10:30].sum())
        score.append(df['batsman_runs'].iloc[30:].sum()) #3elements
        
    ball_score.append(score)
    score = []
    


# In[49]:


ball_score


# In[50]:


balls_df = pd.DataFrame(ball_score, columns = ['0-10', '10-30', '30+'])


# In[51]:


balls_df


# In[52]:


dhoni_matches = dhoni_matches.reset_index()


# In[53]:


dhoni_matches


# In[54]:


df1 = pd.concat([dhoni_matches,balls_df], axis = 1)


# In[55]:


df1


# In[56]:


sr = []
percent_dots = []
is_chasing = []
dhoni_over = []
for match in match_details:
    df = match[(match['batsman']== "MS Dhoni") & (match['wide_runs'] == 0)]
    sr.append(round((df['batsman_runs'].sum()*100)/len(df),2))
    percent_dots.append((len(df.loc[df['batsman_runs'] == 0])*100)/len(df))
    if(df.iloc[0]['inning'] == 1):
        is_chasing.append(0)
    else:
        is_chasing.append(1)
    dhoni_over.append(df.iloc[0]['over'])


# In[57]:


sr


# In[58]:


dhoni_over


# In[59]:


percent_dots


# In[60]:


df1['sr'] = sr
df1['percent_dots'] = percent_dots
df1['is_chasing'] = is_chasing
df1['dhoni_over'] = dhoni_over


# In[62]:


df1


# In[66]:


season_wise = df1.groupby(['season'])


# In[69]:


season_wise


# In[76]:


season_wise = season_wise.mean()


# In[74]:


season_wise.mean()['runs']


# In[77]:


import matplotlib.pyplot as plt


# In[81]:


plt.bar(season_wise.index, season_wise['runs'])


# In[95]:


df2 = df1[df1['is_chasing'] == 0]


# In[96]:


df2['runs'].mean()


# In[97]:


df2 = df1[df1['is_chasing'] == 1]


# In[98]:


df2['runs'].mean()

