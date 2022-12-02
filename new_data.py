import requests 
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


"""
Note on data 

Data is from eurostat - statsitics from the european commission 
their notice here: https://ec.europa.eu/info/legal-notice_en#copyright-notice 
under licence https://creativecommons.org/licenses/by/4.0/  
"""

# API notes 
"""
EUROSTAT REST API docs are short, to understand parameters make a basic call 
to a dataset and use a JSON viewer on the response to understand params. 
e.g.
# https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_cann/default/table?lang=en
# https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/PRC_HICP_CANN?format=JSON&lang=EN
# https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/PRC_HICP_MANR?format=JSON&lang=EN
"""
 
# API parameters   
level2 =  ['C21','C22','C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29','C30', 'C31', 'C32','C33', 'D35', 'E36']
base_url = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/'
data_set = 'STS_INPP_M?format=JSON&lang=EN&geo=EU27_2020&unit=PCH_SM'
pp_url = base_url + data_set  

cpi_const_tax = 'PRC_HICP_CANN?format=JSON&lang=EN&geo=EU27_2020&coicop=CP00'
cpi_vtax = 'PRC_HICP_MANR?format=JSON&lang=EN&geo=EU27_2020&coicop=CP00'
hppi = 'STS_INPPD_M?format=JSON&lang=EN&geo=EU27_2020&unit=PCH_SM'

def pull_PPI_data(since_date,code): 
    """
    For a given PPI code pull the data for the given date range and producer code. 
    """
    url =  pp_url  + f'&nace_r2={code}&sinceTimePeriod={since_date}' 
    data = requests.get(url).json()

    # Get the size of the data points
    shape_months = data['size'][6]-1   

    # Extract two naming columns - one for NACE_R2 code and one for readable name 
    code = list(data['dimension']['nace_r2']['category']['label'].keys())[0]
    name = list(data['dimension']['nace_r2']['category']['label'].values())[0]
    if len(name) > 44:
        name = name[:43].rsplit(' ',1)[0]
    
    # Get time lables, removing this month as no data for this value
    time_labels = list(data['dimension']['time']['category']['label'].values())
    time_labels.pop(-1) #Remove empty latest 

    # Extract data in order
    dictlist = sorted([int(x) for x in list(data['value'].keys())])
    values = [data['value'][str(x)] for x in dictlist]

    code_ls = [str(code) for x in values]
    name_ls = [str(name) for x in values]

    todf = list(zip(code_ls,name_ls,time_labels,values))
    df = pd.DataFrame(data=todf,columns=['code','name','time','index'])

    return df
    


def pull_headline_data(since_date): 
    """
    For a given 
    """
    url_1 = base_url + cpi_const_tax  + f'&sinceTimePeriod={since_date}'
    url_2 = base_url + cpi_vtax  + f'&sinceTimePeriod={since_date}'
    url_3 = base_url + hppi + f'&sinceTimePeriod={since_date}'
    cpi_codes = ['cpi_ctax','hcpi','ppi']
    i = 0
    out_ls = []

    for url in [url_1, url_2,url_3]:
        data = requests.get(url).json()
        dictlist = sorted([int(x) for x in list(data['value'].keys())])
        values = [data['value'][str(x)] for x in dictlist]

        # Get time lables, removing this month as no data for this value
        time_labels = list(data['dimension']['time']['category']['label'].values())
        time_labels.pop(-1) #Remove empty latest   

        code_ls = [str(cpi_codes[i]) for x in values]
        i += 1

        todf = list(zip(code_ls,time_labels,values))
        df = pd.DataFrame(data=todf,columns=['code','time','index'])
        out_ls.append(df)
    
    #cpi_df = out_ls[0].append(out_ls[1]).append(out_ls[2])
    cpi_df = pd.concat([out_ls[0],out_ls[1],out_ls[2]])
    cpi_df.to_csv('data/CPI_EU27_5ys.csv',index=False) 

def get_dfs(): 
    """
    Function to coordinate API requests 
    Calls 'pull_PPI_data' and 'pull_headline_data' with correct inputs 
    """
    fiveyears_ago = str(datetime.date(datetime.now()) - timedelta(days=365*5))[:-3]
    pp_df = pull_PPI_data(fiveyears_ago,level2[0])

    for code in level2[1:]: 

        newdf = pull_PPI_data(fiveyears_ago,code)
        #pp_df = pp_df.append(newdf)
        pp_df = pd.concat([pp_df,newdf])

    #pp_df = pp_df.rename_axis(index='Class', columns="Date")
    pp_df = pp_df.sort_values(by=['time'])
    pp_df.to_csv('data/PPIC_EU27_5ys.csv',index=False) 
    pp_df.to_csv

    pull_headline_data(fiveyears_ago)
