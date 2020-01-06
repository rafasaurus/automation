#!/usr/bin/python
import genanki
from pathlib import Path
import regex as re
# import re
from easygui import codebox
import tkinter as tk
import pymsgbox
from contextlib import contextmanager

my_model = genanki.Model(
    1607392319,
    'Simple Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ])

my_deck = genanki.Deck(
    2059400110,
    'test')

### get the all answers
def getRightAnswers(file):
    with open(Path(file), encoding="utf8", errors='ignore') as f:
        contents = f.read()
        matches = re.search(r"(Right answer)[Ա-ֆա-ֆA-Za-z\n\d\.]+", contents)
        assert(matches)
        return matches[0]
rightAnswer=getRightAnswers('Raf/13_1________________________________________________________________________________________.DOC.txt')

def getAnswer(n):
    global rightAnswer
    answer = None
    # toMatch = "[" + str(n) + "].\[ա֊ֆ]"
    matches = re.search(r"(" + str(n) + ")\.(?P<name>[Ա-ֆա-ֆ])", rightAnswer)
    # print("getAnswer ----- ",matches)
    # matches = re.search(r"(24)\.(?P<name>[Ա-ֆա-ֆ])", rightAnswer)
    print("getAnswer ----- ",matches)
    return matches

    

with open(Path('Raf/13_1________________________________________________________________________________________.DOC.txt'), encoding="utf8", errors='ignore') as f:
    # contents = Path('IT-Sicherheit-Fragen-TINF15AIBC.txt').read_text()
    contents = f.read()
    n = 0
    for frage in re.split(r"\d\.\d\/", contents):
        if n == 0:
            n+=1
            continue
        frage = "\n\n\n\n0.0/" + str(n) + frage
        print(frage)
        back = getAnswer(n);
        # front matches                                         "\d.\d/(?P<name>[Ա-ֆա-ֆA-Za-z.\-\`\,\/\n …….–և]+)"
        # midle part, the end part with abgd                    "\d\.(?P<name>[Ա-ֆա-ֆA-Za-z.\-\`\,\/\n …….–և]+)"
        # end part with middle part                             "\d.\d/(?P<name>[Ա-ֆա-ֆA-Za-z.\-\`\,\/\n …….–և\d\.]+)"
        # get the right answer fage                             "(Right answer)[Ա-ֆա-ֆA-Za-z.\-\`\,\/\n …….–և\d\.]+"

        front = re.findall(r"\d.\d/(?P<name>[Ա-ֆա-ֆA-Za-z.\-\`\,\/\n …….–և\d\.\+\)]+)\n\n", frage, overlapped=True)
        if len(back) != 0:
            # print("back>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", back[0])
            # print("back \ncount>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", n)
            print()
        else:
            continue
        if len(front) != 0:
            print()
            # print("front>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", front[0])
        else:
            continue
        front = front[0]
        back = "\n\n\n" + back[0]
        front = front.strip()
        n += 1
        i = 0
        while not(front.endswith(".") or front.endswith("?")
                  or front.endswith(")") or front.endswith(":")) and i<2:
            i += 1
            newfront, back = back.split("\n", 1)
            front += newfront
        if front.startswith("- "):
            front = front[2:]
        my_note = genanki.Note(
            model=my_model,
            fields=[front, back.replace("\n","<br>")])
        my_deck.add_note(my_note)
        # print(back.replace("\n", "<br>"))

        #with tk(timeout=1.5):
         #   codebox("Contents of file " + filename, "Show File Contents", text)
        #pymsgbox.native.alert(back, front)
        #if(n>15):
         #   print("Frage: ", front, "\n\nAntwort: ", back)
    genanki.Package(my_deck).write_to_file('test.apkg')
