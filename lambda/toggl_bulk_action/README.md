# Toggl bulk actions
bulk CRUD actions on the Toggl API user account

## events_delete_from_dates
deletes events from specified date range start and end

### request arguments

ACTION_TYPE: "events_delete"

DATE_START: query start date YYYY-DD-MM

DATE_END: query end date YYYY-DD-MM

### response
```
{
    "status_code": HTML status code,
    "message": summary message success or failure,
    "request": {...} JSON copy of the user request
}
```

## events_get
fetches Toggl events from API as-is

### request arguments

ACTION_TYPE: "events_get"

DATE_START: query start date YYYY-DD-MM

DATE_END: query end date YYYY-DD-MM

### response
```
{
    "status_code": HTML status code,
    "message": summary message success or failure,
    "data": [...] events as a JSON list,
    "request": {...} JSON copy of the user request 
}
```

## (FUTURE) std_events_get
fetches Toggl events from start to end date converted to standard format as a list of dictionaries

### request arguments

DATE_START: query start date YYYY-DD-MM

DATE_END: query end date YYYY-DD-MM

### response

