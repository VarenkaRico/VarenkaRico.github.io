
'''Generates a file with clean, transformed and merged information to make easier the EDA analysis'''

#Import libraries

#Analysis
import pandas as pd
import numpy as np
#Time
import datetime as dt

import importlib
from pathlib import Path
import os

#Import customized functions
from functions_load_data import fun_open_cyrilic_files
from functions_clean_catalogs import fun_clean_categories
from functions_clean_catalogs import fun_split_category
from functions_clean_catalogs import fun_extract_shop_name_info
from functions_dates import fun_process_dates

#Set files information
script_dir = Path(__file__).parent.resolve() if '__file__' in globals() else Path().resolve()
os.chdir(script_dir)
str_directory = "../data/"

# Opening all files required to create the complete data sheet
logs_loading_data = []

try:
    tbl_sales_train = fun_open_cyrilic_files(str_directory, "sales_train.csv")
    ok_message = f'{dt.datetime.now()}:Ok loading train data:Ok'
    logs_loading_data.append(ok_message)
except Exception as e:
    except_message = f'{dt.datetime.now()}:Error loading train data: {e}'
    logs_loading_data.append(except_message)

try:
    cat_categories_item = fun_open_cyrilic_files(str_directory, "item_categories.csv")
    ok_message = f'{dt.datetime.now()}:Ok loading item_categories data:Ok'
    logs_loading_data.append(ok_message)
except Exception as e:
    except_message = f'{dt.datetime.now()}:Error loading categories dataset: {e}'
    logs_loading_data.append(except_message)

try:
    cat_items = fun_open_cyrilic_files(str_directory, "items.csv")
    ok_message = f'{dt.datetime.now()}:Ok loading items data:Ok'
    logs_loading_data.append(ok_message)
except Exception as e:
    except_message = f'{dt.datetime.now()}:Error loading items dataset: {e}'
    logs_loading_data.append(except_message)

try:
    cat_shops = fun_open_cyrilic_files(str_directory, "shops.csv")
    ok_message = f'{dt.datetime.now()}:Ok loading shops data:Ok'
    logs_loading_data.append(ok_message)
except Exception as e:
    except_message = f'{dt.datetime.now()}:Error loading shops dataset: {e}'
    logs_loading_data.append(except_message)

#Clean catalogs
try:
    cat_categories_item = fun_clean_categories(cat_categories_item)
    cat_shops = fun_clean_categories(cat_shops)
    cat_items = fun_clean_categories(cat_items)
    ok_message = f'{dt.datetime.now()}:Ok cleaning Catalogs:Ok'
    logs_loading_data.append(ok_message)
except Exception as e:
    except_message = f'{dt.datetime.now()}:Error cleaning Catalogs: {e}'
    logs_loading_data.append(except_message)

#Splitting information
try:
    cat_categories_item = fun_split_category(cat_categories_item)
    ok_message = f'{dt.datetime.now()}:Ok spliting cat_categories_item:Ok'
    logs_loading_data.append(ok_message)
except Exception as e:
    except_message = f'{dt.datetime.now()}:Error spliting cat_categories_item: {e}'
    logs_loading_data.append(except_message)

try:
    cat_shops["city"] = cat_shops.shop_name.apply(lambda x: fun_extract_shop_name_info(x, "City"))
    cat_shops["shop_type"] = cat_shops.shop_name.apply(lambda x: fun_extract_shop_name_info(x, "ShopType"))
    ok_message = f'{dt.datetime.now()}:Ok spliting cat_shops:Ok'
    logs_loading_data.append(ok_message)
except Exception as e:
    except_message = f'{dt.datetime.now()}:Error spliting cat_shops: {e}'
    logs_loading_data.append(except_message)


# Merge files and create the data sheet (tbl_sales_complete)
try:
    tbl_sales_complete = tbl_sales_train.merge(cat_shops, how = "left", on = "shop_id")
    tbl_sales_complete = tbl_sales_complete.merge(cat_items, how = "left", on = "item_id")
    tbl_sales_complete = tbl_sales_complete.merge(cat_categories_item, how = "left", on = "item_category_id")
    tbl_sales_complete = tbl_sales_complete.drop(columns = ["shop_id", "item_id", "item_category_id"])
    ok_message = f'{dt.datetime.now()}:Ok merging tables:Ok'
    logs_loading_data.append(ok_message)
except Exception as e:
    except_message = f'{dt.datetime.now()}:Error merging tables: {e}'
    logs_loading_data.append(except_message)

# Transform dates and add columns year, month and year_month
try:
    tbl_sales_complete = fun_process_dates(tbl_sales_complete, "date", '%d.%m.%Y')
    ok_message = f'{dt.datetime.now()}:Ok transforming dates:Ok'
    logs_loading_data.append(ok_message)
except Exception as e:
    except_message = f'{dt.datetime.now()}:Error transforming dates:{e}'
    logs_loading_data.append(except_message)

# ADDITIONAL TRANSFORMATIONS
# Define returns and sales

tbl_sales_complete["sales_type"] = np.where(tbl_sales_complete.item_cnt_day < 0, "Return", "Sale")

try:
    tbl_sales_complete.to_csv("../data/Outputs/sales_train_complete.csv")
    ok_message = f'{dt.datetime.now()}:Ok saving sales_train_complete.csv:Ok'
    logs_loading_data.append(ok_message)
except Exception as e:
    except_message = f'{dt.datetime.now()}:Error saving sales_train_complete.csv:{e}'
    logs_loading_data.append(except_message)

file_logs = open("../logs/logs.txt","a")
file_logs.write("-----New Execution----\n")
file_logs.write("ETL preprocess\n")
for log in logs_loading_data:
    file_logs.write(log+"\n")
file_logs.close()
