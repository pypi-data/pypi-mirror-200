import pandas as pd
import time
import datetime

from app.main_logger import logger

REF_START_COL = "Start"
REF_END_COL = "End"
REF_DATE_COL = "Date"
REF_SUB_COL = "Sub"

TRIAL_START_COL = "TrialStartTimestamp"
SUB_COL = "Sub"
SUB_TEST = "TEST"
SUB_AMBIGUOUS = "AMBIGUOUS"

HHMMSS_FORMAT = '%H:%M:%S'
STD_DATE_FORMAT = '%m/%d/%Y'
SHORT_DATE_FORMAT = '%m/%d/%y'
HOUR_ENDING = "h"
HYPHEN_CHAR = "-"
SEPARATOR_TAG = "_"
BACKSLASH = "/"
COLON = ":"
DOUBLE_ZERO = "00"

def str_date_validate(date_str: str) -> str:
    """
    Function that validates that the date string is in the correct format.
    If not, then it converts it into DD/MM/YYYY

    Args:
        date_str (str): The string date to validate

    Returns:
        str: The date string in the correct format.
    """
    res = True
    try:
        res = bool(datetime.datetime.strptime(date_str, STD_DATE_FORMAT))
    except ValueError:
        res = False

    if not res:
        try:
            parsed_time = datetime.datetime.strptime(
                date_str, SHORT_DATE_FORMAT)
            return parsed_time.strftime(STD_DATE_FORMAT)
        except ValueError:
            logger.debug('Error while parsing the date: ' + date_str)
    logger.debug('Date already in the correct format: ' + date_str)
    return date_str


def change_sub(file_path: str, filename: str, ref_filename: str):
    """Function that changes the subject name to the subject name
    specified in the reference file within the specified time range
    If the name is not specified, put "UNDEFINED" as the subject name.
    Args:
        file_path (str): the full path to the file to be changed
        filename (str): the name of the file to be changed
        ref_filename (str): the name of the reference file

    Returns:
        file_data: the modified content of the file
    """
    ref_data = pd.read_csv(ref_filename)
    file_data = pd.read_csv(file_path)

    # 1. parse the file name for the month, day and year, and change it to this format mm/dd/yyyy
    full_time_str = filename.split(HOUR_ENDING)[0]
    date_str = full_time_str.split(SEPARATOR_TAG)[0]
    dates_array = date_str.split(HYPHEN_CHAR)
    year = int(dates_array[0])
    month = int(dates_array[1])
    day = int(dates_array[2])
    new_date_format = str(month) + BACKSLASH + \
        str(day) + BACKSLASH + str(year)
    # 2. parse the file start time in this format: hh:mm:00
    hour_str = full_time_str.split(SEPARATOR_TAG)[1]
    hours = hour_str[:-2]
    minutes = hour_str[2:]
    new_hours_format = hours + COLON + minutes + COLON + DOUBLE_ZERO
    file_start_time = time.strptime(new_hours_format, HHMMSS_FORMAT)
    # 3. search for the first row that contains the matching date and time in the baboons file
    for index_ref, trial_ref in ref_data.iterrows():
        # find the corresponding date
        if new_date_format != str_date_validate(trial_ref[REF_DATE_COL]):
            continue
        # 3_1 parse the start time to a date
        subject_start_time = time.strptime(
            trial_ref[REF_START_COL], HHMMSS_FORMAT)
        # 3_2 parse the end time to a date
        subject_end_time = time.strptime(
            trial_ref[REF_END_COL], HHMMSS_FORMAT)
        if subject_end_time < file_start_time:  # means the file does not include the subject
            continue
        sub = trial_ref[REF_SUB_COL]
        # 4. loop through the data file
        for index, trial in file_data.iterrows():
            # skip the lines that don't have a start time
            if pd.isnull(trial[TRIAL_START_COL]):
                continue
            # 4_1 parse TrailStartTimestamp to a date
            start_time = time.strptime(
                trial[TRIAL_START_COL], '%H:%M:%S,%f')
            # 4_2 test if the trial start time stamp is greater than the start time and less than the end time
            if start_time >= subject_start_time and start_time < subject_end_time:
                # 4_3 if yes, then change the subject to the corresponding subject in the baboons file
                file_data.at[index, SUB_COL] = sub

    # 5 change the subjects without a name to "AMBIGUOUS"
    for index, trial in file_data.iterrows():
        if trial[SUB_COL] == SUB_TEST:
            file_data.at[index, SUB_COL] = SUB_AMBIGUOUS
    return file_data
