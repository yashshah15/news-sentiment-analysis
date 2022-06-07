# Sentiment Analysis of News articles
## ISI MINDS GROUP SUMMER CHALLENGE

---------------------------

This repository contains the code for sentiment analysis of news articles published on from https://www.aljazeera.com/where/mozambique/. The code will automatically scrape the 10 most recen news articles published on the website. The data is stored in a python list and then sent to the pre-trained model for sentiment analysis. The model will classify the sentiment for article as positive, negative or neutral. The scraped data is stored in a json file [data.json](https://github.com/yashshah15/news-sentiment-analysis/blob/main/data.json)

### List of libraries required for the project

- re
- requests 
- BeautifulSoup
- transformers
- plotly
- tqdm
- time
- json

All the required libraries have been mentioned in [requirements.txt](https://github.com/yashshah15/news-sentiment-analysis/blob/main/requirements.txt)
## Code Walkthrough
---
### Scraping Data
For scraping data I have used requests module from python. For getting the data:
- I have scraped the links to news articles first and stored them in a python list.
- After that I visited each link to scrape the news article content.
- I have used BeautifulSoup to parse the html content using attributes and class names
### Getting links
```sh
result = requests.get("https://www.aljazeera.com/where/mozambique/")
soup = BeautifulSoup(result.content, "html.parser")
articles = soup.find_all("a", class_="u-clickable-card__link")
article_links = []

for i in range(10):
    article_links.append(articles[i]["href"])
```


### Scraping article content
```sh
base_url = "https://www.aljazeera.com"
article_text = []
for i in range(10):
    content = requests.get(base_url+article_links[i])
    soup = BeautifulSoup(content.content, "html.parser")
    main_body = soup.find("div", class_= "wysiwyg")

    contents = main_body.find_all("p")
    text  = ""
    for content in contents:
        clean_text = content.text.replace("\n", " ").strip()
        clean_text= clean_text.replace("/", " ")
        clean_text = re.sub(r'\d+', '', clean_text)
        clean_text = re.sub(r'[^\w\s]', '', clean_text)
        text = text + clean_text
    
    article_text.append(text)
```
### Cleaning Data
To have the model only proces clean data and save computation time, I have pre-processed the data while I append it to the article_text list. I have removed all the white spaces, numbers, newline characters and punctuations from the text. I have also converted the text to lower case
```sh
clean_text = content.text.replace("\n", " ").strip()
clean_text= clean_text.replace("/", " ")
clean_text = re.sub(r'\d+', '', clean_text)
clean_text = re.sub(r'[^\w\s]', '', clean_text)
```
### Performing Sentiment Analysis
I have used transformers library to perform sentiment analysis of the news article. More details have been described in the section below. 
```sh
sentiment_pipeline  = pipeline("sentiment-analysis")
news_sentiments = sentiment_pipeline(article_text)
positive_count, negative_count, neutral_count = 0, 0, 0
```
The sentiment analysis produce a result as follows:
```sh
[{'label': 'NEGATIVE', 'score': 0.9987661838531494}, {'label': 'NEGATIVE', 'score': 0.9926683306694031}, {'label': 'NEGATIVE', 'score': 0.9975306391716003}, {'label': 'NEGATIVE', 'score': 0.9968761205673218}, {'label': 'NEGATIVE', 'score': 0.9986145496368408}, {'label': 'POSITIVE', 'score': 0.5278521180152893}, {'label': 'NEGATIVE', 'score': 0.994573175907135}, {'label': 'NEGATIVE', 'score': 0.9974657297134399}, {'label': 'NEGATIVE', 'score': 0.9913474917411804}, {'label': 'NEGATIVE', 'score': 0.9979806542396545}]
```
The label key indicates the resultant sentiment from the model. It can have three values: Positive, Negativeor Neutral. The score field will indicate the factor by which the model feel a particular piece of text is positive, negative or neutral. 
### Steps to run the project
- Run: git clone https://github.com/yashshah15/news-sentiment-analysis.git
- cd news-sentiment-analysis.git
- Run: pip install -r requirements.txt to install the required packages and dependencies
- Execute the command: python sentiment-analysis.py
- The resultant chart will be displayed in the browser on the address http://127.0.0.1:53695/ 

### Output
The resultant graph is a pie chart demonstraing the distribution of positive, negative and neutral sentiments as percentages.
The Graph generated for the result will pop up and the browserr windown on the address: http://127.0.0.1:53580/
![Sentiment Distribution](graph.png?raw=true "Sentiment distribution by %")

### Interpretation of results
The overall sentiment of news articles is negative as clearly demonstrated by the graph. The articles date back to the commencement of the Russia - Ukraine war. Mostly contain negative information. 

## Reason for choosing the library
The transformers library is a library of https://huggingface.co/
[Hugging Face](https://huggingface.co/) is one of the largest collection of publicly available datasets and models. It consists of 215 publicly available models for sentiment analysis capable of performing analysis on a variety of languages. Interating with python is easy and just takes 4-5 lines of code
```sh
pip install -q transformers
from transformers import pipeline
sentiment_pipeline = pipeline("sentiment-analysis")
data = ["I love you", "I hate you"]
sentiment_pipeline(data)
```
We can choose a specific model that best aligns to our requirements. I chose the default model,  which is quite popular on the platform with over 12 million downloads each month. This makes it an ideal candidate for sentiment analysis. The model is also fast at producing the sentiment results

#### Time required to run the code
The entire code takes around 15 seconds to run completely. The sentment analysis is quick and smooth. The requests module also makes scraping easy and quick. The time to run is also output at the end.