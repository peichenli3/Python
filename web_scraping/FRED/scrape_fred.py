import os
import requests
import csv
import time
import bs4 as BeautifulSoup

url_csv_left = 'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=LAUCN'
url_mid = '01002'
url_csv_right = '0000000005&scale=left&cosd=1990-01-01&coed=2021-03-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2021-05-19&revision_date=2021-05-19&nd=1990-01-01'
url = url_csv_left + url_mid + url_csv_right
response_NA = requests.get(url)
url_content_NA = response_NA.content
url_geo_left = 'https://fred.stlouisfed.org/series/LAUCN'
url_geo_right = '0000000005'


# identify yourself in the header (optional; necessary if FRED refuses us to download frequently)
'''
headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'  # This is another valid field
}
'''

print("Start scraping...")

def get_csv(m = 1, n = 56, p = 1, q = 322):
    for i in range(m, n+1):
        os.makedirs(str(i).zfill(2))
        print("State folder", str(i), "created!")
        for j in range(p, q+1):
            url_mid = str(i).zfill(2) + str(j).zfill(3)
            url_csv = url_csv_left + url_mid + url_csv_right
            url_geo = url_geo_left + url_mid + url_geo_right
            # get employed persons data url_csv
            response = requests.get(url_csv)
            # add headers
            # response = requests.get(url, headers=headers)
            url_content = response.content
            if url_content == url_content_NA:
                continue
            # get state county data url_geo
            geo_text = requests.get(url_geo).text
            soup = BeautifulSoup.BeautifulSoup(geo_text, 'lxml')
            s = str(soup.title)
            start_county = s.find('in ') + 3
            end_county = s.find(', ', start_county)
            county = s[start_county:end_county]
            start_state = s.find(", ") + 2
            end_state = s.find(" (LAUCN", start_state)
            state = s[start_state:end_state]
            data_list = [i.split(',') for i in url_content.decode().split('\n')]
            for row in data_list:
                row.append(state)
                row.append(county)
            data_list[0][1] = 'employed person'
            data_list[0][2] = 'State'
            data_list[0][3] = 'County'
            data_list = data_list[:-1]
            filename = str(i).zfill(2) + '/' + url_mid + ".csv"
            with open(filename, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerows(data_list)
            time.sleep(3)



if __name__ == "__main__":
    get_csv(m = 34, p =1)
