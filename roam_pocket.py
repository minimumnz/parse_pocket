from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import time
import re
import json
import spacy
from newspaper import Article
from collections import Counter
from transformers import pipeline
import torch
import argparse
from pprint import pprint

summarizer = pipeline("summarization")
nlp = spacy.load("en_core_web_sm")


def roam_format(article_dict):
    article_title = article_dict['title']
    url = article_dict['url']
    try:
        date = article_dict['date'].strftime('%a %d %b %Y')
    except Exception as e:
        print(e)
        date = ''
    authors = " ".join([f"[[{k}]]" for k in article_dict['authors']])
    entities = " ".join([f"[[{k}]]" for k in article_dict['entities']])
    keywords = " ".join([f"[[{k}]]" for k in article_dict['long_keywords'][:10]])
    summary = article_dict['summary'].replace('"', '')
    if authors:
        authors_string = f'{{ "string": "**Author**: {authors}"}},\n'
    else:
        authors_string = ''
    if date:
        date_string = f'{{ "string": "**Date**: {date}"}},\n'
    else:
        date_string = ''
    if entities:
        entity_string = f'{{ "string": "**Entities**: {entities}" }},\n'
    else:
        entity_string = ''
    return (f'[{{"title": "{article_title}","children": [\n'
            f'{{ "string": "**URL**: {url}"}},\n'
            f'{date_string}'
            f'{authors_string}'
            f'{entity_string}'
            f'{{ "string": "**Keywords**: {keywords}" }},\n'
            f'{{ "string": "**Summary**:  {summary}."}}\n'
            f']}}]')


def write_roam_json(i, roam_json):
    with open(f"data/{i}.json", "w") as text_file:
        text_file.write(roam_json)


def parse_keywords(nlp, text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'WORK_OF_ART', 'PRODUCT', 'ORG', 'EVENT']:
            print(ent.text, ent.label)
            entities.append((ent.text, ent.label_))
    common_keys = Counter(entities).most_common()
    common_keys_list = [k[0][0] for k in common_keys[0:10]]
    return common_keys_list

def parse_content(url, article_dict):
    article = Article(url)
    try:
        article.download()
        article.parse()
        article.nlp()
    except Exception as e:
        print(e)
        return

    article_dict['title'] = article.title
    article_dict['authors'] = article.authors
    article_dict['url'] = article.url
    article_dict['date'] = article.publish_date
    article_content = article.title + " " + article.text
    article_dict['keywords'] = article.keywords
    article_dict['summary'] = summarizer(article_content)[0]['summary_text']
    common_keys = parse_keywords(nlp, article_content)
    article_dict['long_keywords'] = common_keys
    return common_keys, article_dict

def fetch_tweet_id(url):
    if  ("twitter" in url) & ("photo" in url):
        return url.split("/")[-3]
    if ("twitter" in url):
        return url.split("/")[-1]


def fetch_links(url_list):
    keywords = []
    links = []
    for i, url in enumerate(url_list):
        article_dict = {}
        print(url)
        try:
            keys, article_dict = parse_content(url, article_dict)
            article_dict['entities'] = keys
            long_keywords = [k[0] for k in Counter(article_dict['long_keywords']).most_common(10)]
            article_dict['long_keywords'] = long_keywords
        except Exception as e:
            print(e)
        try:
            pprint((article_dict))
            roam_json = roam_format(article_dict)
            print(roam_json)
            write_roam_json(i, roam_json)
        except Exception as e:
            print(f"Exception here: {e}")
    keywords = [k for k in keywords if k]
    keywords = sum(keywords, [])



def fetch_shortened_links(link):
    link_id = link.split("/")[-1]
    if conn.get(link_id):
        print(f"Already fetched this link id. {link}")
        return
    print(link_id)
    time.sleep(2)
    try:
        s = requests.get(link)
        if s.url:
            print(s.url)
            conn.set(link_id, s.url)
        else:
            print("no url")
    except Exception as e:
        print(f"{e}")

def fetch_url_list():
    """
    Return a list of all webpages saved to pocket.
    """
    url_list = []
    soup = BeautifulSoup(open("pocket_data/ril_export.html"), "html.parser")
    for link in soup.findAll("a")[10:2500]:
        url = link.get("href")
        url_list.append(url)
    return url_list



url_list = fetch_url_list()
fetch_links(url_list)