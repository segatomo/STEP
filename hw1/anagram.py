# coding: utf-8
import itertools

# 辞書を読み込み
dic = []
with open('newdictionary.txt', 'r') as f:
    for line in f:
        dic.append(line.split())


# 与えられた文字が全て入っている単語を作るプログラム
"""
def make_word(a):
    a_list = []
    for x in itertools.permutations(a):
        a_list.append(''.join(x))
    
    return a_list """


# 与えられた文字からn文字選んで単語を作る
""" def make_word(a, n):
    a_list = []
    for x in itertools.permutations(a, n):
        a_list.append(''.join(x))

    return a_list """


# 1文字づつ入力を受け取る
try:
    from msvcrt import getch
except ImportError:
    def getch():
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def anagram(dic):
    """
    char: ソートした入力された文字
    origin_char: そのままの入力された文字
    word: 入力された文字に含まれる単語
    point: 得点
    best: matchのうちbestな単語
    best_point: bestの得点
    """
    char = ''
    origin_char = ''
    word = ''
    best = ''
    point = 0
    best_point = 0

    while True:
        print(word)
        print('Best: ' + best)
        # asciiコードを取得
        key = ord(getch())
        # asciiコードから文字へ
        char += chr(key)

        origin_char += chr(key)
        print('>>>' + origin_char + '\n')
        
        char = ''.join(sorted(char))

        if key == 3:
            break
        else:
            word = ''
            for d in dic:
                # d: 'abracadabra aaaaabbcdrr'とか
                c = char
                match = True
                for match_char in list(d[1]):
                    if c.find(match_char) != -1:
                        # cにmatch_charがあったら
                        c = c[:c.find(match_char)] + c[c.find(match_char)+1:]
                    else:
                        match = False
                        break

                if match == True:
                    # matchしたら
                    word += d[0] + ' '
                    point = len(d[1])

                    for letter in d[1]:
                        if letter in 'cfhlmpvwy':
                            point += 1
                        elif letter in 'jkqxz':
                            point += 2

                    if best_point < point:
                        best = d[0]
                        best_point = point


if __name__ == "__main__":
    anagram(dic)
