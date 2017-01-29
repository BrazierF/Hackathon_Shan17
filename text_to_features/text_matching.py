"""Text matching script.

Usage:
  text_matching.py generate
  text_matching.py loop

"""

from docopt import docopt
from collections import Counter
import numpy as np
import re
import unicodedata
from nltk.stem.snowball import FrenchStemmer
from nltk.tokenize import WordPunctTokenizer
import word2vec
import time
import pickle
import os



def text_cleaning(tweet, stem=False):
    # Removing the 'start', 'end' markers
    t = tweet.replace("<start>", "")
    t = t.replace("<end>\n", "")
    t = t.replace("text:", "")
    # Lowercase
    t = t.lower()
    # Remove accent
    t = strip_accents(t)
    # Remove multiple spaces
    t = re.sub(' +',' ',t)
    # Tokenize
    t = TOKENIZER.tokenize(t)
    # Remove plural, tense
    if stem:
        t = [STEMMER.stem(word) for word in t]
    # Reconstruct
    out = ""
    for word in t:
        out += word + " "
    return out.lower()

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def open_and_read(f, header_length=3):
    with open(f, "r") as f:
        lines = f.readlines()
    header = lines[0:header_length]
    tweets = lines[header_length:]
    return header, tweets

def extract_next_tweet(indice, tweets):
    tweet = tweets[indice]
    indice += 1
    count = 0
    while tweet.find("<end>") < 0 and count < 100:
        tweet += tweets[indice]
        indice += 1
        count += 1
    return tweet, indice

def text_cleaning(tweet, stem=False):
    # Removing the 'start', 'end' markers
    t = tweet.replace("<start>", "")
    t = t.replace("<end>\n", "")
    t = t.replace("text:", "")
    # Lowercase 
    t = t.lower()
    # Remove accent
    t = strip_accents(t)
    # Remove multiple spaces
    t = re.sub(' +',' ',t)
    # Tokenize
    t = TOKENIZER.tokenize(t)
    # Remove plural, tense
    if stem:
        t = [STEMMER.stem(word) for word in t]
    # Reconstruct
    out = ""
    for word in t:
        out += word + " "
    return out.lower()

def open_books():
    book_list = os.listdir("books/")
    books = [open_and_read("books/"+name, 100)[1] for name in book_list]
    books_doc = []
    for book in books:
        for i in range(len(book)/5):
            doc = ""
            for k in range(5):
                doc += text_cleaning(book[5*i+k] + " ")
            books_doc.append(doc)
    return books_doc

def get_list_of_words():
    books = open_books()
    all_stems = []
    all_tokens = []
    all_tokens_name = []
    concat_descriptions = DESCRIPTIONS[:]
    concat_descriptions.extend(books)
    concat_NAMES = NAMES[:]
    concat_NAMES.extend(["book" for i in range(len(books))])
    for name, des in zip(concat_NAMES, concat_descriptions):
        # Cleaning
        clean_text = text_cleaning(des)
        # Tokenize
        tokens = TOKENIZER.tokenize(clean_text)
        # Stemming
        stems = [STEMMER.stem(tok) for tok in tokens]
        # Cleaning
        clean_name = text_cleaning(name)
        # Tokenize
        tokens_name = TOKENIZER.tokenize(clean_name)
        # Stack
        all_stems.append(stems)
        all_tokens.append(tokens)
        all_tokens_name.append(tokens_name)
    return all_stems, all_tokens, all_tokens_name

def get_counters(documents):
    counters = [Counter(doc) for doc in documents]
    sum_per_counters = [np.sum(cnt.values()) for cnt in counters]
    return counters, sum_per_counters

def tf(word, cnt, tot_sum):
    return float(cnt[word]) / tot_sum

def n_containing(word, cnts):
    return float(sum([1 for cnt in cnts if cnt[word] != 0]))

def idf(word, cnts):
    return np.log(len(cnts) / (1 + n_containing(word, cnts)))

def tfidf(word, cnt, tot_sum, cnts):
    return tf(word, cnt, tot_sum) * idf(word, cnts)

def find_original_word(selected_words, tokens):
    out = []
    for word in selected_words:
        for token in tokens:
            if word in token:
                out.append(token)
                break
    return out

def get_features(selected_words):
    all_responses = []
    for words in selected_words:
        responses = []
        for word in words:
            try:
                vector = WORD2VEC.get_vector(word)
                responses.append(vector)
            except:
                pass
        all_responses.append(responses)
    return all_responses

def read_file(path):
    with open(path, "r") as f:
        lines = f.readlines()
    return lines

