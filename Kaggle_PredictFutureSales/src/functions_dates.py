import pandas as pd
#Time
import datetime as dt

def fun_process_dates(tbl, column, format):
    """
    Transforms dates and returns additional columns(month, year, year_month)
    
    :param tbl table in which the date column to be transformed is
    :param column name of the date column in tbl
    :param format is the actual format in which the date is given. For Kaggle Sales Prediction is expected '%d.%m.%Y'
    :required updated dict_shops_info with keys:

    :return tbl with column formated and additional columns added
    """
    try:
         # Update date column type
        tbl[column] = pd.to_datetime(tbl[column], format = format)
        #Adding Month column
        tbl["month"] = tbl[column].dt.month

        #Adding Year column
        tbl["year"] = tbl[column].dt.year

        #First day of the month
        tbl["year_month"] = tbl[column].dt.strftime('%Y.%m.01')


    except Exception as e:
        except_message = f'Error while processing date. Probably format given is incorrect. {e}'
        print(except_message)

    
    return tbl