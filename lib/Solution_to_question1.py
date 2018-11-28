
# coding: utf-8

# # Solution to Question 1

# ## Python imports
#
# Before executing code cells we load some required packages and initiate database connection.

# In[1]:


import os # directory pathfinding
if 'notebooks' in os.getcwd(): # make sure jupyter server is in project root
    get_ipython().run_line_magic('cd', '..')


# In[2]:


import altair as alt # visualization library
import numpy as np  # linear algebra
import pandas as pd  # data processing
from IPython.display import display # show interactive sliders
from ipywidgets import interact # common interactivity features
import ipywidgets as widgets # package for interactivity

# import matplotlib.pyplot as plt
# import seaborn as sns
# color = sns.color_palette()

# alt.data_transformers.enable('json') # if number of records > 5000
alt.renderers.enable('notebook') # Renderer for notebook (comment out if using jupyterlab)

import lib # project code package


# In[3]:


# create a database connection
database = os.path.realpath('../rannala_project/db/rannala_project.db')
conn = lib.create_connection(database)


# ## Data Journey
#
# Now we are ready to start exploring the dataset.

# ### First 5 rows of cleaned dataset

# In[4]:


# read in dataset
df = pd.read_sql_query(
    '''SELECT substr(Time,7)||'-'||substr(Time,4,2)||'-'||substr(Time,1,2) as Time,
    cast(replace(Impressions,",","") as INT) as Impressions,cast(replace(Clicks,",","") as INT) as Clicks,
    cast(replace(CTR,"%","") as FLOAT) / 100 as CTR,
    cast(replace([Cohort size],",","") as INT) as [Cohort Size],
    cast(replace([Click to Install],"%","") as FLOAT) as [Click to Install],
    cast(replace(fCVR,"%","") as FLOAT) / 100 as fCVR,
    cast([D7 Payers] as INT) as [D7 Payers],
    cast(replace([D7 Payer Conversion],"%","") as FLOAT) / 100 as [D7 Payer Conversion]
    FROM question1;''', conn)
df.head()


# ### Data types in dataframe

# In[5]:


df.info()


# ## Field descriptions
#
# - **Time**: Date of action (impression, click or install)
# - **Impressions**: Number of ad impressions on the given date
# - **Clicks**: Number of clicks on the game ad on the given date
# - **CTR**: Click through rate
# - **Cohort size**: Number of game installs on the given date, which came through ads
# - **Click to Install**: Click to Install rate on the given date
# - **fCVR**: Funnel conversion rate for the given date, i.e how much of ad impressions turned into a new game install
# - **D7 Payers**: Number of players who did an in-app purchase in the game within 7 days after the given install date
# - **D7 Payer Conversion**: Share of players who did an in-app purchase within 7 days after installing the game on the given date

# ### Some basic statistical figures

# In[6]:


df.describe()


# ### First impression from data
#
# The pathway from ad views ('impressions') via click'n'installs to players who actually do in-app purchases is very narrow. A million impressions might yield 85 paying customers for example.

# In[7]:


alt.Chart(df).mark_circle().encode(
    alt.Y('Impressions:Q'),
    alt.X('D7 Payers:Q',scale=alt.Scale(zero=False)),
    color=alt.Color('sum(D7 Payer Conversion):Q', legend=None),
    size= 'D7 Payers:Q'
).properties(
    title='Impressions vs D7 Payers (color density = D7 Payer Conversion rate from installs)',
)


# ### Funnel Part I: Impressions vs Clicks
#
# To travel the rocky path from impressions to paying customers, lets first look at the first step along the way. 8th and 9th of September jump out from data. Both had good conversion rates - even though the number of impressions were not particularly great.

# In[8]:


pts = alt.selection(type='interval', encodings=['x'])

base = alt.Chart(df).encode(
    alt.X('Time:N')
)

bar = base.mark_bar().encode(
    y='Impressions:Q',
    color=alt.Color('CTR:Q', legend=None)
).transform_filter(
    pts
).properties(
    selection=pts,
    width=450,
    height=300,
    title='Impressions vs Clicks (color density = CTR conversion rate)'
)

line = base.mark_line(color='red').encode(
    y='Clicks:Q',
)

layer1 = alt.layer(
    bar,
    line
).resolve_scale(
    y='independent', color='independent'
)

layer1


# ### Funnel Part II: Clicks vs Installs
#
# Here we notice that the start of month was great for landing actual installs from ad clicks. First weekend of September looks like a very good time to be out hunting for new players.

# In[9]:


pts = alt.selection(type='interval', encodings=['x'])

base = alt.Chart(df).encode(
    alt.X('Time:N')
)

bar = base.mark_bar().encode(
    y='Clicks:Q',
    color=alt.Color('Click to Install:Q', legend=None)
).transform_filter(
    pts
).properties(
    selection=pts,
    width=450,
    height=300,
    title='Clicks vs Installs aka "Cohort Size" (color density = "Click to Install" conversion rate)'
)

