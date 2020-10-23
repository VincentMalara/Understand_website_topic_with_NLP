from HTML_parsing import Page
import sys
import nltk
import re
import heapq
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


nltk.data.path.append("/nltk_data")

def Analyse_Page(url):
    page = Page()
    page.seturl(url)
    page.extract_html_page()
    page.getLinks()


def manage_last_point(x):
    x=x.strip().lower()
    if x[-1]=='.':
        x=x[0:-1]
    else:
        x=x
    return x


def consider_internal_links(page):
    for i in page.links:
        if i[0] == '/':
            k= url + i
        else:
            k = i
        try:
            pagenew = Page()
            pagenew.seturl(k)
            pagenew.extract_html_page()
            pagenew.getAllText()
            print(k)
            for j in pagenew.H2s:
                print(j)
        except:
            print('error with:' + str(k))
    pass


url_list=sys.argv[1:]

if not url_list:
    print("please input an url")
else:
    for url in url_list:
        print(url)
        Analyse_Page(url)