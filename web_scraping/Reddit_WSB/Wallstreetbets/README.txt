

#########################################
## NLP Project -Reddit Wallstreetbets Data Extraction ##
#########################################

Updata on 03/05/2021

File: wsb_tickers.py: web scraping data of most mentioned tickers in subreddit wallstreetbets

Folder:

1) WSB_data_scraping:

WSB_scrape.py: algorithms to scrape data from subreddit wallstreetbets as JSON file

submissions_20210101ToCurrent.rar: compressed data file of JSON data of posts in WSB from 01/01/2021 to 02/14/2021 (roughly)

sample_data.json: sample data for you to easily explore

2) WSB_construction_pickle:

WSB_construction.py: convert JSON file to pickle for later analysis

read pickle as a dataframe with columns: "created_utc", "num_comments", "selftext"

 reddit_df_pickle.pkl: pickle data for easily importing into python