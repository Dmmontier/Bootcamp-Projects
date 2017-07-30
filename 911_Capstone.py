import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().magic('matplotlib inline')

#Load call data into dataframe
df = pd.read_csv('911.csv')
#Check info
df.info()
#Look at first few elements
df.head(3)


#Check most frequent zip codes and townships
df['zip'].value_counts().head(5)
df['twp'].value_counts().head(5)

#check number of unique call reasons
df['title'].nunique()

#Make a new column for "reason", which is the string of chars preceding ":" in the title column ("EMS", "Traffic", "Fire")
df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])
df['Reason'].value_counts()

#Count number of reasons
sns.countplot(x='Reason',data=df,palette='viridis')

#Get data type of timestamp column (using first element)
type(df['timeStamp'].iloc[0])

#Convert timestamp column to a datetime object instead of string
df['timeStamp'] = pd.to_datetime(df['timeStamp'])

#Create new columns for separate sections of timestamp
df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['Month'] = df['timeStamp'].apply(lambda time: time.month)
df['Day of Week'] = df['timeStamp'].apply(lambda time: time.dayofweek)

#Maps "Day of Week" int values to matching day of week names
dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

#Reassign day of week to string names instead of ints
df['Day of Week'] = df['Day of Week'].map(dmap)

#Make a countplot by day of week, with separate bars for each reason
sns.countplot(x='Day of Week',data=df,hue='Reason',palette='viridis')

# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

#Do same for month
sns.countplot(x='Month',data=df,hue='Reason',palette='viridis')

# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

#Make a dataframe grouping by month as index
byMonth = df.groupby('Month').count()
byMonth.head()

byMonth['twp'].plot()

#Regression plot by month
sns.lmplot(x='Month',y='twp',data=byMonth.reset_index())


df['Date']=df['timeStamp'].apply(lambda t: t.date())



df.groupby('Date').count()['twp'].plot()
plt.tight_layout()

#Plots data by call reason over time
df[df['Reason']=='Traffic'].groupby('Date').count()['twp'].plot()
plt.title('Traffic')
plt.tight_layout()

df[df['Reason']=='Fire'].groupby('Date').count()['twp'].plot()
plt.title('Fire')
plt.tight_layout()

df[df['Reason']=='EMS'].groupby('Date').count()['twp'].plot()
plt.title('EMS')
plt.tight_layout()



dayHour = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
dayHour.head()

plt.figure(figsize=(12,6))
sns.heatmap(dayHour,cmap='viridis')
sns.clustermap(dayHour,cmap='viridis')



dayMonth = df.groupby(by=['Day of Week','Month']).count()['Reason'].unstack()
dayMonth.head()


plt.figure(figsize=(12,6))
sns.heatmap(dayMonth,cmap='viridis')


sns.clustermap(dayMonth,cmap='viridis')

