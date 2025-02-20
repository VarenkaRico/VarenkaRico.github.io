#fun_clean_catalogs

#Import libraries
import pandas as pd

def fun_clean_categories(cat):

    """
    Cleans file by eliminating white space
    
    :param catalog

    :return tables without white space in columns
    """

    # Remove whitespace
    cat = cat.map(lambda x: ' '.join(x.split()) if isinstance(x, str) else x)

    return cat

def fun_split_category(cat):

    """
    Splits the column item_category_name from the cat_categories_item into group-category.
    Fills the category column with group in case no split indicator was found.
    Drops item_category_name column
    
    :param catalog

    :return cat with group, category columns and without item_category_name column.
    """

    # cat_categories_item separated into groups and categories. When no category is included (no word after -), group will be added as category too
    ## group - category

    try:
        cat[["group", "category"]] = cat.item_category_name.str.split(" - ", expand = True, n = 1)
    
    except Exception as e:
        except_message = f'Error while trying to split item_category_name column. {e}'
        print(except_message)

    
    cat["category"] = cat["category"].fillna(cat["group"])

    # Droping original column
    cat = cat.drop(columns = "item_category_name")

    return cat

def fun_extract_shop_name_info(str_shop_name, info_type):

    """
    Extract from the shop_name the city or the shop type
    
    :param str_shop_name string in which the function will search for a given text (lst_cities or shop_types)
    :param info_type ['City', 'ShopType'] is the information that will be search and extracted from info
    :required updated dict_shops_info with keys:
        City: lst_cities

    :return the city if included in the shop_name
    """

    #List of cities where there are stores
    lst_cities = ["!Якутск", "Адыгея", "Балашиха", 
          "Волжский", "Вологда", "Воронеж", 
          "Жуковский", 
          "Казань", "Калуга", "Коломна", "Красноярск", "Курск",
          "Москва", "Мытищи",
          "Н.Новгород", "Новосибирск",
          "Омск", 
          "РостовНаДону",
          "СПб", "Самара", "Сергиев Посад", "Сургут",
          "Томск", "Тюмень",
          "Уфа",
          "Химки",
          "Чехов",
          "Якутск", "Ярославль"
          ]
    
    lst_shop_types = ["ТЦ", "ТРК", "ТРЦ", "МТРЦ", "ТК", 
                   "Интернет-магазин ЧС", #Internet
                   "Цифровой склад", #Digital
                   "Выездная Торговля" #International
    ]
    
    dict_shops_info = {
    "City": lst_cities,
    "ShopType": lst_shop_types
    }
    
    try:
        for value in dict_shops_info[info_type]:
            if value in str_shop_name:
                return value
    
        return None
    
    except Exception as e:
        except_message = "info_type should be 'City' or 'ShopType'. Any other value will raise an error. {e}"
        print(except_message)
    
       ## Some shops have a type of shop as part of the shop_name (international commerce, internet and digital will by considered a type of shop)
    

    