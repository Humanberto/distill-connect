'''
STUDENT: Roberto Pocas Leitao
TEAM NAME: DistillConnect
DATE: June of 2024

'''


'''
NOTES:
    
This Python file is mostly done with the help of ChatGPT as I am not familiar with most of this.
But I wanted to create it as a web application after getting the bulk of functionality working.
Probably only about 20% is my work. But I did type it all in order to get used to the syntax.
'''



# from flask import Flask, render_template, request, redirect, url_for
# # import os
# import report_manager
# from report_manager import save_reports, load_reports, create_report, get_report, delete_report

# app = Flask(__name__)

# # reports =[] # moved to report_manager


# @app.route('/')
# def home():
#     return render_template('home.html')


# @app.route('/reports')
# def view_reports():
#     return render_template('view_reports.html', reports=report_manager.reports)


# @app.route('/report/<int:report_id>', methods=['GET', 'POST'])
# def report_detail(report_id):
#     report = get_report(report_id)
#     # report = next((r for r in reports if r['id'] == report_id), None) #------ moved this to report_manager so it's easier to find/change -----------
    
#     if request.method == 'POST':
#         if 'update' in request.form:
#             for i, row in enumerate(report['details'][1:], start=1):
#                 par = request.form.get(f'par-{i}', type=int, default=0)
#                 pos = request.form.get(f'pos-{i}', type=int, default=0)
#                 report['details'][i][6] = par
#                 report['details'][i][7] = pos
#                 report['details'][i][8] = report['details'][i][4] - par - pos                
#             save_reports()
#         elif 'sort' in request.form:
#             sort_by = request.form['sort']
#             sort_index = report['details'][0].index(sort_by)
#             report['details'] = [report['details'][0]] + sorted(report['details'][1:], key=lambda x: x[sort_index])
#         elif'filter' in request.form:
#             filter_term = request.form['filter']
#             report['details'] = [report['details'][0]] + [row for row in report['details'][1:] if filter_term.lower() in str(row).lower()]
            
#     return render_template('report_detail.html', report=report)
    
        
#     # sort_by = request.args.get('sort_by')
#     # if sort_by:
#     #     sort_index = report['details'][0].index(sort_by)
#     #     report['details'] = [report['details'][0]] + sorted(report['details'][1:], key=lambda x: x[sort_index])
        
#     # # Filtering
#     # filter_term = request.args.get('filter')
#     # if filter_term:
#     #     report['details'] = [report['details'][0]] + [row for row in report['details'][1:] if filter_term.lower() in str(row).lower()]
    



# @app.route('/create', methods=['GET', 'POST'])
# def create_report_route():
#     if request.method == 'POST':
#         # print(request) # testing
#         file = request.files['file']
        
#         if file:
#             report, report_id = create_report(file)
#             if report:
#                 return redirect(url_for('report_detail', report_id=report_id))
#             # return redirect(url_for('report_detail', report_id=report['id'])) # was giving a str TypeError
            
#         else:
#             return "Error processing file", 500
            
#     return render_template('create_report.html')
         
#         #------ moved this to report_manager so it's easier to find/change -----------       
#             # report_id = len(reports) + 1
#             # report = {
#             #     'id': report_id,
#             #     'title': file.filename,
#             #     'date': '2024-05-27',
#             #     'details': file.read().decode('utf-8')                
#             # }
#             # reports.append(report)
#         #------------------------------------------------------------------------------



# @app.route('/instructions')
# def instructions():
#     return render_template('instructions.html')


# @app.route('/report/<int:report_id>/delete', methods=['POST'])
# def delete_report_route(report_id):
#     print(f"Deleting report with ID: {report_id}")  # Debug statement
#     report_manager.delete_report(report_id)
#     return redirect(url_for('view_reports'))
#     # delete_report(report_id)
#     # return '', 204
#     # return redirect(url_for('view_reports'))
    
#     # report_manager.delete_report(report_id)
#     # global reports
#     # reports = [r for r in reports if r['id'] != report_id] #------ moved this to report_manager so it's easier to find/change -----------
#     # return '', 204


# if __name__ == '__main__':
#     app.run(debug=True)
    
    
'''
# =============================================================================
# Version 2
# 
# =============================================================================
'''
from flask import Flask, render_template, request, redirect, url_for
import report_manager
from report_manager import save_reports, load_reports, create_report, get_report, delete_report

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reports')
def view_reports():
    return render_template('view_reports.html', reports=report_manager.reports)

@app.route('/report/<int:report_id>', methods=['GET', 'POST'])
def report_detail(report_id):
    report = get_report(report_id)
    
    if request.method == 'POST':
        if 'update' in request.form:
            for i, row in enumerate(report['details'][1:], start=1):
                par = request.form.get(f'par-{i}', type=int, default=0)
                pos = request.form.get(f'pos-{i}', type=int, default=0)
                report['details'][i][6] = par
                report['details'][i][7] = pos
                report['details'][i][8] = report['details'][i][4] - par - pos                
            save_reports()
        elif 'sort' in request.form:
            sort_by = request.form['sort']
            sort_index = report['details'][0].index(sort_by)
            report['details'] = [report['details'][0]] + sorted(report['details'][1:], key=lambda x: x[sort_index])
        elif 'filter' in request.form:
            filter_term = request.form['filter']
            report['details'] = [report['details'][0]] + [row for row in report['details'][1:] if filter_term.lower() in str(row).lower()]
            
    return render_template('report_detail.html', report=report)

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

@app.route('/report/<int:report_id>/delete', methods=['POST'])
def delete_report_route(report_id):
    report_manager.delete_report(report_id)
    return redirect(url_for('view_reports'))

if __name__ == '__main__':
    app.run(debug=True)
