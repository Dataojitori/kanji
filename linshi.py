# -*- coding:utf-8 -*-
import pickle,csv

my_file = open('my_kanas','r')
my_set = pickle.load(my_file)
my_file.close()

##my_file = open('kanas.txt','r')
##my_set = set()
##for line in my_file.readlines():
##    line = line.strip()  
##    for w in line.split(' ') :
##        my_set.add(w.decode('mbcs'))
##my_file.close()
##
##my_file = open('my_kanas','w' )
##pickle.dump( my_set, my_file )
##my_file.close()


my_file = open('kakidata'+str(5)+'.txt','r')
my_data = pickle.load(my_file)
my_file.close()
#print [ n for n in range(len(my_data[1][438][0])) ]
mondai = my_data[1][438] 
print mondai
for n in range(len(mondai[0])) :
    word = mondai[0][n]
    numkana = [ k in my_set for k in word.decode('mbcs') ]
    print word
    print numkana
    if sum( numkana ) == len(word.decode('mbcs')) :
        mondai[1].insert( n, '' )
##    for w in word.decode('mbcs') :
##        print w in my_set




##quizs = file('C:\Users\LENOVO\OneDrive\kanji\data\quiz'+str(4)+'.csv', 'rb')
##reader = csv.reader(quizs)
##kakimondai = [] 
##for line in reader:
##
##    kanji = line[0].split(' ')
##    for i in range(len(kanji)) :
##        if kanji[i] == 'x' :
##            kanji[i] = '\xa9\x96' 
##    kakimondai.append( [kanji, line[1].split(' '), line[2] ] )
##quizs.close()
##
##for word in kakimondai[401][0] :
##    print word
