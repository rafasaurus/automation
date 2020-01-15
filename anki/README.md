### Generating Anki Cards

ls folder/[0-9]*.txt | xargs -L1 ./create_anki.py -t

### For the debug mode 

ls folder/[0-9]*.txt | xargs -L1 ./create_anki.py -d 0 -t

### For getting statistics

ls ../../folder/* | xargs -L1 ../../create_anki.py  -t | awk '{print $1 "," $2 "," $3 "," $4 "," $5}'


### convert doc to txt

soffice --headless --convert-to txt:Text *.doc

