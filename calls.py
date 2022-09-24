from todoist_api_python.api import TodoistAPI
from simple_term_menu import TerminalMenu


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
    for i in projects:
        print("{}  -> {}\33[0m".format(color_trans(i.color),i.name))


def list_tasks(api):
    projects = api.get_projects()
    print("All Tasks:")
    for i in projects:
        print("  -> {}{}\33[0m".format(color_trans(i.color), i.name))
        tasks = api.get_tasks(project_id=i.id)
        for j in tasks:
            print("     -> {}{}\33[0m;".format(prio_trans(j.priority),j.content))

"""Shows all tasks from specified project"""
def list_tasks_from_project(api):
    project_id = project_menu(api)[1]
    if project_id==0:
        return
    proj = api.get_project(project_id)
    tasks = api.get_tasks(project_id=project_id)
    print("\033[2JTasks from {}{}\33[0m:".format(color_trans(proj.color), proj.name))
    for i in tasks:
        print("  -> {}{}\33[0m".format(prio_trans(i.priority),i.content))
        if len(i.description)>0:
            print("     {}".format(i.description))

"""Create new project"""
def create_project(api):
    name = input("Project name: ")
    if len(name)<1:
        print("Invalid project name")
        return
    color = color_menu()
    print("Color: {}".format(color[0]))
    api.add_project(name,color=color[1])


def create_task(api):
    project = project_menu(api)
    if project[1]==0:
        return
    print("Project: {}".format(project[0]))
    name = input("Task: ")
    if len(name)<1:
        print("Invalid Task")
        return
    desc = input("Description (Default=Empty): ")
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

    ##############################
    #          IN FUTURE         #
    ##############################
    # ADD DATES                  #
    # ADD LABELS                 #
    ##############################

    api.add_task(content=name,description=desc,priority=prio,project_id=project[1])

def close_task(api):
    project_id = project_menu(api)[1]
    if project_id==0:
        return
    tasks = api.get_tasks(project_id=project_id)
    task=task_menu(tasks)
    if task[1]==0: 
        return
    api.close_task(task_id=task[1])
    print("Task \'{}\' closed".format(task[0]))

"""Remove existing project"""
def remove_project(api):
    project_id = project_menu(api)[1]
    if project_id!=0:
        api.delete_project(project_id)

def remove_task(api):
    project_id = project_menu(api)[1]
    if project_id==0:
        return
    tasks = api.get_tasks(project_id=project_id)
    task=task_menu(tasks)
    if task[1]==0: 
        return
    api.delete_task(task_id=task[1])
    print("Task \'{}\' removed".format(task[0]))

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
    if name==31:
        return '\u001b[38;5;160m'
    if name==32:
        return '\u001b[38;5;208m'
    if name==33:
        return '\u001b[38;5;190m'
    if name==35:
        return '\u001b[38;5;46m'
    if name==41:
        return '\u001b[38;5;45m'
    if name==42:
        return '\u001b[38;5;54m'
    if name==44:
        return '\u001b[38;5;200m'
    if name==48:
        return '\u001b[38;5;250m'
    return '\33[0m'
    
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
