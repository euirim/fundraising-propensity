import csv
import datetime
import pickle
import spacy
import sys
import os
from gensim.models.doc2vec import Doc2Vec
from ds import *
from sentence_transformers import SentenceTransformer

start_range, end_range = int(sys.argv[1]), int(sys.argv[2]) # Set both to -1 to read full file
skip_completed_campaigns = True # Don't read campaigns that have unknown goal due to being completed. If set to False, goal is set to 0.
output_documents = False # If True, outputs .txt file of each story and title to data/documents

with open(sys.argv[3], 'rb') as pickle_file:
    categories = pickle.load(pickle_file)

num_categories = 0
dataset = []
nlp = spacy.load('en_core_web_lg')
title_vectorization_technique = 'bert'
story_vectorization_technique = 'doc2vec'
cover_image_vectorization_technique = 'word2vec'
story_image_vectorization_technique = 'word2vec'

out_file = open('dataset_' + str(start_range) + '_' + str(end_range) + '.csv','w')
out_writer = csv.writer(out_file, delimiter=',')

bert_model = SentenceTransformer('bert-base-nli-mean-tokens')

def get_average_word2vec(input_str):
    input_str = nlp(input_str)
    return input_str.vector

story_doc2vec_model = None
title_doc2vec_model = None
def get_story_doc2vec(story_doc2vec_model, input_str):    
    return list(story_doc2vec_model.infer_vector(input_str.split()))
    

def get_title_doc2vec(title_doc2vec_model, input_str):
    return list(title_doc2vec_model.infer_vector(input_str.split()))

def get_bert_vec(bert_model, input_str):
    result = bert_model.encode([input_str])
    return list(result[0])

with open('data/captioned_small.csv') as csv_file:
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
        rownum, url,title,story,created,goal,category,finished,first_cover_image,story_images, raised, cover_image_autocaption, story_images_autocaption, story_image_autocaption = row
        print(row)
        exit(0)
        #title, story, created, raised, goal, category, finished = row
         
        if title_vectorization_technique == 'word2vec':
            title_vec = get_average_word2vec(title)
        elif title_vectorization_technique == 'doc2vec':
            if title_doc2vec_model is None:
                title_doc2vec_model = Doc2Vec.load(os.path.join("models","title_doc2vec.model"))
            title_vec = get_title_doc2vec(title_doc2vec_model, title)
        elif title_vectorization_technique == 'bert':
            title_vec = get_bert_vec(bert_model, title)
        else:
            print("Error: An invalid title vectorization technique was selected.")

        if story_vectorization_technique == 'word2vec':
            story_vec = get_average_word2vec(story)
        elif story_vectorization_technique == 'doc2vec':
            if story_doc2vec_model is None:
                story_doc2vec_model = Doc2Vec.load(os.path.join("models","story_doc2vec.model"))
            story_vec = get_story_doc2vec(story_doc2vec_model, story)
        else:
            print("Error: An invalid story vectorization technique was selected.")

        if cover_image_vectorization_technique == 'word2vec':
            cover_image_vec = get_average_word2vec(cover_image_autocaption)
        else:
            print("Error: An invalid cover image vectorization technique was selected.")
        
        if story_image_vectorization_technique == 'word2vec':
            story_image_vec = get_average_word2vec(story_image_autocaption)
        else:
            print("Error: An invalid story image vectorization technique was selected.")

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
        out_row.extend(title_vec)
        out_row.extend(story_vec)
        out_row.extend(cover_image_vec)
        out_row.extend(story_image_vec)
        out_row.append(raised)

        if line_counter == 1:
            headings = ["url","title","story","created","goal","category","finished","first_cover_image","story_images"]
            headings.extend(["title_vec_{}".format(i) for i in range(0, len(title_vec))])
            headings.extend(["story_vec_{}".format(i) for i in range(0, len(story_vec))])
            headings.extend(["cover_image_vec_{}".format(i) for i in range(0, len(cover_image_vec))])
            headings.extend(["story_image_vec_{}".format(i) for i in range(0, len(story_image_vec))])
            headings.append("raised")
            out_writer.writerow(headings)

        out_writer.writerow(out_row)


        # dataset.append(Data(Features(title, story, created, goal, category, finished), raised))

        line_counter += 1

out_file.close()
#with open('dataset_' + str(start_range) + '_' + str(end_range) + '.pkl', 'wb') as pickle_file:
#    pickle.dump(dataset, pickle_file)
