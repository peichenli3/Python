#!/usr/bin/env python3

"""
Written by: Peichen Li
Last Updated: 06/18/2021

This python script is for cleaning SOI income data, converting long to wide, appending all files into one single csv,
and creating a Choropleth Map 0f 2018 SOI income data
"""

import pandas as pd
import glob

# variables of interest
cols = ["N1", "A00100", "N02650", "A02650", "A00200", "N00300", "A00300", "N00600", "A00600", "N00650"]

# set path
input = "C:/Users/90596/Desktop/PeterHan/SOI_data/SOI_wide/input"
output = "C:/Users/90596/Desktop/PeterHan/SOI_data/SOI_wide/output"


# 2005 SOI
def SOI_05():
    df = pd.read_csv(input+"/05raw.csv", keep_default_na=False)
    # replace empty/NAs with zero
    df.replace('\.', 0, regex=True, inplace=True)
    df.replace("", 0, regex=True, inplace=True)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns of variable cols, add columns and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # select columns
    df = df[["STATE", "ZIPCODE", "AGI_CLASS", "N1", "A00100", "N02650", "A02650", \
             "A00200", "N00300", "A00300", "N00600", "A00600", "N00650"]]
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_CLASS', values=cols).reset_index()
    # combine first two header rows into one header row
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2005
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    # save file
    df_wide.to_csv(output + "/SOI05.csv", index=False)
    print("output:", output, "/SOI05.csv - done")


    # 2006 SOI
def SOI_06():
    df = pd.read_csv(input+"/06raw.csv", keep_default_na=False)
    # replace dot with zero
    df.replace('\.', 0, regex=True, inplace=True)
    df.replace("", 0, regex=True, inplace=True)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns, add and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # select columns
    df = df[["STATE", "ZIPCODE", "AGI_CLASS", "N1", "A00100", \
             "N02650", "A02650", "A00200", "N00300", "A00300", "N00600", "A00600", "N00650"]]
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # remove rows of WY (thousands of agi class, only for 2006)
    df = df[df["STATE"] != "wy"]
    # based on documentation, combine agi class 1 & 2 to 1, and map c(3,4,5,6,7) to c(2,3,4,5,6)
    df['AGI_CLASS'] = df['AGI_CLASS'].map({1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6})
    # save zipcode to state match-up
    df1 = df[['STATE', 'ZIPCODE']]
    df1 = df1.drop_duplicates(subset=['STATE', 'ZIPCODE'], keep='first')
    # delete state column temporarily
    del df['STATE']
    # for each zipcode, sum agi == 1
    df = df.groupby(["ZIPCODE", "AGI_CLASS"], as_index=False)[cols].agg('sum')
    # merge with state column by ZIPCODE
    df = pd.merge(df, df1, on='ZIPCODE', how='outer')
    # arrange columns in order
    df = df[["STATE", "ZIPCODE", "AGI_CLASS", "N1", "A00100", "N02650",\
             "A02650", "A00200", "N00300", "A00300", "N00600","A00600", "N00650"]]
    # State column to upper case
    df['STATE'] = df['STATE'].str.upper()
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_CLASS', values=cols).reset_index()
    # combine first two rows into one header
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2006
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of all N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # Calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    # save file
    df_wide.to_csv(output + "/SOI06.csv", index=False)
    print("output:", output, "/SOI06.csv - done")


