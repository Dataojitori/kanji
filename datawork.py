# -*- coding:utf-8 -*-
import csv
import pickle

#把原始数据转换成python格式并保存

for n in range(2)[1:]:
	# ji = file('C:\Users\LENOVO\OneDrive\kanji\data\index'+str(n)+'.csv', 'rb')
	# reader = csv.reader(ji)
	# kakigame = {} #kaki游戏数据
	# for line in reader:
	    
	#     kakigame[line[0]] = {'ichi':[ int(x) for x in line[1:] ], 'right':0, \
	#                        'wrong':0, 'score':0, 'history':[], 'time':[] }
	# ji.close()

	#更改已知文件
	my_file = open('kakidata'+str(n)+'.txt','r')  
    my_data = pickle.load(my_file)
    my_file.close()      
    
	quizs = file('C:\Users\LENOVO\OneDrive\kanji\data\quiz'+str(n)+'.csv', 'rb')
	reader = csv.reader(quizs)
	kakimondai = [] #kaki题库 [ [汉字123],[注音123],"答案" ]
	for line in reader:

	    kanji = line[0].split(' ')
	    # for i in range(len(kanji)) :
	    #     if kanji[i] == 'x' :
	    #         kanji[i] = '\xa9\x96' 	  
	    kakimondai.append( [kanji, line[1].split(' '), line[2] ] )
	quizs.close() 


	savename = 'kakidata'+str(n)+'.txt'
	# datas = open( savename,'w' )  
	# pickle.dump( [kakigame, kakimondai, savename], datas)  
	# datas.close()  
	my_data[1] = kakimondai
	my_file = open('kakidata'+str(n)+'.txt','w' )  
	pickle.dump( my_data+[savename], my_file )
	my_file.close()

