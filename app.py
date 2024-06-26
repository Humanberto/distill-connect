
from flask import Flask, render_template, request, redirect, url_for, jsonify
import report_manager
from report_manager import save_reports, create_report, get_report, delete_report, filter_item, load_reports

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reports')
def view_reports():
    return render_template('view_reports.html', reports=report_manager.reports)

# =============================================================================
# @app.route('/report/<string:report_id>', methods=['GET', 'POST'])
# def report_detail(report_id):
#     report = get_report(report_id)
#     if request.method == 'POST':
#         if 'sort' in request.form:
#             sort_by = request.form['sort']
#             sort_index = report['details'][0].index(sort_by)
#             report['details'] = [report['details'][0]] + sorted(report['details'][1:], key=lambda x: x[sort_index])
#         elif 'filter' in request.form:
#             filter_term = request.form['filter']
#             report['details'] = [report['details'][0]] + [row for row in report['details'][1:] if filter_term.lower() in str(row).lower()]
#         else:
#             for i, row in enumerate(report['details'][1:], start=1):
#                 par = request.form.get(f'par-{i}', type=int, default=0)
#                 pos = request.form.get(f'pos-{i}', type=int, default=0)
#                 report['details'][i][6] = par
#                 report['details'][i][7] = pos
#                 report['details'][i][8] = report['details'][i][4] - par - pos
#             save_reports()
#     return render_template('report_detail.html', report=report)
# =============================================================================


@app.route('/report/<report_id>')
def report_detail(report_id):
    report = get_report(report_id)
    if report is None:
        return render_template('404.html'), 404  # Render a 404 page if the report is not found
    return render_template('report_detail.html', report=report)
#-----

@app.route('/create', methods=['GET', 'POST'])
def create_report_route():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            report, report_id = create_report(file)
            if report:
                return redirect(url_for('report_detail', report_id=report_id))
        else:
            return "Error processing file", 500
    return render_template('create_report.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/report/<string:report_id>/delete', methods=['POST'])
def delete_report_route(report_id):
    delete_report(report_id)
    return redirect(url_for('view_reports'))

@app.route('/filter_items', methods=['POST'])
def filter_items():
    data = request.get_json()
    report_id = data['report_id']
    item_search = data['item_search']
    filtered_items = filter_item(report_id, item_search)
    return jsonify(filtered_items)

if __name__ == '__main__':
    load_reports()
    app.run(debug=True)






