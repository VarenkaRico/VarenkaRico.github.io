#fun_cyrilic_imports

#Import libraries

#Analysis
import pandas as pd

def fun_open_cyrilic_files(path, file):

    """
    Open csv files and determines if the encoding required is utf-8 or windows-1251 for cyrilic alphabet
    
    :param path is the path from the working directory to the files directory
    :param file is the file's name (with .csv included) of the file required to open

    :return the file opened as a table in pandas
    """

    file_path = path + file
    try:
        tbl = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        tbl = pd.read_csv(file_path, encoding="windows-1251")
    
    return tbl