# 2007 SOI
def SOI_07():
    df = pd.read_csv(input+"/07raw.csv", keep_default_na=False)
    # replace dot with zero
    df.replace('\.', 0, regex=True, inplace=True)
    df.replace("", 0, regex=True, inplace=True)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns, add and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # select columns
    df = df[["STATE", "ZIPCODE", "AGI_CLASS", "N1", "A00100", "N02650", \
             "A02650", "A00200", "N00300", "A00300", "N00600", "A00600", "N00650"]]
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # based on documentation, combine agi class 1 & 2 to 1, and map c(3,4,5,6,7) to c(2,3,4,5,6)
    df['AGI_CLASS'] = df['AGI_CLASS'].map({1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6})
    # save zipcode to state match-up
    df1 = df[['STATE', 'ZIPCODE']]
    df1 = df1.drop_duplicates(subset=['STATE', 'ZIPCODE'], keep='first')
    # delete state column temporarily
    del df['STATE']
    # for each zipcode, sum agi == 1
    df = df.groupby(["ZIPCODE", "AGI_CLASS"], as_index=False)[cols].agg('sum')
    # merge with state column by ZIPCODE
    df = pd.merge(df, df1, on='ZIPCODE', how='outer')
    # arrange columns
    df = df[["STATE", "ZIPCODE", "AGI_CLASS", "N1", "A00100", "N02650",\
             "A02650", "A00200", "N00300", "A00300", "N00600","A00600", "N00650"]]
    # State column to upper case
    df['STATE'] = df['STATE'].str.upper()
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_CLASS', values=cols).reset_index()
    # combine first two rows into one header
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2007
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of all N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # Calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    # save file
    df_wide.to_csv(output + "/SOI07.csv", index=False)
    print("output:", output, "/SOI07.csv - done")


# 2008 SOI
def SOI_08():
    df = pd.read_csv(input+"/08raw.csv", keep_default_na=False)
    # replace dot with zero
    df.replace('\.', 0, regex=True, inplace=True)
    df.replace("", 0, regex=True, inplace=True)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns, add and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # select columns
    df = df[["STATE", "ZIPCODE", "AGI_CLASS", "N1", "A00100", "N02650", "A02650", \
             "A00200", "N00300", "A00300", "N00600", "A00600", "N00650"]]
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # based on documentation, combine agi class 1 & 2 to 1, and map c(3,4,5,6,7) to c(2,3,4,5,6)
    df['AGI_CLASS'] = df['AGI_CLASS'].map({1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6})
    # save zipcode to state match-up
    df1 = df[['STATE', 'ZIPCODE']]
    df1 = df1.drop_duplicates(subset=['STATE', 'ZIPCODE'], keep='first')
    # delete state column temporarily
    del df['STATE']
    # for each zipcode, sum agi == 1
    df = df.groupby(["ZIPCODE", "AGI_CLASS"], as_index=False)[cols].agg('sum')
    # merge with state column by ZIPCODE
    df = pd.merge(df, df1, on='ZIPCODE', how='outer')
    # arrange columns
    df = df[["STATE", "ZIPCODE", "AGI_CLASS", "N1", "A00100", "N02650",\
             "A02650", "A00200", "N00300", "A00300", "N00600","A00600", "N00650"]]
    # State column to upper case
    df['STATE'] = df['STATE'].str.upper()
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_CLASS', values=cols).reset_index()
    # combine first two rows into one header
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2008
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of all N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # Calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    # save file
    df_wide.to_csv(output + "/SOI08.csv", index=False)
    print("output:", output, "/SOI08.csv - done")


# 2009 SOI
def SOI_09():
    df = pd.read_csv(input+"/09raw.csv", keep_default_na=False)
    # replace dot with zero
    df.replace('\.', 0, regex=True, inplace=True)
    df.replace("", 0, regex=True, inplace=True)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns, add and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    df = df[["STATE", "ZIPCODE", "AGI_STUB", "N1", "A00100", "N02650", "A02650", "A00200", \
             "N00300", "A00300", "N00600", "A00600", "N00650"]]
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_STUB', values=cols).reset_index()
    # combine first two rows into one header
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2009
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of all N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # Calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    # save file
    df_wide.to_csv(output + "/SOI09.csv", index=False)
    print("output:", output, "/SOI09.csv - done")



# 2010 SOI
def SOI_10():
    df = pd.read_csv(input+"/10raw.csv", keep_default_na=False)
    # replace dot with zero
    df.replace('\.', 0, regex=True, inplace=True)
    df.replace("", 0, regex=True, inplace=True)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns, add and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    df = df[["STATE", "ZIPCODE", "AGI_STUB", "N1", "A00100", "N02650", "A02650", "A00200", \
             "N00300", "A00300", "N00600", "A00600", "N00650"]]
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_STUB', values=cols).reset_index()
    # combine first two rows into one header
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2010
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of all N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # Calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    # save file
    df_wide.to_csv(output + "/SOI10.csv", index=False)
    print("output:", output, "/SOI10.csv - done")


