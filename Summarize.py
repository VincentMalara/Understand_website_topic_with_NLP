from langdetect import detect


class Text():
    def __init__(self):
        self.lang = ''
        self.textlist = []
        self.text = ''
        self.sentence_list = []
        self.stopwords = []
        self.word_frequencies = {}

    def plot_cloud(self):
        # remove word from url such as company name
        textplot = (' ').join([x for x in text.split(' ') if x not in url])

        # Wordcloud creation (inspired by: https://www.geeksforgeeks.org/generating-word-cloud-python/)
        wordcloud = WordCloud(width=600, height=400,
                              background_color='white',
                              stopwords=stopwords,
                              min_font_size=10).generate(textplot)
        # WordCloud Plot
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()


textlist = [' '.join(x.split()) for x in page.getAllTextCombined()]
textraw = ('. ').join(manage_last_point(x) for x in textlist if x)
text = re.sub('[^a-zA-Z]', ' ', textraw)
text = re.sub(r'\s+', ' ', text)

sentence_list = nltk.sent_tokenize(textraw)

stopwords = nltk.corpus.stopwords.words('english')

for word in nltk.word_tokenize(text):
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

summary = ' '.join(summary_sentences)
print(summary)