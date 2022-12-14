import random

HELP = """
help - print help for the program;
add - add a task to the list (the name of the task is requested from the user);
show - print all added tasks;
random - add a random task for Today."""

RANDOM_TASKS = ['первое', 'второе', 'третье']

tasks = {}

run = True

def add_todo(date, task):
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = []
        tasks[date].append(task)
    print("Task -", task, "- has been added for the date", date)


while run:
    command = input("Enter a request: ")
    if command == "help":
        print(HELP)

    elif command == "show":
        date = input("Enter a date to display the task list: ")
        if date in tasks:
            for task in tasks[date]:
                print('- ', task)
        else:
            print("No tasks")

    elif command == "add":
        date = input("Enter a date: ")
        task = input("Add a task: ")
        add_todo(date, task)

    elif command == 'random':
        task = random.choice(RANDOM_TASKS)
        add_todo("Today", task)
    else:
        print("Unknown request")
        run = False
print("Good bye!")
