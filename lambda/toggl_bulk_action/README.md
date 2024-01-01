# Toggl bulk actions
bulk CRUD actions on the Toggl API user account

## events_delete_from_dates
deletes events from specified date range start and end

### request arguments

START_DATE: query start date YYYY-DD-MM

END_DATE: query end date YYYY-DD-MM

### response
acknowledgement success or failure with error messages

## (FUTURE) std_events_get
fetches Toggl events from start to end date converted to standard format as a list of dictionaries

### request arguments

START_DATE: query start date YYYY-DD-MM

END_DATE: query end date YYYY-DD-MM

### response

## (FUTURE) events_get
fetches Toggl events from API as-is

### request arguments

START_DATE: query start date YYYY-DD-MM

END_DATE: query end date YYYY-DD-MM

### response
