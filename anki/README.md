### regex checker [used](https://pythex.org/)

### Generating Anki Cards

ls folder/[0-9]*.txt | xargs -L1 ./create_anki.py -t

### For the debug mode 

ls folder/[0-9]*.txt | xargs -L1 ./create_anki.py -d 0 -t

very difficult to find regex match for multiple "tests"

"""
    s/^\d\{1,2}\s[^\.]/0.0\//g
"""

todo

data_0 [+]
data_1 [-]
data_2 [+]
