import re
import os
from os.path import join
import csv
from argparse import ArgumentParser
from random import shuffle
from NaiveBayes import NaiveBayes

class NaiveBayesan:

    #Create CSV File with Classnames and their respective terms
    def createTrainingSet(self, dataset, output):
        f = open(output, 'w')
        csvFile = csv.writer(f, delimiter=',')
        for dirname in os.listdir(dataset):
            classname = dirname
            classpath = join(dataset, dirname)
            for dirpath, dirnames, filenames in os.walk(classpath):
                for filename in filenames:
                    filepath = join(dirpath, filename)
                    try:
                        r = open(filepath, 'r', errors='replace')
                    except Exception as e:
                        print('CreateTrainSet: Err open file: ' + str(filepath) + str(e))
                        continue
                    contents = ''.join(r.readlines())
                    cleanContent = self._cleanHTML(contents)
                    terms = self._tokenize(cleanContent)
                    terms.insert(0, classname)
                    csvFile.writerow(terms)
        f.close()
    #returns list containing all words in text
    def _tokenize(self,text):
        terms = re.findall(r'\w+', text)
        terms = [term for term in terms if not term.isdigit()]
        return terms

    def _cleanHTML(self, text):
        removeTagsRE = re.compile('<.*?>')
        removeSpaceRE = re.compile(' +|\t+')
        body = ''.join(re.findall(r'<body.*>.*</body>+', text.replace('\n', '')))
        cleanText = re.sub(removeTagsRE, ' ', body) 
        spacefree = re.sub(removeSpaceRE, ' ', cleanText)
        return spacefree

    def setCsvOutputPath(self,path):
        self._csvOutput = path

    def setDataSetPath(self, path):
        self._dataSetPath = path

    #Load dictionary with classes and Terms
    def loadClasses(self,dataset_file):
        self.classes = {}
        f = open(dataset_file, 'r')
        csvFile = csv.reader(f, delimiter=',')
        for row in csvFile:
            classname, terms = row[0], row[1:]
            self.classes.setdefault(classname, [])
            self.classes[classname].append(terms)
        f.close 

    def trainModel(self):
        self.classifier.train(self.classes)

    def classify(self,text):
        terms = self._tokenize(text)
        classification = self.classifier.classify(terms)
        return classification

    def __init__(self):
        self.classifier = NaiveBayes()
