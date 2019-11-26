# https://medium.com/@klintcho/doc2vec-tutorial-using-gensim-ab3ac03d3a1
'''
This script trains a doc2vec model from a folder of .txt files.
'''


from os import listdir
import os
from os.path import join, isfile
import gensim
from gensim.models.doc2vec import LabeledSentence
from os import listdir
from os.path import isfile, join
import gensim


docLabels = []
docLabels = [f for f in listdir(os.path.join('data','documents','story')) if f.endswith('.txt')]

data = []
for doc in docLabels:
    with open(os.path.join('data','documents','story', doc), 'r') as file:
        contents = file.read()
        data.append(contents)


class DocIterator(object):
    def __init__(self, doc_list, labels_list):
       self.labels_list = labels_list
       self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield LabeledSentence(words=doc.split(),tags=[self.labels_list[idx]])

it = DocIterator(data, docLabels)

print("Initializing model...")
model = gensim.models.Doc2Vec(size=300, window=10, min_count=5, workers=11,alpha=0.025, min_alpha=0.025) # use fixed learning rate
print("Building vocab...")
model.build_vocab(it)
print("Training model with {} examples and {} epochs...".format(model.corpus_count, 15))
model.train(it, total_examples=model.corpus_count, epochs=15, report_delay=5)
print("Saving model...")
model.save(os.path.join('data','story_doc2vec.model'))

