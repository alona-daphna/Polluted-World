import pandas as pd
import consts
import os
import ast

index = 0
#this function initializes the info in the file
def initialize_file():
    if os.stat(consts.FILE_NAME).st_size == 0:
        events = {
            consts.COL_INDEX: [],
            consts.COL_LOCATION: [],
            consts.COL_INFO: [],
            consts.COL_TIME: [],
            consts.COL_DATE: [],
            consts.COL_PARTICIPANTS: []
        }

        df = pd.DataFrame(events)
        df.to_csv(consts.FILE_NAME, mode='a', index = False ,header=True)


#event: {location: "...", info: "...", time: "...", date: "...", participants: "..."}
def add_event(event):
    global index
    df = pd.read_csv(consts.FILE_NAME)
    # gets the row for the specific num
    data_to_append = {consts.COL_INDEX: index,
        consts.COL_LOCATION: [event[consts.COL_LOCATION]],
        consts.COL_INFO: [event[consts.COL_INFO]],
        consts.COL_TIME: [event[consts.COL_TIME]],
        consts.COL_DATE: [event[consts.COL_DATE]],
        consts.COL_PARTICIPANTS: [event[consts.COL_PARTICIPANTS]]
    }
    df = pd.DataFrame(data_to_append)
    df.to_csv(consts.FILE_NAME, mode='a',index = False ,header=False)
    index += 1


def add_participants(event, participants):
    df = pd.read_csv(consts.FILE_NAME)
    index = get_index_by_info(event)
    for item in participants:
        event["participants"].append(item)
    df.loc[index, consts.COL_PARTICIPANTS] = str(event["participants"])
    df.to_csv(consts.FILE_NAME, mode='w', index=False, header=True)


def read_events(location = ""):
    is_location = True
    if len(location) == 0:
        is_location = False
    data = pd.read_csv(consts.FILE_NAME)
    wanted_events = get_records(data, location)
    details = dict()
    events = []
    for event in wanted_events:
        details = {}
        details[consts.COL_INDEX] = event[consts.COL_INDEX]
        details[consts.COL_LOCATION] = event[consts.COL_LOCATION]
        details[consts.COL_INFO] = event[consts.COL_INFO]
        details[consts.COL_TIME] = event[consts.COL_TIME]
        details[consts.COL_DATE] = event[consts.COL_DATE]
        details[consts.COL_PARTICIPANTS] = convert_to_list(event[consts.COL_PARTICIPANTS])
        events.append(details)
    return events


def get_index_by_info(event):
    index = -1
    found = True
    location = event[consts.COL_LOCATION]
    info = event[consts.COL_INFO]
    date = event[consts.COL_DATE]
    events = read_events()
    for item in events:
        if item[consts.COL_LOCATION] == location and item[consts.COL_INFO] == info and item[consts.COL_DATE] == date:
            index = item[consts.COL_INDEX]
    return index


def get_records(data, location = ""):
    dicts = data.to_dict('records')
    events = []
    if len(location) > 0:
        for item in dicts:
            if item[consts.COL_LOCATION] == location:
                events.append(item)
        return events
    else:
        return dicts

def convert_to_list(locations_str):
    return ast.literal_eval(locations_str)


