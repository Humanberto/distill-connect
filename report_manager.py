'''
STUDENT: Roberto Pocas Leitao
TEAM NAME: DistillConnect
DATE: June of 2024

'''

import pandas as pd
from datetime import datetime
import json
import sqlite3

DATABASE_URL = "reports.db"
REPORTS_FILE = 'reports.json'

def init_db():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reports (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        date TEXT,
                        details TEXT
                      )''')
    conn.commit()
    conn.close()

def save_reports():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    for report in reports:
        cursor.execute("INSERT INTO reports (id, title, date, details) VALUES (?, ?, ?, ?)", 
                       (report['id'], report['title'], report['date'], json.dumps(report['details'])))
    conn.commit()
    conn.close()

def load_reports():
    global reports
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports")
    rows = cursor.fetchall()
    conn.close()
    reports = [{'id': row[0], 'title': row[1], 'date': row[2], 'details': json.loads(row[3])} for row in rows]

def create_report(file):
    report_id = len(reports) + 1
    try:
        df = pd.read_csv(file, header=5, usecols=['CATEGORY NAME:', 'ITEM:', 'BOTT. TYPE/SIZE:', 'LOCATION:', 'COUNT:'])
        df = df[df['CATEGORY NAME:'].str.contains('Finished Product', na=False)]
        df['COUNT:'] = pd.to_numeric(df['COUNT:'], errors='coerce').fillna(0).astype(int)
        df['PAR'] = 0
        df['POs'] = 0
        df['Total'] = df['COUNT:'] - df['PAR'] - df['POs']
        details = df.values.tolist()
        details.insert(0, df.columns.tolist())
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

def get_report(report_id):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports WHERE id=?", (report_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {'id': row[0], 'title': row[1], 'date': row[2], 'details': json.loads(row[3])}
    return None

def delete_report(report_id):
    global reports
    reports = [r for r in reports if r['id'] != report_id]
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reports WHERE id=?", (report_id,))
    conn.commit()
    conn.close()

def filter_item(report_id, item_search):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports WHERE id = ?', (report_id,))
    row = cursor.fetchone()
    if row:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(json.loads(row[3]), columns=columns)
        df2 = df.set_index('ITEM:')
        df_filtered = df2[df2.index.str.lower().str.contains(item_search.lower())]
        conn.close()
        return df_filtered.reset_index().to_dict(orient='records')
    conn.close()
    return []

# Initialize the database and load reports
init_db()
load_reports()






'''
# =============================================================================
# Gave up on this
# 
# =============================================================================
'''
# =============================================================================
# 
# # import csv
# import pandas as pd
# from datetime import datetime
# import json
# from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_sqlalchemy import SQLAlchemy
# import report_manager
# from report_manager import save_reports, load_reports, create_report, get_report, delete_report
# 
# import sqlite3
# 
# 
# Base = declarative_base()
# DATABASE_URL = "sqlite:///reports.db"
# 
# 
# engine = create_engine('sqlite:///./reports.db')
# Session = sessionmaker(bind=engine)
# session = Session()
# 
# class Report(Base):
#     __tablename__ = 'reports'
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     date = Column(DateTime)
#     details = Column(String)  # Store details as JSON string
# 
# Base.metadata.create_all(engine)
# 
# '''
# This section will manage the list of reports created.
# '''
# 
# REPORTS_FILE ='reports.json'
# reports =[] #this will be the list of reports created
# 
# 
# def save_reports():
#     with open(REPORTS_FILE, 'w') as file:
#         json.dump(reports, file)
#         
#         
# def load_reports():
#     global reports
#     try:
#         with open(REPORTS_FILE, 'r') as file:
#             reports = json.load(file)
#     except FileNotFoundError:
#         reports = []
#         
# load_reports()
# 
# 
# def create_report(file):
#     report_id = len(reports) + 1
#     
#     try:
#                 
#         df = pd.read_csv(file, header=5, usecols=['CATEGORY NAME:', 'ITEM:', 'BOTT. TYPE/SIZE:', 'LOCATION:', 'COUNT:'])
#         # learned the above from another student
#         print(df)
#         
#         # df.drop(columns= not ['CATEGORY NAME:', 'ITEM:', 'BOTT. TYPE/SIZE:', 'LOCATION:', 'COUNT:'])
#         # print(df)
#         df = df[df['CATEGORY NAME:'].str.contains('Finished Product', na=False)] # trying to filter only Finished Products. Not working
#         
#         # Convert the COUNT: column to integer ---- FROM CHATGPT
#         df['COUNT:'] = pd.to_numeric(df['COUNT:'], errors='coerce').fillna(0).astype(int)
#         #---------------------------
#         
#         #------ decided to add the new columns PAR, POs, and Total from here, even if empty
#         df['PAR'] = 0
#         df['POs'] = 0
#         df['Total'] = df['COUNT:'] - df['PAR'] - df['POs'] #want to eventually only display the negative numbers
#         
#         
#        # df = df[df['Total'] <0] # Need a way to have user input for PAR and POs first
#         
#         
#         
#         #---- Trying a list of lists instead of itertuples()-------
#         
#         details = df.values.tolist()
#         
#         details.insert(0, df.columns.tolist())
# 
#         # for row in df.itertuples():
#                 
#         #     my_col = [index for index in row if 'Finished Product' or 'Supplies' or 'Raw Materials' in row[0]]
#             
#         #     if (my_col[1] == 'Finished Product'): #or (my_col[1] == 'Supplies') or (my_col[1] == 'Raw Materials'):
#         #         # print(my_col)
#         #         print(f'Type: {my_col[1]} \t\t Product: {my_col[2]} \t\t\t\t Size: {my_col[3]} \t\t\t\t Location: {my_col[4]} \t\t\t\t Count: {my_col[5]}')
#                 
#                        
#         
#         #------- Was trying to us cvs instead, too confusing------
#         
#         # csv_reader = csv.reader(file_content.splitlines())
#         # for row in csv_reader:
#         #     details.append(row)
#         # ---------------------------------------
#             
#     except Exception as e:
#         print(f"Error reading csv file: {e}")
#         return None
#     
#     report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     report = {
#         'id': report_id,
#         'title': file.filename,
#         'date': report_date,
#         'details': details        
#         }
#     
#     reports.append(report)
#     save_reports()
#     return report, report_id
# 
#     
# def filter_item(report_id, item_search):
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM report_details WHERE report_id = ?', (report_id,))
#     rows = cursor.fetchall()
#     columns = [desc[0] for desc in cursor.description]
#     df = pd.DataFrame(rows, columns=columns)
#     df2 = df.set_index('ITEM:')
#     df_filtered = df2[df2.index.str.lower().str.contains(item_search.lower())]
#     conn.close()
#     return df_filtered.reset_index().to_dict(orient='records')
# 
#         
# # =============================================================================
# # def filter_item(report):
# 
# #       df = report
# #     # df2 = df.set_index('ITEM:')
# #     # df2.sort_values(by='ITEM:', ascending=True)
# #     # item_search = input('Enter item: ').lower()
# #     # df_filtered = df2[df2.index.str.lower().str.contains(item_search)]
# #     # return df_filtered
# # 
# # =============================================================================
# 
# 
# '''
# locate report by id 
# '''       
# 
# 
# def get_report(report_id):
#     return next((r for r in reports if r['id'] == report_id), None) # Learned this with the Mimo app. YAY!
# 
# 
# '''
# function to delete a report using report_id to locate it
# '''
# 
# def delete_report(report_id):
#     global reports
#     reports = [r for r in reports if r['id'] != report_id]
#     save_reports()
#     
# # def main():
# #     create_report(file)
# #     get_report(report_id)
# #     delete_report(report_id)
#     
# # if __name__ == '__main__':
# #     main()
# 
# 
# =============================================================================
