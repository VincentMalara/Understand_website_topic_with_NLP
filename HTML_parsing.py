from bs4 import BeautifulSoup
import requests
#import re
#import pandas as pd

class Page():
    def __init__(self):
        self.url =''
        self.html =''
        self.Ps = []
        self.Spans = []
        self.H1s = []
        self.H2s = []
        self.H3s = []
        self.H4s = []
        self.H5s = []
        self.H6s = []
        self.getalldone = False
        self.links = []


    def seturl(self, url):
        #add url analysis to pre check
        self.url=url

    def extract_html_page(self):
        response = requests.get(self.url)
        self.html = BeautifulSoup(response.content, "html.parser")

    def getP(self):
        AllP = self.html.findAll('p')
        for P in AllP:
            self.Ps.append(P.get_text())

    def getSpan(self):
        Allspan = self.html.findAll('span')
        for span in Allspan:
            self.Spans.append(span.get_text())

    def getH(self):
        for n in [n + 1 for n in range(6)]:
            AllH = self.html.findAll('h'+str(n))
            for H in AllH:
                exec(f"self.H{str(n)}s.append(H.get_text())")

    def getAllText(self):
        if self.getalldone == False:
            self.getP()
            self.getSpan()
            self.getH()
            self.getLinks()
            self.getalldone = True

    def getAllTextCombined(self):
        self.getAllText()
        Alltext=[]

        for n in [n + 1 for n in range(6)]:
            AllH = []
            exec(f"AllH = self.H{str(n)}s")
            for H in AllH:
                Alltext.append(H)

        for span in self.Spans:
            Alltext.append(span)
        for P in self.Ps:
            Alltext.append(P)
        return Alltext

    def getLinks(self):
        for link in self.html.findAll('a'): #attrs={'href': re.compile("^http://")}):
            #print(link.get('href'))
            self.links.append(link.get('href'))