# """A Markov chain generator that can tweet random messages."""

# import os
# import sys
# from random import choice
# import twitter


# def open_and_read_file(filenames):
#     """Take list of files. Open them, read them, and return one long string."""

#     body = ""

#     for filename in filenames:
#         text_file = open(filename)
#         body = body + text_file.read()
#         text_file.close()

#     return body


# def make_chains(text_string):
#     """Take input text as string; return dictionary of Markov chains."""

#     chains = {}

#     words = text_string.split()

#     for i in range(len(words) - 2):
#         key = (words[i], words[i + 1])
#         value = words[i + 2]

#         if key not in chains:
#             chains[key] = []

#         chains[key].append(value)

#         # or we could replace the last three lines with:
#         #    chains.setdefault(key, []).append(value)

#     return chains


# def make_text(chains):
#     """Take dictionary of Markov chains; return random text."""

#     key = choice(chains.keys())
#     words = [key[0], key[1]]
#     while key in chains:
#         # Keep looping until we have a key that isn't in the chains
#         # (which would mean it was the end of our original text).
#         #
#         # Note that for long texts (like a full book), this might mean
#         # it would run for a very long time.

#         word = choice(chains[key])
#         words.append(word)
#         key = (key[1], word)

#     return " ".join(words)


# def tweet(chains):
#     """Create a tweet and send it to the Internet."""

#     # Use Python os.environ to get at environmental variables
#     # Note: you must run `source secrets.sh` before running this file
#     # to make sure these environmental variables are set.

#     pass


# # Get the filenames from the user through a command line prompt, ex:
# # python markov.py green-eggs.txt shakespeare.txt
# filenames = sys.argv[1:]

# # Open the files and turn them into one long string
# text = open_and_read_file(filenames)

# # Get a Markov chain
# chains = make_chains(text)

# # Your task is to write a new function tweet, that will take chains as input
# # tweet(chains)

"""Generate Markov text from text files."""

from random import choice
import twitter
import os

def open_and_read_file(file_path):
    """Take file path as string; return text as string.
    
    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    read_file = open(file_path).read()

    return read_file


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """
    words = text_string.split()

    chains = {}

    for i in range(len(words) - 1):
     
        new_tuple = tuple([words[i], words[i+1]])
     
        if new_tuple in chains:
            if new_tuple == tuple([words[-2], words[-1]]):
                chains[new_tuple] = None
                break
            chains[new_tuple].append(words[i+2])
        else:
            if new_tuple == tuple([words[-2], words[-1]]):
                chains[new_tuple] = None
                break
            chains[new_tuple] = [words[i+2]]

    #print(chains)

    return chains


def make_text(chains):
    """Return text from chains."""
    import random

    words = []

    random_tuple = random.choice(list(chains.keys()))

    while chains[random_tuple] != None:
        words.append(random_tuple[0])
        chosen_value = random.choice(chains[random_tuple])
        random_tuple = (random_tuple[1], chosen_value)
    
    words.extend(random_tuple)

    random_text = " ".join(words)
    random_text = random_text[:141]
    # print(random_text)
    
    return random_text

    #we want to pick a random key from the dict that is a tuple, so we know where to start
#from tuple, add index[0] to a list, then use index[1] and value to make a "new tuple"
#value should be "random"
#use that new tuple to find the next tuple randomly and do the same thing, adding index [0] to list
#using index[1] to find the next tuple

#will end when hits "None," so length of randomly generated list  will vary
#hint: while loop? ask for clarification if needed

  

def send_tweet(chains):

    chains = make_text(chains)

    api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                      consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                      access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                      access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
    # print(api)
    status = api.PostUpdate(chains)
    print(status.text)


# input_path = "green-eggs.txt"
input_path = "song-philosophy-mashup.txt"

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)
# print(chains)

# Produce random text
send_tweet(chains)


