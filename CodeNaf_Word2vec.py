import pandas as pd
from Summarize import clean
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import numpy as np
from gensim.models import KeyedVectors
import gensim


class word2vec_NAF():
    def __init__(self):
        self.stopwords=[]
        self.NAF=pd.DataFrame()
        self.sim=0
        self.best_NAF=''

    def load_Naf(self):
        self.NAF=pd.read_excel('NAF.xls')
        self.NAF['sim'] = np.zeros(self.NAF.shape[0])

    def clean_Naf(self):
        if self.NAF.empty:
            self.load_Naf()
        #language sensitivity to be implemented
        self.stopwords = stopwords.words('english')
        lemma=WordNetLemmatizer()
        cleant=[]
        for i in self.NAF['intitulé de la naf english']:
            cleant.append(clean(i, self.stopwords, '', lemma))
        self.NAF['cleant_intitul']=cleant

    def find_naf(self, sentences):
        ii = 0
        res=[]
        for naf in self.NAF['cleant_intitul']:
            sim = []
            for sente in sentences:
                try:
                    sim.append(self.model.n_similarity(sente.split(' '), naf.split(' ')))
                except:
                    sim.append(0)
            res.append(np.mean(sim))
            ii += 1
        self.NAF['sim'] = res
        self.best_NAF = self.NAF.loc[self.NAF['sim'].idxmax(), 'intitulé de la naf english']
        self.best_NAF_fr = self.NAF.loc[self.NAF['sim'].idxmax(), 'intitulé de la naf french']
        self.best_NAF_code = self.NAF.loc[self.NAF['sim'].idxmax(), 'code']



    def loadmodel(self):
        print('Model loading (long step to be improved)---')
        import os
        from gensim.models import KeyedVectors
        from gensim.downloader import base_dir

        def load_data():
            path = os.path.join(base_dir, 'glove-twitter-25', 'glove-twitter-25.gz')
            model = KeyedVectors.load_word2vec_format(path)
            return model
        #self.model = KeyedVectors.load_word2vec_format('/glove-twitter-25', binary=False)
        self.model = load_data()
        print('---Model loaded')


