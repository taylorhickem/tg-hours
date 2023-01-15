'''time tracking reports from Toggl Track app user data
'''
# -----------------------------------------------------
# Import
# -----------------------------------------------------
import sys
import ctypes

from tghours import hours

# -----------------------------------------------------
# Module variables
# -----------------------------------------------------
# -----------------------------------------------------
# Setup
# -----------------------------------------------------

# -----------------------------------------------------
# Reports
# -----------------------------------------------------


def update_events():
    '''Update events database sqlite and gsheet with new NowThen records
    '''
    hours.load()
    hours.update_events()

def update_activity_report():
    pass

# -----------------------------------------------------
# User interface
# -----------------------------------------------------


def message_box(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


# -----------------------------------------------------
# Command line interface
# -----------------------------------------------------
def autorun():
    if len(sys.argv) > 1:
        process_name = sys.argv[1]
        if process_name == 'update_events':
            update_events()
        elif process_name == 'update_activity_report':
            update_activity_report()
    else:
        print('no report specified')

if __name__ == "__main__":
    autorun()
# -----------------------------------------------------
# ***
# -----------------------------------------------------