import requests as req
import nltk
import string
import math
import re
from bs4 import BeautifulSoup as BS

def get_sentences(url):
    """
    Returns a summary of a Wikipedia page given its URL.
    """
    # Ensure relevant nltk packages are downloaded.
    nltk.download("wordnet")
    nltk.download("averaged_perceptron_tagger")

    if not url:
        print("Error: Must input page url")

    # Get Wikipedia page html
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'
    }
    response = req.get(url, headers=headers)

    # Parse html to extract page title and text content
    def p_no_coordinates(tag):
        return tag.name == "p" and not tag.find_all(id="coordinates")
    soup = BS(response.content, "html.parser")
    htmltext = soup.find(id="mw-content-text").find(class_="mw-parser-output").find_all(p_no_coordinates, recursive=False)
    
    if not htmltext:
        print("parser error")
        return 
    
    title = soup.title.string
    passage_list = []
    [passage_list.append(line.text.rstrip()) for line in htmltext]

    # Extract and preprocess sentences from text 
    sentences = {}
    raw_sents = {}
    for passage in passage_list:
        for sentence in nltk.sent_tokenize(passage):
            tokens = tokenize(sentence)
            if tokens:
                sentences[sentence[:15]] = tokens # key: list of tokens
                raw_sents[sentence[:15]] = sentence # key: sentence string

    # Get a summary of the text
    scores = compute_score(sentences)
    return title, summary(10, scores, raw_sents)

def summary(n, scores, raw_sents):
    """
    Return a summary of the text given a dict of sentence keys mapped to their frequency scores and another dict of sentence keys mapped to the full sentence.
    """
    # Append first sentence to result.
    result = ""
    first_sent = next(iter(scores))
    result += re.sub("\[+[^\s]+", "",raw_sents[first_sent])
    scores.pop(first_sent)

    # Sort sentences according to their average tf-idf values
    scores = {k: v for k, v in sorted(scores.items(), key=lambda x: x[1], reverse=True)}

    # Select top sentences that have average tf-idf values above threshold value.
    count = 0
    for sent in scores:
        sentence = re.sub("\[+[^\s]+", "", raw_sents[sent]) # Remove [XX]
        result += " " + sentence
        count += 1
        if count == n-1:
            return result

def compute_score(sentences):
    """
    Calculate the scores for all sentences.
    """
    words = {}
    lemm = nltk.stem.WordNetLemmatizer() 
    sentences = {k: [lemm.lemmatize(word) for word in v] for k, v in sentences.items()}

    # Calculate word frequencies.
    for list in sentences.values():
        for word in list:
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
                
    # Calculate sentence scores.
    scores = {}
    for sentence in sentences:
        wordlist = sentences[sentence]
        sent_sum = 0
        for word in wordlist:
            if word in words:
                sent_sum += words[word]
        scores[sentence] = sent_sum / len(wordlist)
    return scores

def tokenize(sentence):
    """
    Process document by coverting a list of all words to lowercase, and removing any punctuation, stopwords and digits. Any words that are not nouns or verbs are also removed.
    """
    # Lowercase all words.
    words = nltk.word_tokenize(sentence)
    words = [word.lower() for word in words]
    stop_words = set(nltk.corpus.stopwords.words("english"))
    
    # Remove punctuation and stopwords.
    for word in words.copy():
        if word in string.punctuation:
            words.remove(word)
            continue
        elif word in stop_words:
            words.remove(word)
            continue
        elif word.isdigit():
            words.remove(word)
            
    # Remove all words that are not nouns or verbs
    tags = ("NN", "NNP", "NNS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ")
    tagged_words = nltk.pos_tag(words)
    for word, tag in tagged_words:
        if tag not in tags:
            words.remove(word)
    return words
