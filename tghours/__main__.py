import sys
from tghours import hours


def run():
    if len(sys.argv) > 1:
        function_name = sys.argv[0]
        if function_name == 'update_events':
            if len(sys.argv) > 2:
                report_date = sys.argv[1]
                hours.update_events(report_date)
            else:
                hours.update_events()


if __name__ == '__main__':
    run()