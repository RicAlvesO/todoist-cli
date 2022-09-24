from todoist_api_python.api import TodoistAPI
from simple_term_menu import TerminalMenu
import get_access
import calls


def menu(api):
    print('\033[2J')
    menu_items=["Create Project", "Create Task", "List projects",
                "List tasks", "List tasks from project", "Close Task",
                "Remove Project","Remove Task","Exit"]

    terminal_menu = TerminalMenu(menu_items, title="Main Menu")
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        calls.create_project(api)
    elif menu_entry_index == 1:
        calls.create_task(api)
    elif menu_entry_index == 2:
        calls.list_projects(api)
    elif menu_entry_index == 3:
        calls.list_tasks(api)
    elif menu_entry_index == 4:
        calls.list_tasks_from_project(api)
    elif menu_entry_index == 5:
        calls.close_task(api)
    elif menu_entry_index == 6:
        calls.remove_project(api)
    elif menu_entry_index == 7:
        calls.remove_task(api)
    else:
        return False
    input("\nPress Enter to continue...")
    return True


if __name__ == "__main__":
    get_access.check_token()
    token=get_access.load_token()
    api=TodoistAPI(token)
    while menu(api):
        pass
