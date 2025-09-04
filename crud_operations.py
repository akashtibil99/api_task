import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory "database"
employees = {
    1: {"name": "Akash", "role": "Data Scientist"},
    2: {"name": "Shivam", "role": "Software Developer"}
}

# GET - fetch all employees
@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)

# GET - fetch single employee
@app.route("/employees/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    emp = employees.get(emp_id)
    if emp:
        return jsonify(emp)
    return jsonify({"error": "Employee not found"}), 404

# POST - add new employee
@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.json
    emp_id = max(employees.keys()) + 1
    employees[emp_id] = data
    return jsonify({"id": emp_id, "data": data}), 201

# PUT - update employee
@app.route("/employees/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    if emp_id in employees:
        employees[emp_id] = request.json
        return jsonify({"id": emp_id, "data": employees[emp_id]})
    return jsonify({"error": "Employee not found"}), 404

# DELETE - remove employee
@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    if emp_id in employees:
        deleted = employees.pop(emp_id)
        return jsonify({"deleted": deleted})
    return jsonify({"error": "Employee not found"}), 404

if __name__ == "__main__":
    # host="0.0.0.0" makes it available on other devices in LAN
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
