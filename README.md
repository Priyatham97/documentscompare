# Comparing two Documents for similiarities

#### Environment Used - Python 3.42 , NLTK

#### Algorithm Used - TD-IDF 

#### Idea - The idea used here is to convert the words in each document into corresponding vectors (i.e, tdidf vectors) and the cosine between them gives the degree of similiarity between them.



Tf-idf stands for term frequency-inverse document frequency, and the tf-idf weight is a weight often used in information retrieval and text mining. This weight is a statistical measure used to evaluate how important a word is to a document in a collection or corpus. The importance increases proportionally to the number of times a word appears in the document but is offset by the frequency of the word in the corpus. 

TF: Term Frequency, which measures how frequently a term occurs in a document. Since every document is different in length, it is possible that a term would appear much more times in long documents than shorter ones. Thus, the term frequency is often divided by the document length (the total number of terms in the document) as a way of normalization: 

TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).

IDF: Inverse Document Frequency, which measures how important a term is. While computing TF, all terms are considered equally important. However it is known that certain terms, such as "is", "of", and "that", may appear a lot of times but have little importance. Thus we need to weigh down the frequent terms while scale up the rare ones, by computing the following: 

IDF(t) = 1+log_e(Total number of documents / Number of documents with term t in it).

For more Details - Wiki page https://en.wikipedia.org/wiki/Tf%E2%80%93idf

So Code Approach is as follows - 

The files to be compared are stored in directory named as 'resumes' and are stored as strings in a list.
```
#Reading files into a dictionary 
for filename in os.listdir(corpus_root):
    file = open(os.path.join(corpus_root, filename), 'r',encoding="utf8")
    filetext = file.read()
    corpus[filename] = str(filetext)
```
Then they are tokenised and stemmed using the modules provided by NLTK for the same.
```
for filename in corpus:
    filetext = corpus[filename]
    
    terms = tokenizer.tokenize(filetext)
    terms = [term.lower() for term in terms]
    terms = [term for term in terms if term not in stopwords] 
    terms = [stemmer.stem(term) for term in terms]

    tf_dict[filename] = {}    
    tf_dict[filename] = Counter(terms)
```
Now, IDF of each term is determined using the definition mentioned above.
```
for filename in tf_dict:
    for word in tf_dict[filename]:
        count = 0
        try:
            for file in temp:
                if word in temp[file]:
                    count = count + 1 
        idf_dict[word] = 1+math.log10(len(tf_dict) / float(count))
```
The idea here is to convert the words in each document into corresponding vectors (i.e, tdidf vectors) and the cosine between them gives the degree of similiarity between them.So two functions for getting tdidf vectors and calculating cosine are defined and implemented as follows-
```
def gettfidfvec(filename):
    tf_wt = {}
    tf_idf_file = {}
    for term in tf_dict[filename]:
        tf_term = tf_dict[filename][term]
        tf_wt[term] = tf_term
        tf_idf_file[term] = tf_wt[term] * idf_dict[term]       
    d = 0
    for term in tf_idf_file:
        d = d + pow(tf_idf_file[term], 2)
   
    normd = math.sqrt(d)
        
    tfidfvec = {}
    for term in tf_idf_file:
        tfidfvec[term] = tf_idf_file[term]/normd 
          
    return tfidfvec
    
def docdocsim(filename1, filename2):
    cosine = 0
    tfidf_f1 = gettfidfvec(filename1)
    tfidf_f2 = gettfidfvec(filename2)
    common = set(tfidf_f1) & set(tfidf_f2)
    a = ' '
    for word in common:
        try:
            cosine = cosine + (tfidf_f1[word] * tfidf_f2[word])
         except KeyError:
            a = a + ' '
     print(cosine)

```
#### Implemented by Priyatham Katta.
