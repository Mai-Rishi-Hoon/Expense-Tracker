from flask import Flask, render_template, request, redirect, url_for
import mysql.connector as mysql

app = Flask(__name__)

# Replace these credentials with your actual MySQL database credentials
con = mysql.connect(host='localhost', user='root', password='rishi', database='expense', charset='utf8')
cur = con.cursor()

# Secret key for CSRF protection
app.secret_key = 'your_secret_key'

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            s = "SELECT * FROM login WHERE username = %s AND password = %s"
            b = (username, password)
            cur.execute(s, b)
            res = cur.fetchall()

            print(f"Rowcount: {cur.rowcount}")
            print(f"Result: {res}")

            if cur.rowcount == 1:
                return redirect(url_for('index'))
            else:
                print("Wrongggggg !!!!")
                return redirect(url_for('login'))
        except Exception as e:
            return f"Error logging In: {e}"

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if request.method == 'POST':
        name = request.form.get('name')
        exp_name = request.form.get('exp_name')
        expense = request.form.get('exp')
        date = request.form.get('date')

        try:
            s = "INSERT INTO expense (Name, Expense_name, Expense, Date) VALUES (%s, %s, %s, %s)"
            b = (name, exp_name, expense, date)
            cur.execute(s, b)
            con.commit()
        except Exception as e:
            return f"Error adding expense: {e}"

    return redirect(url_for('index'))

@app.route('/delete_expense', methods=['POST'])
def delete_expense():
    if request.method == 'POST':
        name = request.form.get('name')
        exp_name = request.form.get('exp_name')
        expense = request.form.get('exp')
        date = request.form.get('date')

        try:
            s = "DELETE FROM expense WHERE Name = %s and Expense_Name = %s and Expense = %s and Date = %s"
            b = (name, exp_name, expense, date)
            cur.execute(s, b)
            con.commit()
        except Exception as e:
            return f"Error deleting expense: {e}"

    return redirect(url_for('index'))

@app.route('/search_expense', methods=['POST'])
def search_expense():
    if request.method == 'POST':
        name = request.form.get('name')

        try:
            s = "SELECT * FROM expense WHERE Name = %s"
            b = (name,)
            cur.execute(s, b)
            records = cur.fetchall()

            print(f"Records: {records}")

            return render_template('index.html', search_results=records)
        except Exception as e:
            return f"Error searching expense: {e}"

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
