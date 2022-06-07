import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import plotly.express as px
from tqdm import tqdm
import time
import json
import re

start_time = time.time()

#Get the article links
result = requests.get("https://www.aljazeera.com/where/mozambique/")
soup = BeautifulSoup(result.content, "html.parser")
articles = soup.find_all("a", class_="u-clickable-card__link")
article_links = []

print("Collecting article links...")
for i in tqdm(range(10)):
    article_links.append(articles[i]["href"])


base_url = "https://www.aljazeera.com"

article_text = []
#Get the article content
print("Collecting article data...")
for i in tqdm(range(10)):
    content = requests.get(base_url+article_links[i])
    soup = BeautifulSoup(content.content, "html.parser")
    main_body = soup.find("div", class_= "wysiwyg")

    contents = main_body.find_all("p")
    text  = ""
    for content in contents:
        #Clean data remove newline, space, numbers and punctuations
        clean_text = content.text.replace("\n", " ").strip()
        clean_text= clean_text.replace("/", " ")
        clean_text = re.sub(r'\d+', '', clean_text)
        clean_text = re.sub(r'[^\w\s]', '', clean_text)
        text = text + clean_text
    #Store the cleaned data in a list
    article_text.append(text)

#Save data in JSON File
with open("data.json", "w") as f:
    json.dump({"article_text": article_text}, f) 

#Use pre-trained model for sentiment analysis
sentiment_pipeline  = pipeline("sentiment-analysis")
news_sentiments = sentiment_pipeline(article_text)

#Analyse results for generating graph 
positive_count, negative_count, neutral_count = 0, 0, 0
print("Analysing Sentiment...")
for sentiment in tqdm(news_sentiments):
    if sentiment['label'] == "POSITIVE":
        positive_count += 1
    
    elif sentiment['label'] == "NEGATIVE":
        negative_count +=1
    
    else:
        neutral_count +=1

print(news_sentiments)



names = ['Positive', 'Negative', 'Neutral']
fig = px.pie(values= [positive_count, negative_count, neutral_count],names = names, title = "Sentiment Distribution by %")
fig.show()

print("Time required to run the code: %s seconds" % (time.time() - start_time))

