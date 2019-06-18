# coding: utf-8
import read_txt

def show_links():
    links = read_txt.read_links("links.txt")
    print(links)

if __name__ == "__main__":
    show_links()