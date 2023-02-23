import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler
import socket
import env
import wrangle


def top_lesson(dfa):
    '''
    This function generates top-accessed lesson from inputed dataframe
    and outputs name
    '''
    lessons = []
    dfa = pd.DataFrame(dfa['path'].value_counts())
    dfa.reset_index(inplace = True)
    dfa.rename(columns = {'index':'top_lesson'}, inplace = True)
    for x in dfa['top_lesson']:
            if x == '/':
                continue
            elif 'search' in x:
                continue
            elif 'index'  in x:
                continue
            else:
                lessons.append(x)
    lessons = pd.DataFrame(lessons)
    lessons.rename(columns = {0:'top lesson'}, inplace = True)
    return lessons.head(1)

def prog_split(dfa):
    '''
    This function splits the DataFrame up by program and outputs
    them as separate DataFrames
    '''
    df_p01 = dfa[dfa['program_id'] == 1]
    df_p02 = dfa[dfa['program_id'] == 2]
    df_p03 = dfa[dfa['program_id'] == 3]
    return df_p01, df_p02, df_p03

def low_access_users(df):
    """
    This function shows the number of users in web dev (program_id = 2) and data science (program_id = 3) who are in the bottom 25%.
    """
    
    students = df[df.name != 'Staff']
    students['start_date'] = pd.to_datetime(students['start_date'], infer_datetime_format=True)
    students['end_date'] = pd.to_datetime(students['end_date'], infer_datetime_format=True)
    active_students = students[(students.index <= students.end_date) & (students.index >= students.start_date)]
    lower_quarter = active_students.user_id.value_counts().index[-183:]
    lower_quarter_students = active_students[active_students['user_id'].isin(lower_quarter)]
    print("Web Dev program_id = 2")
    print("Data Science program_id = 3")
    print(lower_quarter_students.groupby('program_id').count()['path'])
    
def view_web_scraping(df):
    '''
    this function shows a sample of users suspected of webscraping
    '''
    
    null_users = [48, 354, 111, 355, 372]

    for item in null_users:
        plt.plot(df[df.user_id == item].resample('T').count()['path'])
        plt.xticks(rotation = 45)
        plt.title(f'Unathorized user: {item}')
        plt.ylabel("Requests per minute")
        plt.show()
        
def q5(df):
    '''
    Subsets dataframe for only observations in 2019. 
    Removes Staff from observations.
    Resamples data at a weekly rate.
    Plots count of access requests for each program(DS and WD).
    
    Question 5: At some point in 2019, the ability for students and alumni to access 
    both curriculums (web dev to ds, ds to web dev) should have been shut off. 
    Do you see any evidence of that happening? Did it happen before?

    '''
    
    # Year Column
    df['year'] = df.datetime.dt.year
    
    # Set Index
    df = df.set_index(df.datetime)
    
    # All observations in 2019
    twenty_nineteen = df[df['year'] == 2019]
    
    # Data Science and Web Dev data frames
    web_dev = twenty_nineteen[(twenty_nineteen['program_id'] == 1) | (twenty_nineteen['program_id'] == 2)]
    ds = twenty_nineteen[twenty_nineteen['program_id'] == 3]
    
    # Removing Staff 
    ds = ds[ds['name'] != 'Staff']
    web_dev = web_dev[web_dev['name'] != 'Staff']
    
    # DS students accessing Java stuff sampled at a weekly time frame
    ds_to_wd = ds[ds['path'].str.contains('java')].resample('w').count()
    
    # WD students accessing data-scientist stuff at a weekly time frame
    wd_to_ds = web_dev[web_dev['path'].str.contains('data-scientist')].resample('w').count()
    
    # Lineplot for Data Science to Web Dev
    sns.lineplot(x=ds_to_wd.index, y='path',data=ds_to_wd, label='Path')
    plt.title('DS Accessing WD Material 2019')
    plt.xticks(rotation=35)
    plt.ylabel('Number of Requests')
    plt.xlabel('Date')
    plt.legend()
    plt.show()
    
    # Lineplot for Web Dev to Data Science
    sns.lineplot(x=wd_to_ds.index, y='path',data=wd_to_ds, label='Path')
    plt.title('WD Accessing DS Material 2019')
    plt.xticks(rotation=35)
    plt.ylabel('Number of Requests')
    plt.xlabel('Date')
    plt.legend()
    plt.show()
