

import pandas as pd
from mftool import Mftool
from datetime import datetime, timedelta 
import sqlite3
mf = Mftool()


scheme_codes = mf.get_scheme_codes()
scheme_codes


scheme_code_list = [x for x in scheme_codes.keys()]
scheme_code_list

def HistoricalNav(scheme_code_list, start_date, end_date):
  
  assert (isinstance(scheme_code_list, list) is True)
  assert (isinstance(start_date, str) is True)
  assert (isinstance(end_date, str) is True)
  main_df = pd.DataFrame() 

  for schemes in scheme_code_list:
    data = mf.get_scheme_historical_nav_for_dates(schemes, start_date, end_date) 

    df = pd.DataFrame(data['data']) 
    df['scheme_code'] = pd.Series([data['scheme_code'] for x in range(len(df.index))]) 
    df['scheme_name'] = pd.Series([data['scheme_name'] for x in range(len(df.index))]) 

    df = df.sort_values(by = 'date') 

    main_df = main_df.append(df) 

  main_df = main_df[['scheme_code', 'scheme_name', 'date', 'nav']]  
  main_df.reset_index(drop = True, inplace = True) 

  return main_df 


def NAV_Data(start,end): 
  try:
    values_df = HistoricalNav(scheme_code_list = scheme_code_list[0:5], start_date= start, end_date= end) 
    return values_df
  except KeyError:
    
    start=datetime.strptime(start, '%d-%m-%Y') - timedelta(1) 
    return NAV_Data(start.strftime("%d-%m-%Y"),end)

start_date= "07-05-2021" 
end_date = "15-05-2021" 
values_df = NAV_Data(start_date,end_date) 
values_df


values_df[values_df['scheme_code'] == 119552]

values_df 
print(values_df)

conn = sqlite3.connect('TestDB1.db')
c = conn.cursor()
c.execute('''  
DROP TABLE scrap1
          ''')
c.execute('CREATE TABLE scrap1 (scheme_code, scheme_name,date,nav)')
conn.commit()
scrap1 = values_df
        

df = pd.DataFrame(scrap1, columns= ['scheme_code', 'scheme_name', 'date', 'nav'])
df.to_sql('scrap1', conn, if_exists='replace', index = False)
 
c.execute('''  
SELECT * FROM scrap1
          ''')

for row in c.fetchall():
    print (row)

df.to_csv('file1.csv')
