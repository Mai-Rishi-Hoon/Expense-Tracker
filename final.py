from flask import Flask, render_template, request, redirect, url_for

import mysql.connector as mysql

con = mysql.connect(host='localhost', user='root', password='rishi', database='expense', charset='utf8')
cur = con.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_expense', methods=['GET'])
def add_expense():
    if request.method == 'GET':
        name = request.args.get('name')
        exp_name = request.args.get('exp_name')
        expense = request.args.get('exp')
        date = request.args.get('date')

        try:
            s = "INSERT INTO expense (Name, Expense_name, Expense, Date) VALUES (%s, %s, %s, %s)"
            b = (name, exp_name, expense, date)
            cur.execute(s, b)
            con.commit()
        except Exception as e:
            return f"Error adding expense: {e}"

    return redirect(url_for('index'))

@app.route('/delete_expense', methods=['GET'])
def delete_expense():
    if request.method == 'GET':
        name = request.args.get('name')
        exp_name = request.args.get('exp_name')
        expense = request.args.get('exp')
        date = request.args.get('date')

        try:
            s = "DELETE FROM expense WHERE Name = %s and Expense_Name = %s and Expense = %s and Date = %s"
            b = (name, exp_name, expense, date)
            cur.execute(s, b)
            con.commit()
        except Exception as e:
            return f"Error deleting expense: {e}"

    return redirect(url_for('index'))

@app.route('/search_expense', methods=['GET'])
def search_expense():
    print('Hello')
    if request.method == 'GET':
        name = request.args.get('name')

        try:
            # Query the database based on the provided name
            s = "SELECT * FROM expense WHERE Name = %s"
            b = (name,)
            cur.execute(s, b)
            # records
            records = cur.fetchall()
            # search_results=records
            print(f"Records: {records}")
            # Pass the retrieved records to the HTML template
            return render_template('index.html', search_results=records)
        except Exception as e:
            return f"Error searching expense: {e}"

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
