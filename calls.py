from todoist_api_python.api import TodoistAPI
from simple_term_menu import TerminalMenu
from datetime import datetime


"""Gets id of specified project by name"""
def get_project_by_name(api, name):
    project = api.get_projects()
    for i in project:
        if (i.name).lower()==name.lower():
            return i.id
    return None

"""Shows all projects"""
def list_projects(api):
    projects = api.get_projects()
    print("Projects:")
    child=1
    for i in projects:
        if i.parent_id==None:
            child=1
        else:
            child=child+1
        print((child*3*' ')+"{}->\33[0m {}".format(color_trans(i.color),i.name))

"""Shows all projects and their respective tasks"""
def list_tasks(api):
    projects = api.get_projects()
    tasks = api.get_tasks()
    print("All Tasks:")
    child=1;
    for i in projects:
        if i.parent_id==None:
            child=1
        else:
            child=child+1
        print((3*child*' ')+"{}->\33[0m {}".format(color_trans(i.color), i.name))
        child=child+1
        for j in tasks:
            if j.project_id==i.id:
                print((3*child*' ')+"{}->\33[0m {};".format(prio_trans(j.priority),j.content))

"""Shows all tasks from specified project"""
def list_tasks_from_project(api):
    project_id = project_menu(api)[1]
    if project_id==0:
        return
    proj = api.get_project(project_id)
    tasks = api.get_tasks(project_id=project_id)
    print("\033[2JTasks from {}{}\33[0m:".format(color_trans(proj.color), proj.name))
    for i in tasks:
        print("  {}->\33[0m {}".format(prio_trans(i.priority),i.content))
        if len(i.description)>0:
            print("     {}".format(i.description))
        if i.due.date!=None:
            print("     {}".format(i.due.date))

"""Create new project"""
def create_project(api):
    name = input("Project name: ")
    if len(name)<1:
        print("Invalid project name")
        return
    color = color_menu()
    print("Color: {}".format(color[0]))
    try:
        api.add_project(name,color=color[1])
    except:
        print("Could not create new project")

"""Create new child project"""
def create_child_project(api):
    project = project_menu(api)
    if project[1]==0:
        return
    print("Project: {}".format(project[0]))
    name = input("Project name: ")
    if len(name)<1:
        print("Invalid project name")
        return
    color = color_menu()
    print("Color: {}".format(color[0]))
    try: 
        api.add_project(name,parent_id=project[1],color=color[1])
    except:
        print("Could not create new child project!")

"""Creates a task inside a project"""
def create_task(api):
    project = project_menu(api)
    if project[1]==0:
        return
    print("Project: {}".format(project[0]))
    name = input("Task: ")
    if len(name)<1:
        print("Invalid Task")
        return
    desc = input("Description (Default=NONE): ")
    prio=1
    while True:
        inpt = input("Priority (Default=1): ")
        if len(inpt)<1:
            break
        elif int(inpt)<1 or int(inpt)>4:
            print("Invalid priority")
        else:
            prio=int(inpt)
            break
    dt=""
    while True:
        dt = input("Limit Date (Default=NONE, Format:YYYY-MM-DD): ")
        if len(dt)<1:
            break
        try:
            if dt != datetime.strptime(dt, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            break
        except ValueError:
            print("Invalid date")

    ##############################
    #          IN FUTURE         #
    ##############################
    # ADD LABELS                 #
    ##############################
    try:
        if len(dt)<1:
            api.add_task(content=name,description=desc,priority=prio,project_id=project[1])
        else:
            api.add_task(content=name,description=desc,priority=prio,project_id=project[1],due_date=dt)
    except:
        print("Could not create new task")

"""Finishes a task"""
def close_task(api):
    project_id = project_menu(api)[1]
    if project_id==0:
        return
    tasks = api.get_tasks(project_id=project_id)
    task=task_menu(tasks)
    if task[1]==0: 
        return
    try:
        api.close_task(task_id=task[1])
        print("Task \'{}\' closed".format(task[0]))
    except:
        print("Could not close task")

"""Remove existing project"""
def remove_project(api):
    project_id = project_menu(api)[1]
    if project_id!=0:
        api.delete_project(project_id)

"""Removes an existing task"""
def remove_task(api):
    project_id = project_menu(api)[1]
    if project_id==0:
        return
    tasks = api.get_tasks(project_id=project_id)
    task=task_menu(tasks)
    if task[1]==0: 
        return
    try:
        api.delete_task(task_id=task[1])
        print("Task \'{}\' removed".format(task[0]))
    except:
        print("Could not remove task")

"""Shows all projects for selection"""
def project_menu(api):
    projects = api.get_projects()
    names = []
    ids = []
    for i in projects:
        names.append(i.name)
        ids.append(i.id)
    names.append("Cancel")
    ids.append(0)
    terminal_menu = TerminalMenu(names, title="Projects:")
    menu_entry_index = terminal_menu.show()
    return [names[menu_entry_index],ids[menu_entry_index]]

"""Shows all tasks for selection"""
def task_menu(tasks):
    names = []
    ids = []
    for i in tasks:
        names.append(i.content)
        ids.append(i.id)
    names.append("Cancel")
    ids.append(0)
    terminal_menu = TerminalMenu(names, title="Tasks:")
    menu_entry_index = terminal_menu.show()
    return [names[menu_entry_index], ids[menu_entry_index]]

"""Shows all available colors for selection"""
def color_menu():
    names = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Pink", "Grey"]
    ids=['31','32','33','35','41','42','44','48']
    terminal_menu = TerminalMenu(names, title="Color:")
    menu_entry_index = terminal_menu.show()
    return [names[menu_entry_index],ids[menu_entry_index]]

"""Translates color codes to terminal escape sequences"""
def color_trans(name):
    if name==31 or name=='red':
        return '\u001b[38;5;160m'
    if name==32 or name=='orange':
        return '\u001b[38;5;208m'
    if name==33 or name=='yellow':
        return '\u001b[38;5;190m'
    if name==35 or name=='lime_green':
        return '\u001b[38;5;46m'
    if name==41 or name=='blue':
        return '\u001b[38;5;45m'
    if name==42 or name=='grape':
        return '\u001b[38;5;54m'
    if name==44 or name=='lavander':
        return '\u001b[38;5;200m'
    if name==48 or name=='grey':
        return '\u001b[38;5;250m'
    return '\33[0m'
    
"""Gives color to task according to priority"""
def prio_trans(name):
    if name==1:
        return '\u001b[38;5;83m'
    if name==2:
        return '\u001b[38;5;226m'
    if name==3:
        return '\u001b[38;5;208m'
    if name==4:
        return '\u001b[38;5;196m'
    return '\33[0m'
