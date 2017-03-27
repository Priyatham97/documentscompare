import os, math
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter

corpus_root = 'resumes'
stopwords = stopwords.words('english')
stopwords.sort()
corpus = {}
tf_dict = {}
idf_dict = {}
tokenizer = RegexpTokenizer(r'[a-zA-Z0-9]+')
stemmer = PorterStemmer()

#Reading files into a dictionary 
for filename in os.listdir(corpus_root):
    file = open(os.path.join(corpus_root, filename), 'r',encoding="utf8")
    filetext = file.read()
    corpus[filename] = str(filetext)

#Tokenizing, Stemming and TF
for filename in corpus:
    filetext = corpus[filename]
    
    terms = tokenizer.tokenize(filetext)
    terms = [term.lower() for term in terms]
    terms = [term for term in terms if term not in stopwords] 
    terms = [stemmer.stem(term) for term in terms]

    tf_dict[filename] = {}    
    tf_dict[filename] = Counter(terms)
    #print(tf_dict[filename])
    
temp = tf_dict
a = ' '
#Finding IDF of each word
for filename in tf_dict:
    for word in tf_dict[filename]:
        count = 0
        try:
            for file in temp:
                if word in temp[file]:
                    count = count + 1 

        except KeyError:
            a = a + word
        # print(word)
        # print(count)  
        idf_dict[word] = 1+math.log10(len(tf_dict) / float(count))
        # print(idf_dict[word])

def gettfidfvec(filename):
    tf_wt = {}
    tf_idf_file = {}
    for term in tf_dict[filename]:
        tf_term = tf_dict[filename][term]
        tf_wt[term] = tf_term
        tf_idf_file[term] = tf_wt[term] * idf_dict[term]
        #print(len(tf_dict[filename]))
        #print(term)
        #print(tf_idf_file[term])
        
    d = 0
    for term in tf_idf_file:
        d = d + pow(tf_idf_file[term], 2)
    
    normd = math.sqrt(d)
        
    tfidfvec = {}
    for term in tf_idf_file:
        tfidfvec[term] = tf_idf_file[term]/normd 
          
    return tfidfvec
#print(gettfidfvec("a.txt"))
#print(gettfidfvec("b.txt"))

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


print(docdocsim("a.txt", "b.txt"))
