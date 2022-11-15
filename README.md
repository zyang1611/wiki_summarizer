# Wikipedia Summarizer
#### Video Demo:  <https://youtu.be/6CwQeA8eXGY>
#### Description:
##### **Introduction**
As my final project submission for CS50, I've built a web based Wikipedia summarizer using Python, html and css. The webpage accepts as user input a link to a Wikipedia page and display a 10 sentence summary of the page's content. This webpage relies on nltk and BeautifulSoup libraries to implement certain functions further described below. 
##### **textfunctions.py**
This file handles the core function of the webpage as follows. 
1. Fetch and Parse Page Content
- After fetching the html content from the given url, the BeautifulSoup library is used to parse the content and extract out only the text data from all \<p> tags and the page title. 
2. Preprocess Text Data
- Text data is separated in to sentences using the nltk.sent_tokenize().
- Each sentence is separated in to a list of its tokens. 
- All tokens are lowercased.
- Punctuation, stopwords, digits and any words that are not nouns or verbs as tagged by nltk.pos_tag() are removed from the list of tokens.
3. Rank Sentences
- Sentences are scored and sorted based on the word probabilities of its tokens. The top 9 sentences with the highest scores are then combined with the first sentence appearing on the Wiki page to form a 10 sentence summary. This is because the first sentence on a Wiki page in most cases provides a good representation of the topic. 
4. Method for Ranking Sentences
- In this ranking system, a simplification of the SumBasic system [1] is used to rank sentences where the word probabilities are not updated after each sentence selection.
- The word frequencies of all tokens in the text data are first calculated. The score of each sentence is then calculated as the sum of the word frequencies of its tokens divided by the number of tokens in the sentence. 
- >Sentence Score = Sum(W<sub>f</sub> of all tokens) / Number of tokens
- 3 ranking systems were tested for this webpage. The simplified system, SumBasic system and a TFIDF system. 
- Testing showed that when compred to the SumBasic system, the simplified system produced the best short summary for a Wikipedia page. Because word probabilities are not updated, this system was less likely to include "hanging" sentences that made less sense without its accompanying paragraph for context. This was more appropriate to summarize Wikipedia page that could have multiple sections with widely varying sub topics. 
- Both the simplified system and the Sumbasic system produced better results than the TFIDF system. 
##### **app.py**
This file handles the local server for the webpage using the Flask library. Functions defined in textfunctions.py are imported and run here to get the page summary.
##### **index.html, result.html and style.css**
These files handle the display and styling for the webpage utilizing the Bootstrap framework. 
#### References
[1] Nenkova, Ani & Vanderwende, Lucy. (2005). The impact of frequency on summarization. 
[2] Allahyari, Mehdi & Pouriyeh, Seyedamin & Assefi, Mehdi & Safaei, Saeid & Trippe, Elizabeth & Gutierrez, Juan & Kochut, Krys. (2017). Text Summarization Techniques: A Brief Survey. International Journal of Advanced Computer Science and Applications (IJACSA). 8. 397-405. 10.14569/IJACSA.2017.081052. 