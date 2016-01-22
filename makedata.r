library(stringr)

tt=readLines("my_kaki_04.txt",encoding ="UTF-8" )

answer = str_sub(str_extract(tt[1],"\\（.*\\）"), 2,-2)#提取答案
quiz = sub(pattern="\\（.*）",replacement="x",tt[1]) #把答案替换成x
monji = gsub(pattern="(\\［[^］]*］)|(｛[^｝]*｝)",replacement=" ",quiz) #去掉注音
monji = str_trim(monji, side = "both" )
kana = str_c(str_sub( str_extract_all(
    quiz,"\\｛[^｝]*\\｝|\\［[^\\］]*\\］")[[1]], 2, -2 ), collapse = " ")

gsub(pattern="\\［[^］]*］",replacement=" ",tt[1])
sub(pattern=".*\\（(.*)）.*",replacement="\\1",tt[1]) #提取答案
sub(pattern="\\（.*）",replacement="x",tt[1]) #把答案替换成x
fen2 = gsub(pattern="(\\［[^］]*］)|(｛[^｝]*｝)",replacement=" ",quiz) #去掉注音
fen2 = str_trim(fen2, side = "both" ) #去除2端空白

strsplit(fen2," ")[[1]] #包含汉字的部分

fen3 = gsub(pattern="[\\｝］][^｛［]*[｛［]",replacement="-",tt[1]) #先去掉中间部分汉字
fen3 = gsub(pattern="^.*[｛［]|[｝］].*$",replacement="-",fen3) #去掉首尾部分汉字
fen3 = strsplit(fen3,"-")[[1]]
