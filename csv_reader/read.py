import csv
import datetime
import pickle
import spacy
import sys
import os
from ds import *

start_range, end_range = int(sys.argv[1]), int(sys.argv[2]) # Set both to -1 to read full file
skip_completed_campaigns = True # Don't read campaigns that have unknown goal due to being completed. If set to False, goal is set to 0.
output_documents = False # If True, outputs .txt file of each story and title to data/documents

with open(sys.argv[3], 'rb') as pickle_file:
    categories = pickle.load(pickle_file)

num_categories = 0
dataset = []
nlp = spacy.load('en_core_web_lg')

out_file = open('dataset_' + str(start_range) + '_' + str(end_range) + '.csv','w')
out_writer = csv.writer(out_file, delimiter=',')

with open('data/out_full2.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_counter = 0
    num_rows = sum(1 for row in csv_reader)
    csv_file.seek(0)
    for rownum, row in enumerate(csv_reader):
        if line_counter % 100 == 0:
            print ('{}/{}'.format(line_counter, num_rows))

        if line_counter == 0 or (start_range != -1 and line_counter < start_range):
            line_counter += 1
            continue
        if end_range != -1 and line_counter == end_range:
            break
        url,title,story,created,raised,goal,category,finished,first_cover_image,story_images = row
        #title, story, created, raised, goal, category, finished = row
         

        title = nlp(title)
        story = nlp(story)

        ycreated, mcreated, dcreated = created.split('-')
        created = int(datetime.datetime(int(ycreated), int(mcreated), int(dcreated), 0, 0).timestamp())
        
        raised = int(raised)

        if len(goal) == 0:
            if skip_completed_campaigns: continue
            goal = 0
        else:
            goal = int(goal)

        category = categories[category]

        finished = int(finished)

        if output_documents:
            print(story,  file=open(os.path.join('data','documents','story',str(rownum)+'.txt'), 'w'))
            print(title,  file=open(os.path.join('data','documents','title',str(rownum)+'.txt'), 'w'))

        out_row = [url,str(title).replace("\n"," "),str(story).replace("\n"," "),created,goal,category,finished,first_cover_image,story_images]
        out_row.extend(title.vector)
        out_row.extend(story.vector)
        out_row.append(raised)

        if line_counter == 1:
            headings = ["url","title","story","created","goal","category","finished","first_cover_image","story_images"]
            headings.extend(["title_vec_{}".format(i) for i in range(0, len(title.vector))])
            headings.extend(["story_vec_{}".format(i) for i in range(0, len(story.vector))])
            headings.append("raised")
            out_writer.writerow(headings)

        out_writer.writerow(out_row)


        # dataset.append(Data(Features(title, story, created, goal, category, finished), raised))

        line_counter += 1

out_file.close()
#with open('dataset_' + str(start_range) + '_' + str(end_range) + '.pkl', 'wb') as pickle_file:
#    pickle.dump(dataset, pickle_file)
