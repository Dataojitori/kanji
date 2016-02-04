# -*- coding:utf-8 -*-
import pygame, time, pickle
from pygame.locals import *
from sys import exit
from classwork import *
		
#魔法变量
screen_size = (800,600)
red = (201,56,52)
dark_red = (157,54,51)
blue = (47,65,137)
dark_blue = (43,56,107)
light_blue = (146, 168, 209)
ruriiro = (37, 63, 130)

pygame.init()
clock = pygame.time.Clock() 
screen = pygame.display.set_mode(screen_size, 0, 32)
pygame.display.set_caption("ソフト")
background = pygame.image.load("stp_l_017.jpg").convert()

#读取题库
alldatas = {}
for n in range(7)[1:] : 
    my_file = open('kakidata'+str(n)+'.txt','r')  
    my_data = pickle.load(my_file)
    my_file.close()  
    alldatas[my_data[2]] = my_data[:2]
#总分数
all_score = sum([ sum([d['score'] for d in s[0].values()]) \
				  for s in alldatas.values() ])
hp = time_to_hp(all_score)
haaku_kanji = sum([ sum([ score_to_haaku(d['score']) for d in s[0].values()]) \
				  for s in alldatas.values() ])
print haaku_kanji

class menu:
	"""游戏初始菜单"""
	def __init__(self):

		self.background = pygame.Surface(screen_size)
		self.background.fill((200,200,200))
		self.buttons = set()

		button_size = (screen_size[0]/4, 40)
		start_cent = (screen_size[0]/2, screen_size[1]/4)
                 
		#开始游戏按钮
		game_start = button(u"始め", button_size)
		game_start.setichi(( start_cent[0]-button_size[0]/2, \
							 start_cent[1]-button_size[1]/2 ))
		self.buttons.add( (game_start, "question") )

	def run(self, screen):

		while True:    
		    for event in pygame.event.get():
		        if event.type == QUIT:            
		            pygame.quit()
		            exit()
		        elif event.type == MOUSEBUTTONDOWN :
		        	for b in self.buttons :
		        		b[0].combo(event.pos)
		        elif event.type == MOUSEBUTTONUP :
		        	for b in self.buttons :
		        		click = b[0].reset(event.pos)
		        		if click :
		        			print 'hit'
		        			global nowpage
		        			nowpage = b[1]
		        			return
		            
		    clock.tick(60)
		    screen.blit( self.background, (0,0) )

		    for b in self.buttons :
		    	b[0].draw(self.background)
		    
		    pygame.display.update()
		    
