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



from flask import Flask, render_template, request, redirect, url_for
import os
import report_manager

app = Flask(__name__)

# reports =[] # moved to report_manager


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/reports')
def view_reports():
    return render_template('view_reports.html', reports=report_manager.reports)


@app.route('/report/<int:report_id>')
def report_detail(report_id):
    report = report_manager.get_report(report_id)
    # report = next((r for r in reports if r['id'] == report_id), None) #------ moved this to report_manager so it's easier to find/change -----------
    return render_template('report_detail.html', report=report)


@app.route('/create', methods=['GET', 'POST'])
def create_report():
    if request.method == 'POST':
        # print(request) # testing
        file = request.files['file']
        if file:
            report = report_manager.create_report(file)
            if report:
                return redirect(url_for('report_detail', report_id=report['id']))
            else:
                return "Error processing file", 500
            
    return render_template('create_report.html')
         
        #------ moved this to report_manager so it's easier to find/change -----------       
            # report_id = len(reports) + 1
            # report = {
            #     'id': report_id,
            #     'title': file.filename,
            #     'date': '2024-05-27',
            #     'details': file.read().decode('utf-8')                
            # }
            # reports.append(report)
        #------------------------------------------------------------------------------



@app.route('/instructions')
def instructions():
    return render_template('instructions.html')


@app.route('/report/<int:report>/delete', methods=['DELETE'])
def delete_report(report_id):
    report_manager.delete_report(report_id)
    # global reports
    # reports = [r for r in reports if r['id'] != report_id] #------ moved this to report_manager so it's easier to find/change -----------
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
    
    

