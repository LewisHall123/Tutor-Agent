from datetime import datetime


def get_year() -> int:
    """
    Get the current year.
    
    Returns:
        int: The current year as an integer
    """
    now = datetime.now()
    year = int(now.strftime("%Y"))
    return year


def get_date() -> str: 
    """
    Get the date as dd-mm-yyyy.
    
    Returns:
        str: Todays date formatted as dd-mm-yyyy
    """
    now = datetime.now()
    year = str(now.strftime("%Y"))
    month = str(now.strftime("%m"))
    day = str(now.strftime("%d"))
    date = f"{day}-{month}-{year}"
    return date


def get_date_and_time() -> tuple[int, int, int, int, int, int, int]: 
    '''
    Get the current date and time details

     Returns:
        tuple[int, int, int, int, int, int, int]: 
        A tuple containing the current year, month, day, 
        number of days passed this year, hour, minute, and second.
    '''
    # Get the current date and time
    now = datetime.now()

    # Get each value for data and time and convert it to int
    year = int(now.strftime("%Y"))
    month = int(now.strftime("%m"))
    day = int(now.strftime("%d"))
    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))
    second = int(now.strftime("%S"))

    # List corresponding to the number of days in each month
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] 

    # Number of days that have passed this year 
    num_days = day + sum(days_in_months[:month-1])

    return year, month, day, num_days, hour, minute, second