# =============================================================================
# '''
# STUDENT: Roberto Pocas Leitao
# TEAM NAME: DistillConnect
# DATE: June of 2024
# 
# '''
# 
# 
# '''
# NOTES:
#     
# This Python file is mostly done with the help of ChatGPT as I am not familiar with most of this.
# But I wanted to create it as a web application after getting the bulk of functionality working.
# Probably only about 20% is my work. But I did type it all in order to get used to the syntax.
# '''
# 
# 
# 
# # from flask import Flask, render_template, request, redirect, url_for
# # # import os
# # import report_manager
# # from report_manager import save_reports, load_reports, create_report, get_report, delete_report
# 
# # app = Flask(__name__)
# 
# # # reports =[] # moved to report_manager
# 
# 
# # @app.route('/')
# # def home():
# #     return render_template('home.html')
# 
# 
# # @app.route('/reports')
# # def view_reports():
# #     return render_template('view_reports.html', reports=report_manager.reports)
# 
# 
# # @app.route('/report/<int:report_id>', methods=['GET', 'POST'])
# # def report_detail(report_id):
# #     report = get_report(report_id)
# #     # report = next((r for r in reports if r['id'] == report_id), None) #------ moved this to report_manager so it's easier to find/change -----------
#     
# #     if request.method == 'POST':
# #         if 'update' in request.form:
# #             for i, row in enumerate(report['details'][1:], start=1):
# #                 par = request.form.get(f'par-{i}', type=int, default=0)
# #                 pos = request.form.get(f'pos-{i}', type=int, default=0)
# #                 report['details'][i][6] = par
# #                 report['details'][i][7] = pos
# #                 report['details'][i][8] = report['details'][i][4] - par - pos                
# #             save_reports()
# #         elif 'sort' in request.form:
# #             sort_by = request.form['sort']
# #             sort_index = report['details'][0].index(sort_by)
# #             report['details'] = [report['details'][0]] + sorted(report['details'][1:], key=lambda x: x[sort_index])
# #         elif'filter' in request.form:
# #             filter_term = request.form['filter']
# #             report['details'] = [report['details'][0]] + [row for row in report['details'][1:] if filter_term.lower() in str(row).lower()]
#             
# #     return render_template('report_detail.html', report=report)
#     
#         
# #     # sort_by = request.args.get('sort_by')
# #     # if sort_by:
# #     #     sort_index = report['details'][0].index(sort_by)
# #     #     report['details'] = [report['details'][0]] + sorted(report['details'][1:], key=lambda x: x[sort_index])
#         
# #     # # Filtering
# #     # filter_term = request.args.get('filter')
# #     # if filter_term:
# #     #     report['details'] = [report['details'][0]] + [row for row in report['details'][1:] if filter_term.lower() in str(row).lower()]
#     
# 
# 
# 
# # @app.route('/create', methods=['GET', 'POST'])
# # def create_report_route():
# #     if request.method == 'POST':
# #         # print(request) # testing
# #         file = request.files['file']
#         
# #         if file:
# #             report, report_id = create_report(file)
# #             if report:
# #                 return redirect(url_for('report_detail', report_id=report_id))
# #             # return redirect(url_for('report_detail', report_id=report['id'])) # was giving a str TypeError
#             
# #         else:
# #             return "Error processing file", 500
#             
# #     return render_template('create_report.html')
#          
# #         #------ moved this to report_manager so it's easier to find/change -----------       
# #             # report_id = len(reports) + 1
# #             # report = {
# #             #     'id': report_id,
# #             #     'title': file.filename,
# #             #     'date': '2024-05-27',
# #             #     'details': file.read().decode('utf-8')                
# #             # }
# #             # reports.append(report)
# #         #------------------------------------------------------------------------------
# 
# 
# 
# # @app.route('/instructions')
# # def instructions():
# #     return render_template('instructions.html')
# 
# 
# # @app.route('/report/<int:report_id>/delete', methods=['POST'])
# # def delete_report_route(report_id):
# #     print(f"Deleting report with ID: {report_id}")  # Debug statement
# #     report_manager.delete_report(report_id)
# #     return redirect(url_for('view_reports'))
# #     # delete_report(report_id)
# #     # return '', 204
# #     # return redirect(url_for('view_reports'))
#     
# #     # report_manager.delete_report(report_id)
# #     # global reports
# #     # reports = [r for r in reports if r['id'] != report_id] #------ moved this to report_manager so it's easier to find/change -----------
# #     # return '', 204
# 
# 
# # if __name__ == '__main__':
# #     app.run(debug=True)
#     
#     
# '''
# # =============================================================================
# # Version 2
# # 
# # =============================================================================
# '''
# # from flask import Flask, render_template, request, redirect, url_for
# # import report_manager
# # from report_manager import save_reports, load_reports, create_report, get_report, delete_report
# 
# # app = Flask(__name__)
# 
# # @app.route('/')
# # def home():
# #     return render_template('home.html')
# 
# # @app.route('/reports')
# # def view_reports():
# #     return render_template('view_reports.html', reports=report_manager.reports)
# 
# # @app.route('/report/<int:report_id>', methods=['GET', 'POST'])
# # def report_detail(report_id):
# #     report = get_report(report_id)
#     
# #     if request.method == 'POST':
# #         if 'update' in request.form:
# #             for i, row in enumerate(report['details'][1:], start=1):
# #                 par = request.form.get(f'par-{i}', type=int, default=0)
# #                 pos = request.form.get(f'pos-{i}', type=int, default=0)
# #                 report['details'][i][6] = par
# #                 report['details'][i][7] = pos
# #                 report['details'][i][8] = report['details'][i][4] - par - pos                
# #             save_reports()
# #         elif 'sort' in request.form:
# #             sort_by = request.form['sort']
# #             sort_index = report['details'][0].index(sort_by)
# #             report['details'] = [report['details'][0]] + sorted(report['details'][1:], key=lambda x: x[sort_index])
# #         elif 'filter' in request.form:
# #             filter_term = request.form['filter']
# #             report['details'] = [report['details'][0]] + [row for row in report['details'][1:] if filter_term.lower() in str(row).lower()]
#             
# #     return render_template('report_detail.html', report=report)
# 
# # @app.route('/create', methods=['GET', 'POST'])
# # def create_report_route():
# #     if request.method == 'POST':
# #         file = request.files['file']
#         
# #         if file:
# #             report, report_id = create_report(file)
# #             if report:
# #                 return redirect(url_for('report_detail', report_id=report_id))
# #         else:
# #             return "Error processing file", 500
#             
# #     return render_template('create_report.html')
# 
# # @app.route('/instructions')
# # def instructions():
# #     return render_template('instructions.html')
# 
# # @app.route('/report/<int:report_id>/delete', methods=['POST'])
# # def delete_report_route(report_id):
# #     report_manager.delete_report(report_id)
# #     return redirect(url_for('view_reports'))
# 
# # if __name__ == '__main__':
# #     app.run(debug=True)
# 
# 
# 
# '''
# # =============================================================================
# # Version 3
# # 
# # =============================================================================
# '''
# from flask import Flask, render_template, request, redirect, url_for, jsonify
# import sqlite3
# import pandas as pd
# from datetime import datetime
# from sqlalchemy import create_engine
# from flask_sqlalchemy import SQLAlchemy
# import report_manager
# from report_manager import save_reports, load_reports, create_report, get_report, delete_report, filter_item
# 
# 
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./reports.db'
# 
# db = SQLAlchemy(app)
# DATABASE = 'reports.db'
# 
# class Report(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(150), nullable=False)
#     date = db.Column(db.DateTime, default=datetime.utcnow)
#     details = db.Column(db.Text, nullable=False)
# 
# 
# 
# @app.route('/')
# def home():
#     return render_template('home.html')
# 
# @app.route('/reports')
# def view_reports():
#     return render_template('view_reports.html', reports=report_manager.reports)
# 
# 
# @app.route('/report/<int:report_id>', methods=['GET', 'POST'])
# def report_detail(report_id):
#     report = get_report(report_id)
# 
#     if request.method == 'POST':
#         if 'sort' in request.form:
#             sort_by = request.form['sort']
#             sort_index = report['details'][0].index(sort_by)
#             report['details'] = [report['details'][0]] + sorted(report['details'][1:], key=lambda x: x[sort_index])
#         elif 'filter' in request.form:
#             filter_term = request.form['filter']
#             report['details'] = [report['details'][0]] + [row for row in report['details'][1:] if filter_term.lower() in str(row).lower()]
#         else:
#             for i, row in enumerate(report['details'][1:], start=1):
#                 par = request.form.get(f'par-{i}', type=int, default=0)
#                 pos = request.form.get(f'pos-{i}', type=int, default=0)
#                 report['details'][i][6] = par
#                 report['details'][i][7] = pos
#                 report['details'][i][8] = report['details'][i][4] - par - pos
#             save_reports()
#     return render_template('report_detail.html', report=report)
# 
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
# @app.route('/filter_items', methods=['POST'])
# def filter_items():
#     data = request.get_json()
#     report_id = data['report_id']
#     item_search = data['item_search']
#     filtered_items = report_manager.filter_item(report_id, item_search)
#     return jsonify(filtered_items)
# 
# 
# 
# 
# '''
# 
# # =============================================================================
# # @app.route('/report/<int:report_id>', methods=['GET', 'POST'])
# # def report_detail(report_id):
# #     report = get_report(report_id)
# #     
# #     if request.method == 'POST':
# #         if 'update' in request.form:
# #             for i, row in enumerate(report['details'][1:], start=1):
# #                 par = request.form.get(f'par-{i}', type=int, default=0)
# #                 pos = request.form.get(f'pos-{i}', type=int, default=0)
# #                 report['details'][i][6] = par
# #                 report['details'][i][7] = pos
# #                 report['details'][i][8] = report['details'][i][4] - par - pos                
# #             save_reports()
# #         elif 'sort' in request.form:
# #             sort_by = request.form['sort']
# #             sort_index = report['details'][0].index(sort_by)
# #             report['details'] = [report['details'][0]] + sorted(report['details'][1:], key=lambda x: x[sort_index])
# #         elif 'filter' in request.form:
# #             filter_term = request.form['filter']
# #             report['details'] = [report['details'][0]] + [row for row in report['details'][1:] if filter_term.lower() in str(row).lower()]
# #             
# #     return render_template('report_detail.html', report=report)
# # =============================================================================
# 
# '''
# 
# 
# @app.route('/create', methods=['GET', 'POST'])
# def create_report_route():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file:
#             report, report_id = create_report(file)
#             if report:
#                 return redirect(url_for('report_detail', report_id=report_id))
#         else:
#             return "Error processing file", 500
#     return render_template('create_report.html')
# 
# 
# @app.route('/instructions')
# def instructions():
#     return render_template('instructions.html')
# 
# 
# @app.route('/report/<int:report_id>/delete', methods=['POST'])
# def delete_report_route(report_id):
#     report_manager.delete_report(report_id)
#     return redirect(url_for('view_reports'))
# 
# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)
# 
# 
# 
# '''
# # =============================================================================
# # Version 4
# # 
# # =============================================================================
# '''
# 
# # from flask import Flask, render_template, request, jsonify
# # import json
# 
# # app = Flask(__name__)
# 
# # # Load reports (assuming the reports are loaded here)
# # with open('reports.json', 'r') as f:
# #     reports = json.load(f)
# 
# # @app.route('/')
# # def index():
# #     return render_template('view_report.html', reports=reports)
# 
# # @app.route('/report/<int:report_id>')
# # def report_detail(report_id):
# #     report = next((r for r in reports if r['id'] == report_id), None)
# #     if not report:
# #         return "Report not found", 404
# #     return render_template('report_detail.html', report=report)
# 
# # @app.route('/update_report/<int:report_id>', methods=['POST'])
# # def update_report(report_id):
# #     data = request.json
# #     rowIndex = data['rowIndex']
# #     par = data['par']
# #     pos = data['pos']
# #     total = data['total']
# 
# #     # Update the report details
# #     for report in reports:
# #         if report['id'] == report_id:
# #             report['details'][rowIndex + 1][5] = par  # Update PAR
# #             report['details'][rowIndex + 1][6] = pos  # Update POs
# #             report['details'][rowIndex + 1][7] = total  # Update Total
# 
# #     # Save the updated reports back to the file
# #     with open('reports.json', 'w') as f:
# #         json.dump(reports, f)
# 
# #     return jsonify({'status': 'success'})
# 
# # if __name__ == '__main__':
# #     app.run(debug=True)
# 
# =============================================================================
