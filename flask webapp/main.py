from flask import Flask, render_template, request, redirect
from flask import jsonify

app = Flask(__name__, template_folder="templates")

tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    task = request.form['task']
    tasks.append(task)
    return redirect('/')

@app.route('/delete/<int:task_index>', methods=['DELETE'])
def delete_task(task_index):
    if task_index < len(tasks):
        del tasks[task_index]
        return jsonify({'message': 'Task deleted successfully'})
    else:
        return jsonify({'message': 'Task not found'})


if __name__ == '__main__':
    app.run()
