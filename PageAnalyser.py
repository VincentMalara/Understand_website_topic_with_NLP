from HTML_parsing import Page
from Summarize import Text
import sys
from CodeNaf_Word2vec import word2vec_NAF


#Not used, can be used to take other internal link into account to understand website main topic
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



url_list=sys.argv[1:] #url to analyse list created from command

if not url_list:
    print("please input an url")
else:
    for url in url_list:
        print(url)
        page = Page() #page instanciation
        page.process(url) #html content extraction
        text = Text() #Text instanciation
        text.inputtext(page.textlist, url) #page content is input
        ##text.plot_cloud()  #plot cloud to have a visual object to understant website topic, not used
        text.get_summary() #create a summary of home page

        W2V=word2vec_NAF()
        W2V.clean_Naf()
        W2V.loadmodel()

        print('-' * 10)
        print('summary: ')
        print(text.summary)
        print('-' * 10)
        print('Topics: ')
        text.get_N_topic() #extract topics of text via word vectors
        print(text.topics)
        W2V.find_naf(text.topics)
        print('Most probable NAF is:')
        print(W2V.best_NAF)
        print(W2V.best_NAF_fr)
        print(W2V.best_NAF_code)