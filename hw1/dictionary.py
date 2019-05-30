# coding: utf-8

# 辞書を読み込み大文字を小文字に変換、元の文字列とソートした文字列辞書を作る
dic = {}
with open('dictionary.words.txt', 'r') as f:
    for line in f:
        word = line.rstrip('\n').lower()
        new_word = ''.join(sorted(word))
        dic[word] = new_word

dic_sorted = sorted(dic.items(), key=lambda x:x[1])

# 書き込み
f = open('newdictionary.txt', 'w')
for i in range(len(dic_sorted)):
    for j in range(len(dic_sorted[i])):
        if j == len(dic_sorted[i])-1:
            f.write(str(dic_sorted[i][j]))
        else:
            f.write(str(dic_sorted[i][j]) + ' ')
    if i != len(dic_sorted)-1:
        f.write('\n')
f.close()



