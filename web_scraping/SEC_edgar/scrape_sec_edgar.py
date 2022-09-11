#!/usr/bin/python3

"""
Written by: Peichen Li
Last Updated: 10/21/2021

Purpose: 
    Downloading all of these files. https://www.sec.gov/dera/data/edgar-log-file-data-set.html



Steps: 
    (1) Generate a list of dates with the format of YYYYMMDD in string
    (2) URL Manipulation
    (3) Downloading



"""




import urllib.request



import pandas as pd
from datetime import datetime




if __name__ == "__main__":

    import urllib.request
    import pandas as pd
    from datetime import datetime

    # Generate a list of dates with the format of YYYYMMDD in string
    dates = pd.date_range(start="2003-01-01",end="2017-06-30")
    dates = [date_obj.strftime('%Y%m%d') for date_obj in dates]


    # URL Manipulation and downloading
    for date in dates:
        Qtr = "Qtr" + str((int(date[4:6])-1)//3 + 1)
        Year = date[:4]
        filename = "log" + date + ".zip"
        url = "http://www.sec.gov/dera/data/Public-EDGAR-log-file-data/"+Year+"/"+Qtr+"/"+filename

        print(url, "downloading ...")
        urllib.request.urlretrieve(url, filename)
