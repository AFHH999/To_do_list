#!/bin/python3

import sqlite3
import pandas as pd

def create_table ():
        # Connect to database
    with sqlite3.connect("database.db") as conn:
        # Create a cursor
        c = conn.cursor()
        # Creating a table
        c.execute("""CREATE TABLE IF NOT EXISTS
        Tasks (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Task TEXT NOT NULL,
            Due_Date TEXT,
            Status TEXT DEFAULT 'incomplete'
        )""")
        conn.commit()

def new_task():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        sql = "INSERT INTO Tasks (Task, Due_Date, Status) VALUES (?, ?, ?)"
        task = input("What is your task? ")
        due_date = input("When it expire (mm/dd/yyyy)? ")
        status = input("What is the status of your task? (if incomplete don't write) ")
        if not status.strip():
            status = "Incomplete"
        c.execute(sql, (task, due_date, status))
        conn.commit()

def list_tasks():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Tasks")
        results = c.fetchall()
        results_df = pd.DataFrame(results)
        results_df.columns = ['ID', 'Task', 'Due Date', 'Status']
        print(results_df.to_string(index=False))

def delete_task():
    try:
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            ID = int(input("Which task you need to erase? "))
            c.execute("DELETE FROM Tasks WHERE ID = ?", (ID,))
            conn.commit()
            print(f"Task with the ID {ID} deleted succesfully.")
    except sqlite3.Error as e:
        print("Error occurred:", e)

def main():
    create_table()
    while True:
        print("\nTo-Do list")
        try:
            option = int(input("""Write what do you want to do?
            1- To add a new task
            2- To see your list of tasks
            3- To delete your task
            4- Exit
            Choose an option: """))

            if option == 1:
                new_task()
            elif option == 2:
                list_tasks()
            elif option == 3:
                delete_task()
            elif option == 4:
                print("Goodbye!")
                break
            else:
                print("Please write a valid option! (1-4)")
        except ValueError:
            print("Please enter a number!")

if __name__ == "__main__":
    main()
