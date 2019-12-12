import genanki
from pathlib import Path
import re
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
with open(Path('test.txt'), encoding="utf8", errors='ignore') as f:
    # contents = Path('IT-Sicherheit-Fragen-TINF15AIBC.txt').read_text()
    contents = f.read()
    n = 0
    for frage in re.split(r"\d\.\d\/", contents):
        frage = "\n\n\n\n0.0/" + frage
        back = re.findall(r"\n\ա\)\S*\s*\n\բ\)\S*\s*\n\գ\)\S*\s*\n\դ\)\S*\s*", frage)
        front = re.findall(r"\d\.\d\/(?P<name>[Ա-ֆա-ֆ\s\-\d\`\,\/\n .]+)\n\n", frage)
        if len(back) is not 0:
            print("back>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", back[0])
        else:
            continue
        if len(front) is not 0:
            print("front>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", front[0])
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
