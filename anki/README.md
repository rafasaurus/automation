### Generating Anki Cards

ls folder/[0-9]*.txt | xargs -L1 ./create_anki.py -t

for the debug mode 

ls folder/[0-9]*.txt | xargs -L1 ./create_anki.py -d 0 -t
