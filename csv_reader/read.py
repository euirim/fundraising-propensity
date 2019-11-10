import csv
import datetime
import pickle
import spacy
import sys
from ds import *

start_range, end_range = int(sys.argv[1]), int(sys.argv[2])
with open(sys.argv[3], 'rb') as pickle_file:
    categories = pickle.load(pickle_file)

num_categories = 0
dataset = []
nlp = spacy.load('en_core_web_sm')

with open('out.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_counter = 0
    num_rows = sum(1 for row in csv_reader)
    csv_file.seek(0)
    for row in csv_reader:
        if line_counter % 100 == 0:
            print ('{}/{}'.format(line_counter, num_rows))

        if line_counter == 0 or line_counter < start_range:
            line_counter += 1
            continue
        if line_counter == end_range:
            break
        title, story, created, raised, goal, category, finished = row

        title = nlp(title)
        story = nlp(story)

        ycreated, mcreated, dcreated = created.split('-')
        created = int(datetime.datetime(int(ycreated), int(mcreated), int(dcreated), 0, 0).timestamp())
        
        raised = int(raised)

        if len(goal) == 0:
            goal = 0
        else:
            goal = int(goal)

        category = categories[category]

        finished = int(finished)

        dataset.append(Data(Features(title, story, created, goal, category, finished), raised))

        line_counter += 1

with open('dataset_' + str(start_range) + '_' + str(end_range) + '.pkl', 'wb') as pickle_file:
    pickle.dump(dataset, pickle_file)