# 2011 SOI
def SOI_11():
    df = pd.read_csv(input+"/11raw.csv", keep_default_na=False)
    # replace dot with zero
    df.replace('\.', 0, regex=True, inplace=True)
    df.replace("", 0, regex=True, inplace=True)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns, add and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    df = df[["STATE", "ZIPCODE", "AGI_STUB", "N1", "A00100", "N02650", "A02650", "A00200", \
             "N00300", "A00300", "N00600", "A00600", "N00650"]]
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_STUB', values=cols).reset_index()
    # combine first two rows into one header
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2011
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of all N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # Calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    # save file
    df_wide.to_csv(output + "/SOI11.csv", index=False)
    print("output:", output, "/SOI11.csv - done")



# 2012 SOI
def SOI_12():
    df = pd.read_csv(input+"/12raw.csv", keep_default_na=False)
    # replace dot with zero
    df.replace('\.', 0, regex=True, inplace=True)
    df.replace("", 0, regex=True, inplace=True)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns, add and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    df = df[["STATE", "ZIPCODE", "AGI_STUB", "N1", "A00100", "N02650", "A02650", "A00200", \
             "N00300", "A00300", "N00600", "A00600", "N00650"]]
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_STUB', values=cols).reset_index()
    # combine first two rows into one header
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2012
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of all N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # Calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    # save file
    df_wide.to_csv(output + "/SOI12.csv", index=False)
    print("output:", output, "/SOI12.csv - done")



# 2013 SOI
def SOI_13():
    df = pd.read_csv(input+"/13raw.csv", keep_default_na=False)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns, add and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    df = df[["STATE", "ZIPCODE", "AGI_STUB", "N1", "A00100", "N02650", "A02650", \
             "A00200", "N00300", "A00300", "N00600", "A00600", "N00650"]]
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_STUB', values=cols).reset_index()
    # combine first two rows into one header
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2013
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of all N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # Calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    # save file
    df_wide.to_csv(output + "/SOI13.csv", index=False)
    print("output:", output, "/SOI13.csv - done")


# 2014 SOI
def SOI_14():
    df = pd.read_csv(input+"/14raw.csv", keep_default_na=False)
    # replace dot with zero
    df.replace('\.', 0, regex=True, inplace=True)
    df.replace("", 0, regex=True, inplace=True)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns, add and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    df = df[["STATE", "ZIPCODE", "AGI_STUB", "N1", "A00100", "N02650", "A02650", \
             "A00200", "N00300", "A00300", "N00600", "A00600", "N00650"]]
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_STUB', values=cols).reset_index()
    # combine first two rows into one header
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2014
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of all N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # Calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    # save file
    df_wide.to_csv(output + "/SOI14.csv", index=False)
    print("output:", output, "/SOI14.csv - done")


# 2015 SOI
def SOI_15():
    df = pd.read_csv(input+"/15raw.csv", keep_default_na=False)
    # replace dot with zero
    df.replace('\.', 0, regex=True, inplace=True)
    df.replace("", 0, regex=True, inplace=True)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns, add and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    df = df[["STATE", "ZIPCODE", "AGI_STUB", "N1", "A00100", "N02650", "A02650", "A00200", \
         "N00300", "A00300", "N00600", "A00600", "N00650"]]
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_STUB', values=cols).reset_index()
    # combine first two rows into one header
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2015
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of all N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # Calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    # save file
    df_wide.to_csv(output + "/SOI15.csv", index=False)
    print("output:" , output, "/SOI15.csv - done")



