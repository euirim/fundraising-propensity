import csv


out_file = open('data/captioned_no_vectors.csv','w')
out_writer = csv.writer(out_file, delimiter=',')

with open('data/out_final.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    keep_indices = []
    for rownum, row in enumerate(csv_reader):
        if rownum == 0:
            for index, colname in enumerate(row):
                if "vec" not in colname:
                    keep_indices.append(index)

        out_row = []
        for keep_index in keep_indices:
            out_row.append(row[keep_index])
        

        out_writer.writerow(out_row)

out_file.close()