# coding: utf-8

# 辞書を読み込み大文字を小文字に変換、元の文字列とソートした文字列の辞書を作る
dic = {}
with open('dictionary.words.txt', 'r') as f:
    for line in f:
        word = line.rstrip('\n').lower()
        new_word = ''.join(sorted(word))
        dic[word] = new_word

dic_sorted = sorted(dic.items(), key=lambda x:x[1])

# 書き込み
with open('newdictionary.txt', 'w') as f:
    for origin, sort in dic_sorted:
        words = origin + ' ' + sort
        f.write(words+'\n')
f.close()



