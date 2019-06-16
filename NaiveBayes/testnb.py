from NaiveBayesan import NaiveBayesan
import os


NB = NaiveBayesan()
trainset = '/Users/webcrawler/Projects/Bachelor/CrawlerData/classes/medium'
testset = '/Users/webcrawler/Projects/Bachelor/CrawlerData/classes/small'


NB.createTrainingSet(trainset, 'trainset.csv')
NB.loadClasses('trainset.csv')
NB.trainModel()

for dirname in os.listdir(testset):
    classpath = os.path.join(testset, dirname)
    #print(classpath)
    for dirpath, dirnames, filenames in os.walk(classpath):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                f = open(filepath, 'r',  errors='replace')
            except Exception as e:
                print('TEST: Error reading file: ' + str(filepath) + ' ' + str(e))
            text = f.read()
            klasse = NB.classify(text)
            f.close()
            print('Klasse von: ' + filepath + str(klasse))
            """
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
print('Hallo Strasse')
for path, subdir, files in os.walk(testset):
    print('Hallo Statd')
    for name in files:
        print('Hallo welt')
        filepath = os.path.join(path, name)
        f = open(filepath, 'rb')
        klasse = NB.classify(f)
        f.close
        print('Klasse von: ' + filepath + str(klasse))
"""
