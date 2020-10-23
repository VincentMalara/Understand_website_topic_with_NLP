from HTML_parsing import Page
from Summarize import Text
import sys
import nltk


def consider_internal_links(page):
    for i in page.links:
        if i[0] == '/':
            k= url + i
        else:
            k = i
        try:
            pagenew = Page()
            pagenew.process(k)
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
        page = Page()
        page.process(url)
        text=Text()
        text.inputtext(page.textlist, url)
        text.plot_cloud()
        print(page.summary())