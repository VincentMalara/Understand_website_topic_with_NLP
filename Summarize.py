from langdetect import detect
import nltk
import heapq
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora


#delete last point of each phrase when there is one.
def manage_last_point(x):
    x = x.strip().lower()
    if x[-1] == '.':
        x = x[0:-1]
    else:
        x = x
    return x

#all the cleaning operations done to each sentence
def clean(text, stop, url, lemma):
    exclude = set(string.punctuation)
    stop_free = ' '.join([i for i in text.lower().split() if i not in stop])
# remove word from url such as company name:
    url_free = ' '.join([i for i in stop_free.lower().split() if i not in url])
    punc_free = ''.join([ch for ch in url_free if ch not in exclude])
    normalized = ' '.join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


class Text():
    def __init__(self):
        self.lang = ''
        self.textlist = []
        self.text = ''
        self.sentence_list = []
        self.stopwords = []
        self.word_frequencies = {}
        self.summary=''
        self.textlist=[]
        self.textraw = ''
        self.text = ''
        self.url = ''
        self.textnoname = ''
        self.topics = []
        self.N = 3
        self.Nword = 4
        self.N_sente_summ = 4
        self.topics = []

    # input text and processing
    def inputtext(self,textlist, url):
        self.textlist=textlist
        self.url = url
        self.textraw = ('. ').join(manage_last_point(x) for x in self.textlist if x)
        text = re.sub('[^a-zA-Z]', ' ', self.textraw)
        self.text = re.sub(r'\s+', ' ', text)
        if self.lang == '':
            self.getlang()
        self.textformat = [clean(sente, self.stopwords, self.url, WordNetLemmatizer()).split()
                           for sente in self.text.split('. ')]


# set parameters for number of
    def set_N(self, N): #N topics, by default 3
        self.N = N

    def set_Nword(self, N): #N word per topics, by default 4
        self.Nword = N

    def set_N_sente_summ(self, N): #N sentence for the summary, by default 4
        self.N_sente_summ = N

    #get lang and select appropriate stop words list
    def getlang(self):
        #detect language
        self.lang = detect(self.text)
        #load stopwordlist depending on language
        #dict to be completed to be able to consider other languages
        dictlang = {
            'en': 'english',
            'fr': 'french'
        }
        self.stopwords = nltk.corpus.stopwords.words(dictlang.get(self.lang))


    # plot word cloud
    def plot_cloud(self):
        if self.lang == '':
            self.getlang()

        # Wordcloud creation (inspired by: https://www.geeksforgeeks.org/generating-word-cloud-python/)
        wordcloud = WordCloud(width=600, height=400,
                              background_color='white',
                              stopwords=self.stopwords,
                              min_font_size=10).generate(self.textformat)
        # WordCloud Plot
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()

    #summaryse all the content by selecting the most important sentence
    def get_summary(self):
        #inspired from https://github.com/rsundhar247/NLP-AbstractiveSummarizer
        sentence_list = nltk.sent_tokenize(self.textraw)
        for word in nltk.word_tokenize(self.text):
            if word not in self.stopwords:
                if word not in self.word_frequencies.keys():
                    self.word_frequencies[word] = 1
                else:
                    self.word_frequencies[word] += 1

        maximum_frequency = max(self.word_frequencies.values())

        for word in self.word_frequencies.keys():
            self.word_frequencies[word] = (self.word_frequencies[word] / maximum_frequency)
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in self.word_frequencies.keys():
                    if len(sent.split(' ')) < 40:  # limiting sentences with < 30 words
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = self.word_frequencies[word]
                        else:
                            sentence_scores[sent] += self.word_frequencies[word]

        summary_sentences = heapq.nlargest(self.N_sente_summ, sentence_scores, key=sentence_scores.get)
        self.summary = ' '.join(summary_sentences)


    # identify topics by creating vector of word
    def get_N_topic(self):
        #inspired by:
        # https://github.com/susanli2016/Machine-Learning-with-Python/blob/master/topic_modeling_Gensim.ipynb
        # https://github.com/susanli2016/Machine-Learning-with-Python/blob/master/Topic%20Modeling.ipynb

        dictionary = corpora.Dictionary(self.textformat)
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in self.textformat]
        Lda = gensim.models.ldamodel.LdaModel
        ldamodel = Lda(doc_term_matrix, num_topics= self.N, id2word=dictionary, passes=50)
        topics = ldamodel.print_topics(num_words=self.Nword)
        topss=[]
        for topic in topics:
            tops=[]
            for aa in topic[1].split(' + '):
                tops.append(aa.split('*')[1].replace('"',''))
            topss.append((' ').join(tops))
        self.topics=topss