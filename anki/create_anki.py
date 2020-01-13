#!/usr/bin/python
from pathlib import Path
import regex as re
import os
import argparse
import genanki
# import pymsgbox
# import tkinter as tk
# from easygui import codebox

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--txt", type=str,
    help="txt file", required=True)
parser.add_argument("-d", "--debug", type=bool,
    help="print debug info, example -> [-d 0]", required=False)
parser.add_argument("-te", "--test", type=bool,
    help="activate Test mode !! -> [-te if 1, then test mode is activated, else not activated", required=False)
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

counter_a = 0
counter_b = 0
counter_g = 0
counter_d = 0
global_counter = 0 

try:
    def getRightAnswers(file):
        with open(Path(file), encoding="utf8", errors='ignore') as f:
            contents = f.read()
            matches = re.search(r"(Right answer)[Ա-ֆա-ֆA-Za-z\n\d\.\ \)]+", contents)
            assert(matches)
            return matches[0]

    txtFile = None

    if args.get("txt", False):
        txtFile = args.get("txt")
        txtFileName = os.path.basename(txtFile)
        # print(txtFileName)
        rightAnswers=getRightAnswers(txtFile)
        # print("************************* debug rightAnswer ****************", rightAnswers)

    my_deck = genanki.Deck(
        2059400110,
        txtFileName)

    def getAnswer(n):
        global rightAnswers
        answer = None
        matches = re.search(r"(" + str(n) + ")\. (?P<name>[Ա-ֆա-ֆ])\)", rightAnswers)
        # print("************************* debug ****************", matches)
        assert(matches)
        return matches

    with open(Path(txtFile), encoding="utf8", errors='ignore') as f:
        contents = f.read()
        numberOfAnswers = 0
        for frage in re.split(r"\d\.\d\/", contents):
            # skip the first intro stuff, it is specific for the task
            if numberOfAnswers == 0:
                numberOfAnswers+=1
                continue
            frage = "\n\n\n\n0.0/" + str(numberOfAnswers) + frage
            # print("********************* frage *****************", frage)
            back = getAnswer(numberOfAnswers);
            front = re.findall(r"\d.\d/(?P<name>[Ա-ֆա-ֆA-Za-z.\-\`\,\/\n …….–և\d\.\+\)]+)\n\n", frage, overlapped=True)
            # print("***************************** front ******************", front)
            front = frage
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
            # front = front[0]
            back = "\n\n\n" + back[0]
            # print(back)
            stat_answer_per_chapter = None 

            find_stat_a = re.findall(r"[ա]", back)
            if find_stat_a:
                counter_a += 1
                global_counter += 1
            find_stat_b = re.findall(r"[բ]", back)
            if find_stat_b:
                counter_b += 1
                global_counter += 1
            find_stat_g = re.findall(r"[գ]", back)
            if find_stat_g:
                counter_g += 1
                global_counter += 1
            find_stat_d = re.findall(r"[դ]", back)
            if find_stat_d:
                counter_d += 1
                global_counter += 1

            front = front.strip()
            numberOfAnswers += 1
            index = 0
            while not(front.endswith(".") or front.endswith("?")
                      or front.endswith(")") or front.endswith(":")) and index<2:
                index += 1
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
            # if(numberOfAnswers>15):
            #   print("Frage: ", front, "\n\nAntwort: ", back)
        genanki.Package(my_deck).write_to_file(txtFileName + ".apkg")

        # print("for test ", txtFileName , " a: ", int(counter_a), "b: ", int(counter_b), "g: ", int(counter_g), "d: ", int(counter_d), "counter: ", global_counter)
        print("", int(counter_a), "", int(counter_b), "", int(counter_g), "", int(counter_d), "", global_counter)
        if args.get("test", False):
            if counter_a/global_counter*100 != 0:
                print("TEST HAS PASSED, CONGRAGTULATIONS !!! yuhu")
            else:
                print("TEST FAILED !!!")

        # print("DONE EXPORTING " + txtFileName + ".apkg")
except AssertionError as error:
    print("ERROR: " + txtFile + ":")
    if args.get("debug", False):
        pass
        # print("DEBUG INFO\n\t" +error)
