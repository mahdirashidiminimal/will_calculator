import sqlite3
from datetime import date
import models

class Repository:
    def __init__(self, ):

        # loading database
        self.conn = sqlite3.connect('database\will_calculator.db')
        # Create a cursor object
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT,
                time_spent INTEGER,
                difficulty INTEGER,
                time_created DATE
            )
        ''')
        self.conn.commit()

    def add_task(self, title: str, time_spent: int, difficulty: int):
        # Insert data into the table
        self.cursor.execute("SELECT MAX(id) + 1 FROM tasks;")
        id = self.cursor.fetchall()[0][0]
        if id == None:
            id = 1
        task = models.Task(id=id, title=title, time_spent=time_spent,
                           difficulty=difficulty, time_created=str(date.today()))
        self.cursor.execute('''
            INSERT INTO tasks (title, time_spent, difficulty, time_created)
            VALUES (?, ?, ?, ?)
        ''', (title, int(time_spent), difficulty, task.time_created))

        # Commit the changes
        self.conn.commit()
        return task

    def get_all_tasks(self):
        self.cursor.execute('''
            SELECT * FROM tasks
        ''')

        tasks = self.cursor.fetchall()
        tasks = [models.Task(id=task[0],
                             title=task[1],
                             time_spent=task[2],
                             difficulty=task[3],
                             time_created=task[4]) for task in tasks]
        return tasks

    def delete_task(self, task_id: int):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def restart_tasks(self):
        self.cursor.execute("DELETE FROM tasks")
        self.conn.commit()
        tasks = self.get_all_tasks()
        print()
