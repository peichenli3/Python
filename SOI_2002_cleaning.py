#!/usr/bin/env python3

"""
Written by: Peichen Li
Last Updated: 08/13/2021

This python script is for cleaning SOI income data, SPECIFICALLY for year 2002
"""


from typing import Text
import pandas as pd
from os import listdir
from os.path import isfile, join
import re
import glob

# variables of interest
#cols = ["N1", "A00100", "N02650", "A02650", "A00200", "N00300", "A00300", "N00600", "A00600", "N00650"]

# set path
input = "C:/Users/90596/Desktop/PeterHan/SOI_data/SOI_wide/input/2002zipcode/"
output = "C:/Users/90596/Desktop/PeterHan/SOI_data/SOI_wide/output/"


def clean_2002_STATE(filename):
    """
    This function is for cleaning 2002 SOI data for each state
    """

    # Import data
    # Read excel data from line 9 
    df = pd.read_excel(input+filename, 
                        skiprows=7,
                        names=["AGI_Size", "NR", "NE_Total", "NE_DE", "AGI", 
                        "SW_NR", "SW_Amount", "TI_NR", "TI_Amount", "TT_NR", 
                        "TT_Amount", "Contributions_Number", "Contributions_Amount", 
                        "ScheduleC_NR", "ScheduleF_NR", "ScheduleA_NR"])
    
    # Deal with inconsistent format between spreadsheets
    if filename == "zptab02ca.xls":
        df.iloc[5022, 0] = 92504
    
    #Take a quick look at the data
    #df.iloc[:10, :3]
    #df.head(2).iloc[1]['AGI_Size']

    # Convert 'AGI_Size' to string type first
    df['AGI_Size'] = df['AGI_Size'].astype(str)
    # Remove white space from column 'AGI_Size'
    df['AGI_Size'] = df['AGI_Size'].str.strip()


    # Create 'numeric' = True if AGI_Size is only of digits
    df['numeric'] = df.AGI_Size.str.isdigit()

    # Find the index of first occurrence of zipcode
    # Subset the data frame from that index, so it won't have summary statistics from the first few rows
    # And then drop column 'numeric'
    Index = df[df.numeric == True].first_valid_index()
    df = df.iloc[int(Index):, ]
    del df['numeric']

    # Remove empty rows
    df = df.drop(df[df['AGI_Size'] == ''].index)

    # Reset index
    df = df.reset_index(drop=True)

    # Create AGI_CLASS
    # 1 for "Under $10,000"
    # 2 for "$10,000 under $25,000"
    # 3 for "$25,000 under $50,000"
    # 4 for "$50,000 or more"
    def AGI_CLASS (row):
        if row['AGI_Size'] ==  'Under $10,000':
            return 1
        if row['AGI_Size'] ==  '$10,000 under $25,000':
            return 2
        if row['AGI_Size'] ==  '$25,000 under $50,000':
            return 3
        if row['AGI_Size'] ==  '$50,000 or more':
            return 4

    # Apply the above function 'AGI_CLASS'
    df['AGI_CLASS'] = df.apply (lambda row: AGI_CLASS(row), axis=1)
    
    # Convert AGI_CLASS to type integer and fill others(STATE and Zipcodes) with 0
    # 0 for TOTAL for each ZIPCODE
    df["AGI_CLASS"] = df["AGI_CLASS"].fillna(0.0).astype(int)

    # Reorder columns
    cols = list(df)

    # Move the column to head of list using index, pop and insert
    cols.insert(1, cols.pop(cols.index('AGI_CLASS')))
    df = df[cols]

    # Label AGI_CLASS for each ZIPCODE
    AGI_0 = df.index[df['AGI_CLASS'] == 0].tolist()
    AGI_1 = [x+1 for x in AGI_0]
    AGI_2 = [x+2 for x in AGI_0]
    AGI_3 = [x+3 for x in AGI_0]
    AGI_4 = [x+4 for x in AGI_0]
    
    for i, j in zip(AGI_0, AGI_1):
        df.loc[j, 'AGI_Size'] = df.loc[i, 'AGI_Size']


    for i, j in zip(AGI_0, AGI_2):
        df.loc[j, 'AGI_Size'] = df.loc[i, 'AGI_Size']

    for i, j in zip(AGI_0, AGI_3):
        df.loc[j, 'AGI_Size'] = df.loc[i, 'AGI_Size']

    for i, j in zip(AGI_0, AGI_4):
        df.loc[j, 'AGI_Size'] = df.loc[i, 'AGI_Size']

    # Rename column 'AGI_Size' to 'ZIPCODE'
    df.rename(columns={'AGI_Size':'ZIPCODE'}, inplace=True)


    # Remove special character '*' and '--' from the ENTIRE dataframe
    # \ before '*' is used for 'escape' in regular expressions
    df = df.replace('\*','', regex=True)
    df = df.replace('\--','', regex=True)

    # Write to long format
    df.to_csv(input + filename[:9] + '.csv', index=False)
    print(input + filename[:9] + '.csv', " done")
    
    return 1



def append_all():

    path = input  # use your path
    all_files = glob.glob(path + "*.csv")

    li = []

    for filename in all_files:
        if "zptab02us" in filename:
            continue
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.to_csv(output + "SOI02_long.csv", index=False)
    print(output + "SOI02_long.csv done")

    return 1



if __name__ == "__main__":
    
    # filenames end with '.xls'
    onlyfiles = [f for f in listdir(input) if isfile(join(input, f))]
    filenames = [i for i in onlyfiles if i.endswith(".xls")]

    for filename in filenames:
        print(filename)
        if filename == "zptab02us.xls":
            continue
        clean_2002_STATE(filename)

    append_all()