def write_file(path, ids, scores):
    with open(path, "w") as f:
        for s, id_ in zip(scores, ids):
            f.writelines("%d : %.4f\n"%(id_, s))

if __name__ == '__main__':

    arguments = docopt(__doc__, version='0.1')
    print(arguments)

    TOKENIZER = WordPunctTokenizer()
    STEMMER = FrenchStemmer()
    WORD2VEC = word2vec.load('frWac_non_lem_no_postag_no_phrase_200_cbow_cut100.bin')

    with open("db.pkl", "r") as f:
        res = pickle.load(f)

    IDS = [r[0] for r in res]
    NAMES = [r[2] for r in res]
    TYPE = [r[1] for r in res]
    TAGS = [r[3] for r in res]
    GOOGLE_SCORES = [r[4] for r in res]

    NAMES = [id_ for j,id_ in enumerate(NAMES) if TAGS[j] is not None]
    TYPE = [id_ for j,id_ in enumerate(TYPE) if TAGS[j] is not None]
    TAGS = [t for j,t in enumerate(TAGS) if TAGS[j] is not None]

    TAGS = [unicodedata.normalize('NFKD', t).encode('ascii','ignore') for t in TAGS]
    TYPE = [unicodedata.normalize('NFKD', t).encode('ascii','ignore') for t in TYPE]
    NAMES = [unicodedata.normalize('NFKD', t).encode('ascii','ignore') for t in NAMES]

    DESCRIPTIONS = [text_cleaning(id_) + " " + text_cleaning(type_) + " " + text_cleaning(tag)
                for id_, type_, tag in zip(NAMES, TYPE, TAGS)]

    if arguments["generate"]:
        # Tokenize each description
        stemmed_descriptions, tokenized_descriptions, tokenized_names = get_list_of_words()
        # Pre-compute statistics
        counters, sum_per_counters = get_counters(tokenized_descriptions)
        with open("counters.pkl", "w") as f:
            pickle.dump([counters, sum_per_counters], f)
        # Select few words per ID
        K = 10
        selected_words = []
        for i in range(len(DESCRIPTIONS)):
            tfidf_ = [tfidf(w, counters[i], sum_per_counters[i], counters) for w in stemmed_descriptions[i]]
            index = np.argsort(tfidf_)[-K:]
            words_of_interest = [stemmed_descriptions[i][k] for k in index]
            final_words = list(set(find_original_word(words_of_interest, tokenized_descriptions[i]) + tokenized_names[i]))
            selected_words.append(final_words)

            # Get features for each ID
            all_responses = get_features(selected_words)

            np.save("features_description.npy", all_responses)

    else:
        K = 10

        with open("counters.pkl", "r") as f:
            counters, sum_per_counters = pickle.load(f)
        all_responses = np.load("features_description.npy")

        while True:
            query_file = os.listdir("queries/")
            if query_file:
                time.sleep(0.25)
                # Read file
                queries = read_file("queries/"+query_file[0])
                os.remove("queries/"+query_file[0])
                for count, QUERY in enumerate(queries):
                    cleaned_query = text_cleaning(QUERY)
                    # Tokenize
                    tokens_query = TOKENIZER.tokenize(cleaned_query)
                    # Stemming
                    #stems_query = [STEMMER.stem(tok) for tok in tokens_query]
                    # TF IDF
                    #if False:
                    #    cnt_query = Counter(stems_query)
                    #    tfidf_query = [tfidf(w, cnt_query, np.sum(cnt_query.values()), counters) for w in stems_query]
                    #    index_query = np.argsort(tfidf_query)[-K:]
                    #    words_of_interest_query = [stems_query[k] for k in index_query]
                    #    final_words_query = list(set(find_original_word(words_of_interest_query, tokens_query)))
                    #    print final_words_query
                    # Features
                    features_query = get_features([tokens_query])[0]
                    end = time.time()

                    feat_query = np.mean(features_query, axis=0)

                    correlation_scores = np.array([np.mean([np.corrcoef(feat_description, feat_query)[0,1] for feat_description in responses])
                                                   for responses in all_responses])
                    topsort = np.argsort(correlation_scores)
                    matches = [(NAMES[k], correlation_scores[k]) for k in topsort[::-1]]

                    for match in matches:
                        print QUERY, ":\t\t", match[0][0:15], "\t%.4f"%match[1]
                    print "\n"
                    write_file("scores/out_%d.txt"%count, IDS, correlation_scores)
            else:
                print "Waiting..."
                time.sleep(1)


	
