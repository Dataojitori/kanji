library(stringr)


kaki <- function( word ){
    answer = str_sub(str_extract(word,"\\（.*\\）"), 2,-2)#提取答案
    quiz = sub(pattern="\\（.*）",replacement="〇",word) #把答案替换成x
    monji = gsub(pattern="(\\［[^］]*］)|(｛[^｝]*｝)",replacement=" ",quiz) #去掉注音
    monji = str_trim(monji, side = "both" )
    kana = str_c(str_sub( str_extract_all(
        quiz,"\\｛[^｝]*\\｝|\\［[^\\］]*\\］")[[1]], 2, -2 ), collapse = " ")
    
    out = c(monji, kana, answer)
    return( out )
}
          
yomi <- function( word ){
    answer = str_sub(str_extract(word,"\\（.*\\）"), 2,-2)#提取答案
    kanji = str_sub(str_extract(word,"\\｛.*\\｝"), 2,-2)#提取答案汉字做索引
    quiz = sub(pattern="\\（.*）",replacement="（x）",word) #把答案替换成（x）
    #去掉注音
    monji = gsub(pattern="(\\［[^］]*］)|（x）",replacement=" ",quiz) 
    monji = gsub(pattern="[\\｛\\｝]",replacement="",monji) 
    monji = str_trim(monji, side = "both" )
    
    kana = str_c(str_sub( str_extract_all(quiz,"（x）|\\［[^\\］]*\\］")[[1]],
                          2, -2 ), collapse = " ")
    
    out = c(monji, kana, answer, kanji)
    return( out )
}

file = "C:/Users/LENOVO/OneDrive/kanji/data/"
for (i in 10:11) {
    name = paste(file, "my_kaki_", i, ".txt", sep="")    
    
    data=readLines(name,encoding ="UTF-8" )       
    
    #每一行为汉字部分,注音部分,答案
    barabara = t( sapply( data, kaki,USE.NAMES = F ) )
    print(name)
    kanjis = levels( factor( barabara[,3] ) )
    #每一个汉字所在行数
    zu = t( sapply(kanjis, function(x)  which(barabara[, 3] == x) ) ) 
#     write.table(zu, paste("yomiindex", i, ".csv", sep=""), 
#                 col.names = F, sep=",")
    write.table(barabara,paste("quiz", i, ".csv", sep=""), 
                col.names = F, row.names = F, sep=",")
}