# 2016 SOI
def SOI_16():
    df = pd.read_csv(input+"/16raw.csv", keep_default_na=False)
    # replace dot with zero
    df.replace('\.', 0, regex=True, inplace=True)
    df.replace("", 0, regex=True, inplace=True)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns, add and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    df = df[["STATE", "ZIPCODE", "AGI_STUB", "N1", "A00100", "N02650", "A02650", "A00200", \
         "N00300", "A00300", "N00600", "A00600","N00650"]]
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_STUB', values=cols).reset_index()
    # combine first two rows into one header
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2016
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of all N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # Calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    # save file
    df_wide.to_csv(output + "/SOI16.csv", index=False)
    print("output:", output, "/SOI16.csv - done")



# 2017 SOI
def SOI_17():
    df = pd.read_csv(input+"/17raw.csv", keep_default_na=False)
    # replace dot with zero
    df.replace('\.', 0, regex=True, inplace=True)
    df.replace("", 0, regex=True, inplace=True)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns, add and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    df = df[["STATE", "ZIPCODE", "AGI_STUB", "N1", "A00100", "N02650", "A02650", "A00200", "N00300", \
         "A00300", "N00600", "A00600","N00650"]]
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_STUB', values=cols).reset_index()
    # combine first two rows into one header
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2017
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of all N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # Calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    # save file
    df_wide.to_csv(output + "/SOI17.csv", index=False)
    print("output:", output, "/SOI17.csv - done")


# 2018 SOI
def SOI_18():
    df = pd.read_csv(input+"/18raw.csv", keep_default_na=False)
    # replace dot with zero
    df.replace('\.', 0, regex=True, inplace=True)
    df.replace("", 0, regex=True, inplace=True)
    # columns name upper case
    df.columns = df.columns.str.upper()
    # if absent some columns, add and impute with zeros
    df = df.reindex(df.columns.union(cols, sort=False), axis=1, fill_value=0)
    # columns numeric type (necessary for pivot table)
    df[cols] = df[cols].apply(pd.to_numeric)
    df = df[["STATE", "ZIPCODE", "AGI_STUB", "N1", "A00100", "N02650", "A02650", "A00200", \
             "N00300", "A00300", "N00600", "A00600", "N00650"]]
    # remove zipcode == 0
    df = df[df['ZIPCODE'] != 0]
    # long to wide
    df_wide = df.pivot_table(index=["STATE", "ZIPCODE"], columns='AGI_STUB', values=cols).reset_index()
    # combine first two rows into one header
    df_wide.columns = [c[0] + "_" + str(c[1]) for c in df_wide.columns]
    df_wide.rename(columns={'STATE_': 'STATE', 'ZIPCODE_': 'ZIPCODE'}, inplace=True)
    # add year
    df_wide['Year'] = 2018
    # fill empty cells with zero
    df_wide.fillna(0, inplace=True)
    # sum of all A00100 categories
    col_list_A00100 = ['A00100_1', 'A00100_2', 'A00100_3', 'A00100_4', 'A00100_5', 'A00100_6']
    df_wide['A00100'] = df_wide[col_list_A00100].sum(axis=1)
    # sum of all N1 categories
    col_list_N1 = ['N1_1', 'N1_2', 'N1_3', 'N1_4', 'N1_5', 'N1_6']
    df_wide['N1'] = df_wide[col_list_N1].sum(axis=1)
    # Calculate A00100 per N1
    df_wide['A00100perN1'] = df_wide['A00100'] / df_wide['N1']
    df_new = df_wide
    df_new = df_new.sort_values('A00100perN1')
    rows = len(df_new.index)
    one_pct = int(0.01 * rows)
    df_new = df_new[one_pct:-one_pct]
    average_income = df_new['A00100perN1'].mean()
    print("Average adjusted gross income for 2018 is ",average_income)
    # save file
    df_wide.to_csv(output + "/SOI18.csv", index=False)
    print("output:", output, "/SOI18.csv - done")



def append_all():

    path = output  # use your path
    all_files = glob.glob(path + "/*.csv")

    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.to_csv(output + "/SOI05to18.csv", index=False)



if __name__ == "__main__":
    SOI_05()
    SOI_06()
    SOI_07()
    SOI_08()
    SOI_09()
    SOI_10()
    SOI_11()
    SOI_12()
    SOI_13()
    SOI_14()
    SOI_15()
    SOI_16()
    SOI_17()
    SOI_18()
    append_all()