# -*- coding:utf-8 -*-
import pickle,csv

my_file = open('kakidata'+str(4)+'.txt','r')
my_data = pickle.load(my_file)
for word in my_data[1][401][0] :
    print word

quizs = file('C:\Users\LENOVO\OneDrive\kanji\data\quiz'+str(4)+'.csv', 'rb')
reader = csv.reader(quizs)
kakimondai = [] 
for line in reader:

    kanji = line[0].split(' ')
    for i in range(len(kanji)) :
        if kanji[i] == 'x' :
            kanji[i] = '\xa9\x96' 
    kakimondai.append( [kanji, line[1].split(' '), line[2] ] )
quizs.close()

for word in kakimondai[401][0] :
    print word
