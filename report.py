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


def update_events(report_date, window_days=None):
    '''Update events database sqlite and gsheet with new NowThen records
    '''
    hours.load()
    hours.report_update(report_date, window_days)


def sync():
    hours.db_sync()


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
            if len(sys.argv) > 2:
                report_date = sys.argv[2]
                if len(sys.argv) > 3:
                    window_days = int(sys.argv[3])
                    update_events(report_date, window_days)
                else:
                    update_events(report_date)
            else:
                update_events(None)
        elif process_name == 'update_activity_report':
            update_activity_report()
        elif process_name == 'sync':
            sync()
    else:
        print('no report specified')


if __name__ == "__main__":
    autorun()
# -----------------------------------------------------
# ***
# -----------------------------------------------------