line = base.mark_line(color='red').encode(
    y='Cohort Size:Q',
)

layer1 = alt.layer(
    bar,
    line
).resolve_scale(
    y='independent', color='independent'
)

layer1


# ### Funnel Parts I & II together form a key KPI
#
# - **fCVR** aka share of ad impressions turned into new game installs.

# In[10]:


pts = alt.selection(type='interval', encodings=['x'])

base = alt.Chart(df).encode(
    alt.X('Time:N')
)

bar = base.mark_bar().encode(
    alt.Y('Impressions:Q'),
    color=alt.Color('Cohort Size:Q', legend=None)
).transform_filter(
    pts
).properties(
    selection=pts,
    width=450,
    height=300,
    title='fCVR (color density = Installs aka "Cohort Size")'
)

line = base.mark_line(color='red').encode(
    alt.Y('fCVR:Q',axis=alt.Axis(format='%')),
)

layer1 = alt.layer(
    bar,
    line
).resolve_scale(
    y='independent', color='independent'
)





layer1


# ### Funnel Part III: Installs vs D7 Payers
#
# The share of ad-sourced player cohort that makes in-app purchases within 7 days of game install.

# In[11]:


pts = alt.selection(type='interval', encodings=['x'])

base = alt.Chart(df).encode(
    alt.X('Time:N')
)

bar = base.mark_bar().encode(
    y='Cohort Size:Q',
    color=alt.Color('D7 Payer Conversion:Q')
).transform_filter(
    pts
).properties(
    selection=pts,
    width=450,
    height=300,
    title='Installs aka "Cohort Size" vs D7 Payers (color density = "D7 Payer Conversion" rate)'
)

line = base.mark_line(color='red').encode(
    y='D7 Payers:Q',
)

layer1 = alt.layer(
    bar,
    line
).resolve_scale(
    y='independent', color='independent'
)

layer1


# ### KPI Comparison: CTR vs fCVR vs D7 Payer Conversion Rate aka "D7CVR"
#
# Lets see how the three KPIs match up against each other.

# In[12]:



brush = alt.selection(type='interval', encodings=['x'])

# Define the base chart, with the common parts of the
# background and highlights
base = alt.Chart(df).mark_line().encode(
    y=alt.X(alt.repeat('column'), type='quantitative',axis=alt.Axis(format='%')),
    x='Time:O'
).properties(
    width=250,
    height=200
)

# blue background with selection
background = base.properties(
    selection=brush
)

# yellow highlights on the transformed data
highlight = base.encode(
    color=alt.value('bluegreen')
).transform_filter(
    brush
)

# layer the two charts & repeat
alt.layer(
    background, highlight,
    data=df
).repeat(
    column=["CTR", "fCVR", "D7 Payer Conversion"]
)


# In[13]:


layer1 = alt.Chart(df).mark_circle().encode(
    alt.X('fCVR:Q', bin=True,axis=alt.Axis(format='%')),
    alt.Y('Impressions:Q', bin=True),
    alt.Color('Time:O', legend=None),
    size='D7 Payers'
).properties(
    selection=pts,
    width=450,
    height=250,
    title='Binned Impressions vs fCVR (color density = Progress of Month)'
)

layer2 = alt.Chart(df).mark_circle().encode(
    alt.X('D7 Payer Conversion:Q', bin=True, axis=alt.Axis(format='%')),
    alt.Y('Impressions:Q', bin=True),
    alt.Color('Time:O', legend=None),
    size='D7 Payers'
).properties(
    selection=pts,
    width=450,
    height=250,
    title='Binned Impressions vs D7CVR (color density = Progress of Month)'
)



layer1 & layer2


# ### Altair Selections Demo
#
# Paint days of month in 1st chart to see filter effect in 2nd chart!

# In[14]:


pts = alt.selection(type='interval', encodings=['x'])

base = alt.Chart(df).encode(
    alt.X('Time:O')
)

bar = base.mark_bar().encode(
    y='D7 Payers:Q',
    color=alt.Color('sum(D7 Payer Conversion):Q', legend=None)
).transform_filter(
    pts
).properties(
    selection=pts,
    width=450,
    height=300,
    title='D7 Payers (color density = D7CVR)'
)

line = base.mark_line(color='red').encode(
    alt.Y('D7 Payer Conversion:Q',axis=alt.Axis(format='%'))
)

layer1 = alt.layer(
    bar,
    line
).resolve_scale(
    y='independent', color='independent'
)


layer0 = alt.Chart(df).mark_circle().encode(
    alt.X('fCVR:Q', bin=True, axis=alt.Axis(format='%')),
    alt.Y('Impressions:Q', bin=True),
    color='Time:O',
    size='D7 Payers'
).transform_filter(
    pts
).properties(
    selection=pts,
    width=450,
    height=250,
    title='Binned Impressions vs Binned fCVR (color density = Progress of Month)'
)

layer1 & layer0

