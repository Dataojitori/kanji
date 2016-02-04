# -*- coding:utf-8 -*-
import pygame, time, pickle, random
from math import e
from pygame.locals import *
from sys import exit

class bun(object):
    """可显示的文字"""
    font_color = (2,50,164)
    def __init__(self, word, font_size):        
        self.font = pygame.font.Font( "NotoSansCJKjp-Regular.otf", font_size)                                                        
        self.word_picture = self.font.render( word, False, self.font_color )
        
    def get_width(self):
        #返回文字部分长度像素
        return self.word_picture.get_width()

    def setichi(self, word_ichi):
        #设定左上角坐标,并生成按钮工作区
        self.word_ichi = word_ichi
       
    def draw(self, screen):
        #给定表面,画图     
        screen.blit( self.word_picture, self.word_ichi )
        
class button(bun):
    #给定文字,长,宽,生成一个按钮
    color_normal = (233,67,233)
    color_excite = (255,0,0)
    #font_color = (0,255,0)

    def __init__(self, word, size, c_normal = None, c_excite = None):
        self.size = size
        if c_normal :
            self.color_normal = c_normal
        if c_excite :
            self.color_excite = c_excite
        self.tu = pygame.Surface(self.size)
        self.tu.fill(self.color_normal)   
        #文字部分
        super(button, self).__init__(word, int(self.size[1]*0.8))    
        self.draw_word = True   
        #可执行语句
        self.magic = "None"
        #是否隐藏
        self.hide_all = False
        
    def setichi(self, ichi):
        #设定左上角坐标,并生成按钮工作区
        self.ichi = ichi
        super(button, self).setichi((self.ichi[0] + self.size[0]/2 - \
                          self.word_picture.get_width()/2, self.ichi[1] + \
                          self.size[1]/2 - self.word_picture.get_height()/2))     
        self.rect = Rect(self.ichi, self.size)
        
    def get_ichi(self) :
        return self.ichi
        
    def get_width(self):
        #获得按钮宽度
        return self.tu.get_width()
        
    def block_word(self) :
        #把文字改为不描绘
        self.draw_word = False
        
    def show_word(self) :
        #把文字改为可见
        self.draw_word = True
        
    def show_button(self) :
        #显现按钮
        self.hide_all = False
        
    def hide_button(self) :
        #隐藏按钮
        self.hide_all = True

    def combo(self, pos):
        #检测所给坐标是否在按钮区域内,是就返回true并引发按钮变色
        if not self.hide_all :
            if self.rect.collidepoint(pos) :
                self.tu.fill(self.color_excite) 
                return True
            
    def link_to(self, wtf) :
        #当按钮被触发后要引发何种事件
        self.magic = wtf

    def reset(self, pos):
        #按钮颜色复原并且如果被点击就返回True
        self.tu.fill(self.color_normal)
        if not self.hide_all :            
            if self.rect.collidepoint(pos) :                      
                return self.magic  
        
    def draw(self, screen):
        #给定表面,画图
        if self.hide_all == False:
            screen.blit( self.tu, self.ichi)
            if self.draw_word == True :
                super(button, self).draw(screen)
            #print self.hide, time.time()


def num_to_probability(num) :
    #给一个分数,根据1 / ( 1 + e**z)返回它的对应概率
    #数值越大概率越小
    return 1 / ( 1 + e**num)
    
def cool_down(mytime) :
    #给定一个日期列表,根据它最后日期距现时刻的时长返回一个概率,时间越长概率越大 
    #如果列表为空,返回0.5   
    #间隔为2天时z为4
    if mytime :
        z = 4 - (time.time() - mytime[-1] ) / 86400 * 4 
        return num_to_probability(z)
    else :
        return 0.5
        
def data_to_probability(dirt) :
    #给定游戏字典里的一行值,返回它的加权概率
    return num_to_probability( dirt['score'] ) * cool_down(dirt['time'])
    
def pickup(datas):
    #传入不同年级题库的集合,按照加权随机从题库中出题,
    #返回所选题的[data,题目,文件名]
    
    #求总加权分数
    probabilitys = []
    aver_time = 0  
    aver_prob = 0
    this_time = time.time()
    for filename in datas :
        mygame = datas[filename][0]
        for x in mygame.values() :
            one_prob = data_to_probability(x)
            probabilitys.append( one_prob )
            aver_prob += one_prob**2
            if x['time'] :              
                aver_time += one_prob * ( this_time - x['time'][-1] )
            else :
                aver_time += one_prob * 3600 * 48               
            
    totla_prob = sum(probabilitys)
    aver_time = round( aver_time / totla_prob / 3600, 2) #加权平均小时 
    aver_prob = round( aver_prob / totla_prob, 3)
        
    #probabilitys.sort(reverse = True)
    #print "加权平均小时", aver_time
    #print "加权平均概率", aver_prob
    totla_prob = totla_prob*random.random()    
    #根据随机数寻找目标
    for filename in datas :
        mygame, mondai = datas[filename]
        for key in mygame : #每一个字的资料
            totla_prob -= data_to_probability( mygame[key] )
            if totla_prob < 0 :
                quiz = mondai[ random.choice(mygame[key]['ichi'])-1 ]
                return [ mygame[key], quiz, filename, aver_time, aver_prob ]
        
def is_all_kana(mondai):
    #给一条mondai,检查汉字部分分块数是否跟假名部分分块数相等
    #如果不等,检查汉字部分哪一块是全假名,并用空集添加到假名部分相应分块
    #返回修正后的mondai
    if len(mondai[0]) == len(mondai[1]) :
        pass
    else :
        my_file = open('my_kanas','r')
        my_set = pickle.load(my_file)
        my_file.close()
        
        for n in range(len(mondai[0])) :
            word = mondai[0][n]
            numkana = [ k in my_set for k in word.decode('mbcs') ]
            if sum(numkana) == len( word.decode('mbcs') ) :
                #如果所有字符都为假名
                mondai[1].insert( n, '' )
    return mondai

def time_to_hp(all_score):
    #给定当前分数,求出当前hp
    starttime = 1454401404.71
    hp = ( starttime - time.time() ) / 3600 * 5 -161.33 + all_score
    return hp

def score_to_haaku(score):
    #把一道题的得分转换成对这个汉字的掌握率.只计算正值,负值返回0
    if score > 0 :     
        return 1 - num_to_probability(score)
    else :
        return 0
    
# datas = {}
# for n in range(7)[1:] : 
#     my_file = open('kakidata'+str(n)+'.txt','r')  
#     my_data = pickle.load(my_file)
#     my_file.close()  
#     datas[my_data[2]] = my_data[:2]
