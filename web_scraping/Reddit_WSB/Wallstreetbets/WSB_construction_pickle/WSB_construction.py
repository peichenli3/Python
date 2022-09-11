import pandas as pd
import json

def parse_reddit_json():

    # Opening JSON file
    json_List = []
    f = open("submissions_20210101ToCurrent.json")
    lines = f.readlines()
    f.close()
    for line in lines:
        try:
            json_List.append(json.loads(line))
        except ValueError:
            print(line)
            continue

    # Save to a dictionary
    Final_result = {"created_utc": [], "num_comments": [], "selftext": []}

    for json_single in json_List:
        Final_result["created_utc"].append(json_single.get("created_utc"))
        Final_result["num_comments"].append(json_single.get("num_comments"))
        Final_result["selftext"].append(json_single.get("title") + json_single.get("selftext","None").replace('\n', ' ').replace('\r', ''))

    # Save to pickle
    df = pd.DataFrame(Final_result)
    df.to_pickle('reddit_df_pickle.pkl')
    return 1


if __name__ == '__main__':
    parse_reddit_json()
