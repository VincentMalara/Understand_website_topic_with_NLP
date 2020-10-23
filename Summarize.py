from langdetect import detect
import nltk
import heapq
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re



def manage_last_point(x):
    x = x.strip().lower()
    if x[-1] == '.':
        x = x[0:-1]
    else:
        x = x
    return x


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

    def inputtext(self,textlist, url):
        self.textlist=textlist
        self.url = url
        self.textraw = ('. ').join(manage_last_point(x) for x in self.textlist if x)
        text = re.sub('[^a-zA-Z]', ' ', self.textraw)
        self.text = re.sub(r'\s+', ' ', text)

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

    def plot_cloud(self):
        if self.lang == '':
            self.getlang()
        # remove word from url such as company name
        textplot = (' ').join([x for x in self.text.split(' ') if x not in self.url])

        # Wordcloud creation (inspired by: https://www.geeksforgeeks.org/generating-word-cloud-python/)
        wordcloud = WordCloud(width=600, height=400,
                              background_color='white',
                              stopwords=self.stopwords,
                              min_font_size=10).generate(textplot)
        # WordCloud Plot
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()

    def get_summary(self):
        #inspired from https://github.com/rsundhar247/NLP-AbstractiveSummarizer
        sentence_list = nltk.sent_tokenize(self.textraw)
        for word in nltk.word_tokenize(self.text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequency = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word] / maximum_frequency)
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 40:  # limiting sentences with < 30 words
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
        self.summary = ' '.join(summary_sentences)