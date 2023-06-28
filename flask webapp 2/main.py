from flask import Flask, render_template, request, redirect
from flask import jsonify
from flask import g
import sqlite3

#Initialize Flask instance
app = Flask(__name__, template_folder="templates")

#initialize sqlite to store to-do tasks into database
conn = sqlite3.connect('todo.db')
#cursor to store sqlite objects
cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT
        )''')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('todo.db')
    return db

tasks = []

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add.html')
def add(): 
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    return render_template('add.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    task = request.form['task']
    tasks.append(task)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    cursor.close()
    return redirect('/')

@app.route('/delete/<int:task_index>', methods=['DELETE'])
def delete_task(task_index):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_index,))
    conn.commit()
    cursor.close()
    if task_index < len(tasks):
        del tasks[task_index]
        return jsonify({'message': 'Task deleted successfully'})
    else:
        return jsonify({'message': 'Task not found'})
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run()
