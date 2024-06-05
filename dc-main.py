# -*- coding: utf-8 -*-

'''
# =============================================================================
# STUDENT: Roberto Pocas Leitao
# TEAM NAME: DistillConnect
# DATE: June of 2024
# =============================================================================

'''

import pandas as pd
import random

# Display headers
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#--------

file_path = r"C:\Users\rober\Dropbox\.WORK\distillery\Reports\INVENTORY-2024-05-08.csv"

def create_dataframe(file_path):
  
    df = pd.read_csv(file_path, header=5, usecols=['CATEGORY NAME:', 'ITEM:', 'BOTT. TYPE/SIZE:', 'LOCATION:', 'COUNT:'])
    
    # COUNT: to int for calculating Total
    df['COUNT:'] = pd.to_numeric(df['COUNT:'], errors='coerce').fillna(0).astype(int)

    df = df[df['CATEGORY NAME:'] == 'Finished Product']
    
     
    # Unrealistic, but generating random PAR and POs amounts. Couldn't figure out how to make it user input with so many items.
    df['PAR'] = [random.randint(0, 300) for num in range(len(df))]
    df['POs'] = [random.randint(0, 100) for num in range(len(df))] 
    df['Total'] = df['COUNT:'] - df['PAR'] - df['POs']
    df.insert(0, 'Item #', range(1, len(df) + 1))
    df = df.sort_values(by=['Total'], ascending=True) # sorting Totals to show lowest inventory
    
    # Best way I found to print all columns on the same line
    print(df.to_string(index=False, header=True)) 
    return df


# =============================================================================
# def filter_by_item(df):
#     '''
#     This function is set for the user to filter by brand under the "ITEM:" column.
#     Can be partial terms too.
#     '''
#     
#     while True:
#         print()
#         item = input("Enter item to filter by: ")
#         filtered_df = df[df['ITEM:'].str.contains(item, case=False, na=False)]
#         filtered_df = filtered_df.sort_values(by=['Total'], ascending=True) # sorting Totals to show lowest inventory
#         print(filtered_df.to_string(index=False, header=True))
#     return filtered_df
# 
# 
# def main(): 
#     df = create_dataframe(file_path)    
#     create_dataframe(file_path)
#     filter_by_item(df)
# 
# =============================================================================

def filter_by_item(df):
    '''
    This function is set for the user to filter by brand under the "ITEM:" column.
    Can be partial terms too.
    '''
    
    
    while True:
        print()
        print("Options:")
        print("1. Enter item to filter by")
        print("2. Show all items")
        print("3. Exit")
        
        option = input("Choose an option (1/2/3): ").strip()
        
        if option == '3':
            break
        elif option == '2':
            print(df.to_string(index=False, header=True))
        elif option == '1':
            item = input("Enter item to filter by: ")
            filtered_df = df[df['ITEM:'].str.contains(item, case=False, na=False)]
            filtered_df = filtered_df.sort_values(by=['Total'], ascending=True)  # sorting Totals to show lowest inventory
            print(filtered_df.to_string(index=False, header=True))
        else:
            print("Invalid option. Please try again.")
    return df
    
    
    
# =============================================================================
#   1
# 
# =============================================================================
def main(): 
    df = create_dataframe(file_path)    
    while True:
        filter_by_item(df)
        another_filter = input("Do you want to filter by another item? (yes/no): ").strip().lower()
        if another_filter != 'yes':
            break




if __name__ == '__main__':
    main()