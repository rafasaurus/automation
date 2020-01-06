#!/usr/bin/python
import genanki
from pathlib import Path
import regex as re
# import re
from easygui import codebox
import tkinter as tk
import pymsgbox
from contextlib import contextmanager

import csv
import os, fnmatch
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--txt", type=str,
	help="txt file", required=True)
parser.add_argument("-d", "--debug", type=bool,
	help="print debug info, example -> [-d 0]", required=False)
args = vars(parser.parse_args())

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

### get the all answers
try:
    def getRightAnswers(file):
        with open(Path(file), encoding="utf8", errors='ignore') as f:
            contents = f.read()
            matches = re.search(r"(Right answer)[Ա-ֆա-ֆA-Za-z\n\d\.]+", contents)
            assert(matches)
            return matches[0]


    txtFile = None

    if args.get("txt", False):
        txtFile = args.get("txt")
        txtFileName = os.path.basename(txtFile)
        # print(txtFileName)
        rightAnswers=getRightAnswers(txtFile)

    my_deck = genanki.Deck(
        2059400110,
        txtFileName)

    def getAnswer(n):
        global rightAnswers
        answer = None
        matches = re.search(r"(" + str(n) + ")\.(?P<name>[Ա-ֆա-ֆ])", rightAnswers)
        assert(matches)
        return matches

    with open(Path(txtFile), encoding="utf8", errors='ignore') as f:
        contents = f.read()
        n = 0
        for frage in re.split(r"\d\.\d\/", contents):
            # skip the first intro stuff, it is specific for the task
            if n == 0:
                n+=1
                continue
            frage = "\n\n\n\n0.0/" + str(n) + frage
            back = getAnswer(n);
            front = re.findall(r"\d.\d/(?P<name>[Ա-ֆա-ֆA-Za-z.\-\`\,\/\n …….–և\d\.\+\)]+)\n\n", frage, overlapped=True)
            assert(back)
            assert(front)
            if len(back) != 0:
                # print("back:", back[0])
                pass
            else:
                continue
            if len(front) != 0:
                # print("front:", front[0])
                pass
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
                fields=[front, back.replace("\n", "<br>")])
            my_deck.add_note(my_note)
            # print(back.replace("\n", "<br>"))
            # with tk(timeout=1.5):
            #   codebox("Contents of file " + filename, "Show File Contents", text)
            # pymsgbox.native.alert(back, front)
            # if(n>15):
            #   print("Frage: ", front, "\n\nAntwort: ", back)
        genanki.Package(my_deck).write_to_file(txtFileName + ".apkg")
        print("DONE EXPORTING " + txtFileName + ".apkg")
except AssertionError as error:
    print("ERROR: " + txtFile + ":")
    if args.get("debug", False):
        print("DEBUG INFO\n\t" +error)
