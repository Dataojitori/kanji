library(stringr)


format <- function( word ){
    answer = str_sub(str_extract(word,"\\（.*\\）"), 2,-2)#提取答案
    quiz = sub(pattern="\\（.*）",replacement="x",word) #把答案替换成x
    monji = gsub(pattern="(\\［[^］]*］)|(｛[^｝]*｝)",replacement=" ",quiz) #去掉注音
    monji = str_trim(monji, side = "both" )
    kana = str_c(str_sub( str_extract_all(
        quiz,"\\｛[^｝]*\\｝|\\［[^\\］]*\\］")[[1]], 2, -2 ), collapse = " ")
    
    out = c(monji, kana, answer)
    return( out )
}
          
file = "C:/Users/LENOVO/OneDrive/kanji/data/"
for (i in 10:11) {
    name = paste(file, "my_kaki_", i, ".txt", sep="")
    print(name)
    
    data=readLines(name,encoding ="UTF-8" )        
    #每一行为汉字部分,注音部分,答案
    barabara = t( sapply( data, format,USE.NAMES = F ) )
    kanjis = levels( factor( barabara[,3] ) )
    #每一个汉字所在行数
    zu = t( sapply(kanjis, function(x)  which(barabara[, 3] == x) ) ) 
    write.table(zu, paste("index", i, ".csv", sep=""), 
                col.names = F, sep=",")
    write.table(barabara,paste("quiz", i, ".csv", sep=""), 
                col.names = F, row.names = F, sep=",")
}


