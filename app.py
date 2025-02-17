from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

#function to work with database
def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row # для удобной работы с результатами
    return conn

# Главная страница с задачами
@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall() # Получаем все задачи
    conn.close()
    return render_template('index.html', tasks=tasks)


# Добавление новой задачи
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (task, done) VALUES (?, ?)', (task, 0))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

#Обновление статуса задачи (выполненф или нет)
@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

#Удаление задачи
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)