class question:
	"""出题页面"""
	def __init__(self):		
		self.background = pygame.Surface(screen_size)
		self.background.fill((247,202,201))
		
		self.words = set()
		self.buttons = set()
		self.clean = False		
		#题目的汉字部分
		kanji_size = 80
		kana_size = 40
		#随机抽取一道题的data,问题,所属题库文件名
		self.one_data, mondai, self.filename, shinsen, cooldown = pickup2(alldatas) 
		print "probability" , data_to_probability(self.one_data)
		#修正题目为全假名的情况
		mondai = is_all_kana(mondai)
		#self.one_data = alldatas['kakidata5.txt'][0]['\xd4O']
		#mondai = is_all_kana( alldatas['kakidata5.txt'][1][438] )
		print self.filename
		print self.one_data['ichi']
		kanji_line = [ bun(x.decode('mbcs'), kanji_size) for x in mondai[0]]
		kana_line = [ bun(x.decode('mbcs'), kana_size) for x in mondai[1]]
		#计算最大行宽
		line_width = sum( [ max( kanji_line[n].get_width(), \
								 kana_line[n].get_width() ) \
							for n in range(len(kanji_line)) ] )
		#根据行宽计算汉字行的起点坐标,使汉字行居中
		start_point = [ (screen_size[0]-line_width)/2, kanji_size ] 
		#给每段文字分配坐标并添加到文字集合里
		for n in range(len(kanji_line)) :
			w = kanji_line[n]
			k = kana_line[n]
			w.setichi( (start_point[0], start_point[1]) )
			k.setichi( (start_point[0], start_point[1]-kana_size) )
			start_point[0] += max( w.get_width(), k.get_width() )
			self.words.add(w)
			self.words.add(k)
			
		#答案部分
		answer_size = 300 #答案字号
		pix_to_ground = 80 #答案距离底边的高度
		#左边显示答案
		self.answer = button( mondai[2].decode('mbcs'), (answer_size, answer_size),\
						 (255,231,231) )
		self.answer.setichi( ( (screen_size[0]-answer_size*2)/4, \
						   screen_size[1]-pix_to_ground-answer_size ) )
		self.answer.block_word()
		self.words.add(self.answer)
		#右边手写区
		answer_tekaku = button( "", (answer_size, answer_size), (255,231,231) )		
		answer_tekaku.setichi( (screen_size[0]*0.75-answer_size/2, \
								screen_size[1]-pix_to_ground-answer_size ))		
		self.words.add(answer_tekaku)
		
		#按钮部分
		#右下角提交		
		self.submit = button('submit', (answer_size, pix_to_ground), \
							 light_blue, ruriiro)
		self.submit.setichi( [answer_tekaku.get_ichi()[0], \
						 answer_tekaku.get_ichi()[1] + answer_size] )
		self.submit.link_to( "self.answer.show_word(); self.submit.hide_button(); \
						      self.right.show_button(); self.wrong.show_button()" )
		
		self.buttons.add(self.submit)
		#判断对错
		ox_size = ( (screen_size[0]-answer_size*2)/2, answer_size/2 )
		self.right = button(u'O', ox_size, red, dark_red)
		self.right.setichi( (self.answer.get_ichi()[0] + answer_size, \
							 self.answer.get_ichi()[1]) )
		self.right.link_to( "self.submit_answer('right')" )
		self.right.hide_button() 
		self.buttons.add(self.right)
		self.wrong = button(u'X', ox_size, blue, dark_blue)
		self.wrong.setichi( (self.answer.get_ichi()[0] + answer_size, \
		 					 self.answer.get_ichi()[1] + answer_size/2) )
		self.wrong.link_to( "self.submit_answer('wrong')" )
		self.wrong.hide_button()
		self.buttons.add(self.wrong)
		
		#显示分数
		global all_score
		num_size = 25
		seiseki = bun( u'得点:'+str(round(all_score, 2)), num_size )
		seiseki.setichi( [screen_size[0] - seiseki.get_width(), 0] )
		self.words.add(seiseki)
		#显示hp
		global hp
		life = bun( 'hp:'+str(round(hp, 2)), num_size )
		life.setichi( [screen_size[0] - life.get_width(), num_size*1])
		self.words.add(life)
		#新鲜度
		shinsen = bun( u'新鮮:'+str(shinsen), num_size )
		shinsen.setichi( [screen_size[0] - shinsen.get_width(), num_size*2])
		self.words.add(shinsen)
		#新鲜度
		cooldown = bun( u'冷却率:'+str(cooldown), num_size )
		cooldown.setichi( [screen_size[0] - cooldown.get_width(), num_size*3])
		self.words.add(cooldown)
		
	def submit_answer(self, answer) :
		#提交答案并把答案记录到data里
		if answer == 'right' :
			#当答案正确时
			point = 1
		else :
			point = -1
		moto_score = self.one_data['score']
		self.one_data[answer] += 1
		self.one_data['history'].append(point)		
		self.one_data['score'] = ( self.one_data['score'] + point ) \
								 * abs(sum(self.one_data['history'][-5:])) \
								 / float(len( self.one_data['history'][-5:] ))
		self.one_data['time'].append( time.time() )
		print self.one_data
		print data_to_probability(self.one_data) #出现概率
		self.clean = True
		#保存文件
		my_file = open( self.filename,'w' )  
		pickle.dump( alldatas[self.filename]+[self.filename], my_file )
		my_file.close()
		
		global all_score, hp
		all_score += self.one_data['score'] - moto_score
		hp = time_to_hp(all_score)
		
	def run(self, screen):

		while True:    
		    for event in pygame.event.get():
		        if event.type == QUIT:            
		            pygame.quit()
		            exit()
		        elif event.type == MOUSEBUTTONDOWN :	    		        	
		        	for b in self.buttons :
		        		b.combo(event.pos)
		        elif event.type == MOUSEBUTTONUP :
		        	for b in self.buttons :
		        		click = b.reset(event.pos)
		        		if click :		        			
		        			#print 'hit'			    		        				
		        			exec click   				        		
		            
		    clock.tick(60)
		    screen.blit( self.background, (0,0) ) #画背景

		    for w in self.words :
		    	w.draw(screen)	
		    for b in self.buttons :
		    	b.draw(screen)
		    
		    pygame.display.update()
		    
		    if self.clean :
		    	global pages
		    	pages["question"] = question()
		    	return
		
pages = {}
pages["menu"] = menu()
pages["question"] = question()

nowpage = "question"


while True:
	
	pages[nowpage].run(screen)

print "all done"


mygame = alldatas.values()[0][0]
print sum([ x['score'] for x in mygame.values() ])
#出现概率
[ num_to_probability(x['score']) for x in mygame.values() ]
[ data_to_probability(x) for x in mygame.values() ]



