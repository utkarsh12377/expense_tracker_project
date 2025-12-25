import json
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = 'expenses.json'

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=4)

@app.route('/')
def index():
    expenses = load_expenses()
    total = sum(exp['amount'] for exp in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add_expense():
    amount = float(request.form['amount'])
    description = request.form['description']
    category = request.form['category']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    expenses = load_expenses()
    expenses.append({'amount': amount, 'description': description, 'category': category, 'date': date})
    save_expenses(expenses)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete_expense(index):
    expenses = load_expenses()
    if 1 <= index <= len(expenses):
        expenses.pop(index - 1)
        save_expenses(expenses)
    return redirect(url_for('index'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_expense(index):
    expenses = load_expenses()
    if not (1 <= index <= len(expenses)):
        return redirect(url_for('index'))
    expense = expenses[index - 1]
    if request.method == 'POST':
        expense['amount'] = float(request.form['amount'])
        expense['description'] = request.form['description']
        expense['category'] = request.form['category']
        save_expenses(expenses)
        return redirect(url_for('index'))
    return render_template('edit.html', expense=expense, index=index)

if __name__ == "__main__":
    app.run(debug=True)