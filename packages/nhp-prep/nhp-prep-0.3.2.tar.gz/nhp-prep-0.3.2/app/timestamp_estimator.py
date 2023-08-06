import pandas as pd
import datetime
from datetime import datetime as dt

from app.main_logger import logger

TRIAL_START_TIME_COL = "TrialStartTimestamp"
EXP_START_TIME_COL = "ExpStartTimestamp"
TIME_COL = "Time"

def change_timestamp(filename: str):
    """Function that creates an estimated time from the start time epoch
    timestamp and the Time column (which records the end time in ms
    since the start time)
    It will add the value in the Time column to the value in the 
    ExpStartTimestamp column, and parse the format to be hh:mm:ss;ms
    Args:
        filename (str): The name of the file to be modified

    Returns:
        file_date: The modified file data
    """
    file_data = pd.read_csv(filename)
    #1. read from the time column and add that to the start time
    for index,trial in file_data.iterrows():
        if not pd.isnull(trial[TRIAL_START_TIME_COL]): #if the file already has "TrialStartTimestamp", no need to change it
            continue
        #2. read timestamp of the start of the exp from col (example: 11:47:57,444)
        if pd.isnull(trial[EXP_START_TIME_COL]): #if the file does not contain a start timestamp
            continue
        if pd.isnull(trial[TIME_COL]): #don't have info to check the time
            continue
        start_time = dt.strptime(trial[EXP_START_TIME_COL], "%X,%f")
        time_from_start = trial["Time"]
        estimate_time = start_time + datetime.timedelta(milliseconds=time_from_start)
        datestr = estimate_time.strftime("%X,%f")[:-3] #To trim the last three zeros
        file_data.at[index, TRIAL_START_TIME_COL] = datestr

    return file_data
