## Reddit r/wallstreetbets Webscraping

If you want to know about short selling, short sqeeze, GameStop and subreddit WallStreetBets, You probably want to read [this WSJ article](https://www.gq.com.au/success/finance/your-guide-to-gamestop-rwallstreetbets-and-the-short-squeeze-that-has-wall-st-in-chaos/news-story/46e90e8b16744794bfaadd5089afcc15).
Personally I find it quite enjoyable. Now back to our story. Technology breakthrough in the recent years is quite fascinating. It enpowers researchers in finance/econ great tools to analyze unstructured data.
Tools in natural language process area has made it rewarding for finance researchers to analysze its hidden information. You may wonder why text data can be of our interest? Well, right after [the speech](https://www.wsj.com/articles/feds-powell-to-take-questions-on-job-market-interest-rates-bond-yields-11614872817) given by Fed Chairman Jerome Powell on 03/04/2021, you can notice the big move of market.
What if we can analyze his speech text and do a series of analysis? That could be interesting! And this kind of textual analysis is not uncommon in finance currently. See related [paper1](https://github.com/MS20190155/Measuring-Corporate-Culture-Using-Machine-Learning),
[paper2](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3286887). Also check [Prof. Manela's webpage](http://apps.olin.wustl.edu/faculty/manela/), as I find he's also working on projects related with NLP/text, ML and fintech.
For paper 1 in particular, it mainly uses Stanford NLP package [Stanza](https://stanfordnlp.github.io/stanza/index.html). I believe up to now it has been merged into [spaCy](https://spacy.io/universe/project/spacy-stanza) for easier use.
Now suppose you have the ideal statistical tools for textual analysis. What text data can be used? Paper 1 uses firm earning call transcripts while paper 2 utilizes patent documents.

## Description

Ok, now what if you want to use text data from subreddit wallstreetbets to better analyze the short squeeze frenzy event in early 2021? This github repo is the destination for you.
In short, I used the [Pushshift API](https://pushshift.io/) to extract the raw reddit data. You can see its Github repo [here](https://github.com/pushshift/api).
Why use Pushshift API? Well, there are also some other alternatives like ([PRAW](https://praw.readthedocs.io/en/latest/) in Python, and a wonderful package called [RedditExtractoR](https://cran.r-project.org/web/packages/RedditExtractoR/RedditExtractoR.pdf))
But unfortunately due to the limit of [Reddit API](https://www.reddit.com/dev/api/), you can only extract 1000 posts once. It may be impossible to extract all posts from WallStreetBets in a given period.

This project can serve as a data pipeline for textual analysis of reddit data. In particular, I'm going to use PushShift API to extract all raw data from subreddit Wallstreetbets, do some data cleaning and extract useful information.
In the end, I would convert the data into pickle format to make your NLP analysis easier. Pickle can be read into Python in few seconds.

## Getting Started

### Dependencies

* [Google Colab](https://colab.research.google.com/). (I run my webscraping scripts on this platform.)


### Executing program

* First, run the script **WSB_scrape.py** on your notebook of Google colab. This might take some time (1 month data ~ 40min). You can modify the parameters *max_created_utc*, *type* and *subreddit*. Parameter *max_created_utc* is for time-frame and *type* can be submissions (posts) or commments. This script is mostly recplicated from [this blog](https://www.osrsbox.com/blog/2019/03/18/watercooler-scraping-an-entire-subreddit-2007scape/).
```
max_created_utc = 1606802400  # 12/01/2020 @ 12:00am (UTC)

extract_reddit_data(subreddit="wallstreetbets", type="submission")
```
* Second, clean the data. Now after running the scraping script, the size of your JSON data can be up to ~2GB. We are interested in values with keys of: *created_utc*, *num_comments*, *title* and *selftext*. You may explore parameters of Pushshift API [here](https://pushshift.io/). Run script **WSB_construction.py** and you will get your pickle data called *reddit_df_pickle.pkl*. Notice that I merge column *title* into column *selftext*.

* Now you can start your NLP project. Happy scraping!
```
    # Save to pickle
    df = pd.DataFrame(Final_result)
    df.to_pickle('reddit_df_pickle.pkl')
```  
## Authors

Contributors names and contact info

Peichen Li

peichen3@illinois.edu


<!---
## Help

Any advise for common problems or issues. To be continued....
```
command to run if program contains helper info
```

## Authors

Peichen Li  

peichen3@illinois.edu

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [Peichen Li] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.

-->
