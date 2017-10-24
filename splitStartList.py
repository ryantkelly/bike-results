import csv, sys

sourcefile = "start-list.csv"

categoryCol = 13 #column containing category name/info
otherCols = [0, 2, 3, 4, 5, 6, 7] #other columns we want

data = {}
rowcount = 0
with open(sourcefile, "r") as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    for row in reader:
        rowcount+=1
        if rowcount==1:
            continue
        if row[categoryCol] not in data:
            data[row[categoryCol]] = [[row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[13]]]
        else:
            data[row[categoryCol]].append([row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[13]])

for cat in data:
    writer = csv.writer(open('output/start-list-'+cat.replace('/', '-').replace(':', '-')+'.csv', 'w'))
    for row in data[cat]:
         writer.writerow(row)