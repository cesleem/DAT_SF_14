import sys
import string

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove punctuation
    for c in string.punctuation:
        line = line.replace(c," ")
    # remove leading and trailing whitespace 
    line = line.strip()
    # split the line into words
    # extremly naive tokenization: can you improve?
    words = line.split()
    # increase counters
    for word in words:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        print '%s\t%s' % (word.lower(), 1)