import pandas as pd
import numpy as np
from env import get_connection
import os
import socket

#Removes warnings and imporves asthenics
import warnings
warnings.filterwarnings("ignore")


def dns_ptr_lookup(addr):
    """
    Small function to look up IP address if available.
    """
    try:
        return socket.gethostbyaddr(addr)
    except socket.herror:
        return None, None, None
    
def resolve_ip_addy(df):
    """
    Finds the resolved IP address if available.
    """
    
    ip_list = []
    
    #Iterates through IPs to get resolved address 
    for item in np.unique(df.ip):
        output = dns_ptr_lookup(str(item))
        ip_item = {'ip':item,
                   'ip_name':output[0]}
        ip_list.append(ip_item)
        
    #Creates DataFrame and merges with the origional
    ip_df = pd.DataFrame(ip_list)
    df = df.merge(ip_df, left_on = 'ip', right_on = 'ip')
    
    return df

def wrangle_logs():
    """
    This function gets all data from the connection_logs database.
    """
    filename = "curriculum_logs.csv"
    
    #Checks if file is catched
    if os.path.isfile(filename):
        
        df = pd.read_csv(filename, infer_datetime_format=True)

        #Changes to datetime type
        df['datetime'] = pd.to_datetime(df['datetime'], infer_datetime_format=True)
        df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
        #Sets index
        df = df.set_index('date')

        return df
    
    else:
        
        # read the SQL query into a dataframe
        query = """
        SELECT * FROM logs
        LEFT JOIN cohorts on logs.cohort_id = cohorts.id;
        """
        #Gets connection to Codeup database
        df = pd.read_sql(query, get_connection('curriculum_logs'))
        
        #Prepares data for exploration
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], utc=True)

        #Removes time offset
        df['datetime'] = df['datetime'].dt.tz_localize(None)

        #Changes date to datetime object
        df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
        
        #Finds addresses for IP if available
        df = resolve_ip_addy(df)
        df = df.drop(columns='id')
        #Caching
        df.to_csv(filename, index=False)
        #Sets index
        df = df.set_index('date')

        #Return the dataframe
        return df