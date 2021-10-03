#!/usr/bin/env python3

"""
Written by: Peichen Li
Last Updated: 08/14/2021

This python script is for cleaning SOI income data, SPECIFICALLY for year 2004
"""


import pandas as pd
from os import listdir
from os.path import isfile, join
import re
import glob
import numpy as np

# variables of interest
#cols = ["N1", "A00100", "N02650", "A02650", "A00200", "N00300", "A00300", "N00600", "A00600", "N00650"]

# set path
input = "C:/Users/90596/Desktop/PeterHan/SOI_data/SOI_wide/input/2004zipcode/"
output = "C:/Users/90596/Desktop/PeterHan/SOI_data/SOI_wide/output/"


def clean_2004_STATE(filename):
    """
    This function is for cleaning 2004 SOI data for each state
    """

    # Read excel data from line 13 
    df = pd.read_excel(input+filename, 
                        skiprows=11,
                        names=["AGI_Size", "NR", "NE_Total", "NE_DE", "AGI", 
                        "SW_NR", "SW_Amount", "TI_NR", "TI_Amount", "TD_NR", 
                        "TD_Amount", "NCG_NR", "NCG_Amount", "ScheduleCNP_NR", "ScheduleCNP_Amount", 
                        "ScheduleFNP_NR", "ScheduleFNP_Amount", "IRA_PD_NR", "IRA_PD_Amount", "SPD_NR", "SPD_Amount",
                        "TID_NR", "TID_AGI", "TID_Amount", "CD_NR", "CD_AGI", "CD_Amount", "TPD_NR", "TPD_AGI", "TPD_Amount",
                        "AMT_NR", "AMT_Amount", "ITBC_NR", "ITBC_Amount", "TT_NR", "TT_Amount", "EIC_NR", "EIC_Aount", "PP_NR"])
    #test
    #df.iloc[:10, :3]
    #df.head(2).iloc[1]['AGI_Size']

    # Convert 'AGI_Size' to string
    df['AGI_Size'] = df['AGI_Size'].astype(str)

    # Remove white space from column 'AGI_Size'
    df['AGI_Size'] = df['AGI_Size'].str.strip()

    # Create 'numeric' = True if 'AGI_Size' is only of digits
    df['numeric'] = df.AGI_Size.str.isdigit()

    # Find the index of first occurrence of zipcode
    # Subset the data frame from that index, so it won't have summary statistics from the first few rows
    # And then drop column 'numeric'
    Index = df[df.numeric == True].first_valid_index()
    df = df.iloc[int(Index):, ]
    del df['numeric']

    # Remove NaN rows
    df = df[df['NR'].notna()]

    # Remove special character '.' from the ENTIRE dataframe
    # \ before '*' is used for 'escape' in regular expressions
    df = df.replace('\*','', regex=True)
    df = df.replace('\--','', regex=True)

    # Remove empty rows
    df = df.drop(df[df['AGI_Size'] == ''].index)

    # Reset index
    df = df.reset_index(drop=True)

    # Add AGI_CLASS
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
        if row['AGI_Size'] ==  '$50,000 under $75,000':
            return 4
        if row['AGI_Size'] ==  '$75,000 under 100,000' or row['AGI_Size'] ==  '$75,000 under $100,000' or row['AGI_Size'] == '$75,000 under $100,00':
            return 5
        if row['AGI_Size'] ==  '$100,000 or more':
            return 6


    # Apply function AGI_CLASS
    df['AGI_CLASS'] = df.apply (lambda row: AGI_CLASS(row), axis=1)
    # Convert AGI_CLASS to type int and fill others(STATE and Zipcodes) with 0
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
    AGI_5 = [x+5 for x in AGI_0]
    AGI_6 = [x+6 for x in AGI_0]


    for i, j in zip(AGI_0, AGI_1):
        df.loc[j, 'AGI_Size'] = df.loc[i, 'AGI_Size']

    for i, j in zip(AGI_0, AGI_2):
        df.loc[j, 'AGI_Size'] = df.loc[i, 'AGI_Size']

    for i, j in zip(AGI_0, AGI_3):
        df.loc[j, 'AGI_Size'] = df.loc[i, 'AGI_Size']

    for i, j in zip(AGI_0, AGI_4):
        df.loc[j, 'AGI_Size'] = df.loc[i, 'AGI_Size']
    
    for i, j in zip(AGI_0, AGI_5):
        df.loc[j, 'AGI_Size'] = df.loc[i, 'AGI_Size']

    for i, j in zip(AGI_0, AGI_6):
        df.loc[j, 'AGI_Size'] = df.loc[i, 'AGI_Size']

    # Rename column 'AGI_Size' to 'ZIPCODE'
    df.rename(columns={'AGI_Size':'ZIPCODE'}, inplace=True)
    # convert column "a" to int64 dtype and "b" to complex type
    df = df.astype({"ZIPCODE": int})

    # Write to long format
    df.to_csv(input + filename[:16] + '.csv', index=False)
    print(input + filename[:16] + '.csv', " done")
    
    return 1



def append_all():

    path = input  # use your path
    all_files = glob.glob(path + "*.csv")

    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.to_csv(output + "SOI04_long.csv", index=False)
    print(output + "SOI04_long.csv done")

    return 1



if __name__ == "__main__":
    
    # filenames end with '.xls'
    onlyfiles = [f for f in listdir(input) if isfile(join(input, f))]
    filenames = [i for i in onlyfiles if i.endswith(".xls")]

    for filename in filenames:
        print(filename)
        clean_2004_STATE(filename)

    append_all()
