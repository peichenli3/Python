***********************************
****** Three main functionalities

1) Get corresponding State and County information by using BeautifulSoup (url_geo)

2) Get corresponding county-level employed person content (url_csv)

3) Combine the above data into a list of lists and write property into a single csv file


***********************************
****** Details

1) Define the general format of url_csv (below we only need to modify url_mid for each county) and url_geo

2) In order to igonore some non-existent url_mid, we get the content of NA csv. (e.g. we don't have county represented by url_mid "01002"). 
The idea is that when we scrape csv from non-existent url, they basically have the exactly same content.

3) A nested-loop: for each U.S. State, create a folder and then write the final csv of each county into that folder

4) Important variables in each sub-loop:

   state
   county
   url_content
   data_list (a list of lists where each list element is one row of our final csv file)
   filename


***********************************
****** Customized downloading

1) Default: according to FRED employed person data, we have state rangin from 1 to 56
so m_default = 1 and n_default = 56
Also we may find that county ranges from 1 to 321
so p_default = 1 and q_default = 321

2) Adjustment: if our downloanding somehow stops at some point due to unexpected error,
we can just modify the values of m, n, p and q to customize our downloading process.

