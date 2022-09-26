#!/usr/bin/env python3
from todoist_api_python.api import TodoistAPI
from simple_term_menu import TerminalMenu
import get_access
import calls

"""Main App Menu"""
def menu(api):
    print('\033[2J')
    menu_items=["[1] Create Task",   "[2] Create Project", "[3] Create Child Project",
                "[4] List projects", "[5] List tasks",     "[6] List tasks from project",
                "[7] Close Task",    "[8] Remove Project", "[9] Remove Task",
                "[0] Exit"]

    terminal_menu = TerminalMenu(menu_items, title="Main Menu")
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        calls.create_task(api)
    elif menu_entry_index == 1:
        calls.create_project(api)
    elif menu_entry_index == 2:
        calls.create_child_project(api)
    elif menu_entry_index == 3:
        calls.list_projects(api)
    elif menu_entry_index == 4:
        calls.list_tasks(api)
    elif menu_entry_index == 5:
        calls.list_tasks_from_project(api)
    elif menu_entry_index == 6:
        calls.close_task(api)
    elif menu_entry_index == 7:
        calls.remove_project(api)
    elif menu_entry_index == 8:
        calls.remove_task(api)
    else:
        return False
    input("\nPress Enter to continue...")
    return True

"""Main function"""
if __name__ == "__main__":
    get_access.check_token()
    token=get_access.load_token()
    api=TodoistAPI(token)
    while menu(api):
        pass
