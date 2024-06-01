'''
STUDENT: Roberto Pocas Leitao
TEAM NAME: DistillConnect
DATE: June of 2024

'''

import csv
import pandas as pd
from datetime import datetime
import json

'''
This section will manage the list of reports created.
'''

REPORTS_FILE ='reports.json'
reports =[] #this will be the list of reports created


def save_reports():
    with open(REPORTS_FILE, 'w') as file:
        json.dump(reports, file)
        
        
def load_reports():
    global reports
    try:
        with open(REPORTS_FILE, 'r') as file:
            reports = json.load(file)
    except FileNotFoundError:
        reports = []
        
load_reports()


def create_report(file):
    report_id = len(reports) + 1
    
    try:
        df = pd.read_csv(file, header=5, usecols=['CATEGORY NAME:', 'ITEM:', 'BOTT. TYPE/SIZE:', 'LOCATION:', 'COUNT:'])
        # learned the above from another student
        
        
        df = df[df['CATEGORY NAME:'].str.contains('Finished Product', na=False)] # trying to filter only Finished Products. Not working
        
        # Convert the COUNT: column to integer ---- FROM CHATGPT
        df['COUNT:'] = pd.to_numeric(df['COUNT:'], errors='coerce').fillna(0).astype(int)
        #---------------------------
        
        #------ decided to add the new columns PAR, POs, and Total from here, even if empty
        df['PAR'] = 0
        df['POs'] = 0
        df['Total'] = df['COUNT:'] - df['PAR'] - df['POs'] #want to eventually only display the negative numbers
        
        
       # df = df[df['Total'] <0] # Need a way to have user input for PAR and POs first
        
        
        
        #---- Trying a list of lists instead of itertuples()-------
        
        details = df.values.tolist()
        
        details.insert(0, df.columns.tolist())

        
        # for row in df.itertuples():
                
        #     my_col = [index for index in row if 'Finished Product' or 'Supplies' or 'Raw Materials' in row[0]]
            
        #     if (my_col[1] == 'Finished Product'): #or (my_col[1] == 'Supplies') or (my_col[1] == 'Raw Materials'):
        #         # print(my_col)
        #         print(f'Type: {my_col[1]} \t\t Product: {my_col[2]} \t\t\t\t Size: {my_col[3]} \t\t\t\t Location: {my_col[4]} \t\t\t\t Count: {my_col[5]}')
                
                       
        
        #------- Was trying to us cvs instead, too confusing------
        
        # csv_reader = csv.reader(file_content.splitlines())
        # for row in csv_reader:
        #     details.append(row)
        # ---------------------------------------
            
    except Exception as e:
        print(f"Error reading csv file: {e}")
        return None
    report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = {
        'id': report_id,
        'title': file.filename,
        'date': report_date,
        'details': details        
        }
    
    reports.append(report)
    save_reports()
    return report, report_id

'''
locate report by id 
'''       

def get_report(report_id):
    return next((r for r in reports if r['id'] == report_id), None) # Learned this with the Mimo app. YAY!


'''
function to delete a report using report_id to locate it
'''

def delete_report(report_id):
    global reports
    reports = [r for r in reports if r['id'] != report_id]
    save_reports()
    
# def main():
#     create_report(file)
#     get_report(report_id)
#     delete_report(report_id)
    
# if __name__ == '__main__':
#     main()