import csv
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
    return render_template('alert.html')

@app.route('/calculateAlerts', methods=['POST'])
def calculateAlerts():
    dataset_file = request.files['csvFile']
    try:
        results = calculate_alert_percentages(dataset_file)
        return json.dumps(results)
    except Exception as e:
        return jsonify({'msg': 'Invalid file'}), 1001

def calculate_alert_percentages(dataset):
    emp_data = []
    total_alerts = 0
    str_file_value = dataset.read().decode('utf-8')
    file = str_file_value.splitlines()
    csv_reader = csv.reader(file, delimiter=',')
    header = next(csv_reader)  # Skip the header row
    emp_id_index = header.index('empId')
    alert_index = header.index('alert')
    if emp_id_index != -1 or alert_index != -1:
        for row in csv_reader:
            emp_id = row[emp_id_index]
            alert = row[alert_index]
            emp_data.append([emp_id, alert])
            total_alerts += 1

        emp_alerts = {}
        for emp_id, alert in emp_data:
            if emp_id not in emp_alerts:
                emp_alerts[emp_id] = {'Total Alerts': 0, 'Distress Alerts': 0, 'Fall Alerts': 0}
            emp_alerts[emp_id]['Total Alerts'] += 1
            if alert == 'DISTRESS':
                emp_alerts[emp_id]['Distress Alerts'] += 1
            elif alert == 'FALL':
                emp_alerts[emp_id]['Fall Alerts'] += 1

        results = []
        for emp_id, alerts in emp_alerts.items():
            total_emp_alerts = alerts['Total Alerts']
            distress_alerts = alerts['Distress Alerts']
            fall_alerts = alerts['Fall Alerts']
            total_percentage = total_emp_alerts / total_alerts * 100
            distress_percentage = distress_alerts / total_emp_alerts * 100
            fall_percentage = fall_alerts / total_emp_alerts * 100
            results.append({
                'empId': emp_id,
                'noOfAlerts': total_emp_alerts,
                'alertsToTotal': total_percentage,
                'noOfDistressAlerts': distress_alerts,
                'distressAlertsToSubtotal': distress_percentage,
                'noOfFallAlerts': fall_alerts,
                'fallAlertsToSubtotal': fall_percentage
            })

        return results
    else:
        return -1

if __name__ == '__main__':
    app.run()
