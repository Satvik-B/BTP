#!/usr/bin/env python
# coding: utf-8

# In[2]:


import nltk
import docx2txt
from nltk.corpus import stopwords

stopwrds=stopwords.words("english")

def preprocessing(raw):
    wordlist=nltk.word_tokenize(raw)
    text=[w.lower() for w in wordlist if w not in stopwrds]
    return text


jd1= docx2txt.process("JD-CS Agent.docx")
text1=preprocessing(jd1)

import textract
jd2=textract.process("cv.pdf").decode('UTF-8')
text2=preprocessing(jd2)


# In[3]:


from nltk.probability import FreqDist
word_Set=set(text1).union(set(text2))

freqd_text1=FreqDist(text1)
text1_count_dict=dict.fromkeys(word_Set,0)
for word in text1:
    text1_count_dict[word]=freqd_text1[word]
    
freqd_text2=FreqDist(text2)
text2_count_dict=dict.fromkeys(word_Set,0)
for word in text2:
    text2_count_dict[word]=freqd_text2[word]


# In[4]:


freq_text1=FreqDist(text1)
text1_length=len(text1)
text1_tf_dict=dict.fromkeys(word_Set,0)
for word in text1:
    text1_tf_dict[word]=freq_text1[word]/text1_length
    
freq_text2=FreqDist(text2)
text2_length=len(text2)
text2_tf_dict=dict.fromkeys(word_Set,0)
for word in text2:
    text2_tf_dict[word]=freq_text2[word]/text2_length


# In[5]:


text12_idf_dict=dict.fromkeys(word_Set,0)
text12_length = 2
for word in text12_idf_dict.keys():
    if word in text1:
        text12_idf_dict[word]+=1
    if word in text2:
        text12_idf_dict[word]+=1

import math 
for word,val in text12_idf_dict.items():
    text12_idf_dict[word] = 1+ math.log(text12_length/float(val))


# In[6]:


text1_tfidf_dict = dict.fromkeys(word_Set,0)
for word in text1:
    text1_tfidf_dict[word]=(text1_tf_dict[word])*(text12_idf_dict[word])
  
text2_tfidf_dict = dict.fromkeys(word_Set,0)
for word in text2:
    text2_tfidf_dict[word]=(text2_tf_dict[word])*(text12_idf_dict[word])


# In[9]:


v1= list(text1_tfidf_dict.values())
v2= list(text2_tfidf_dict.values())


# In[10]:


similarity = 1- nltk.cluster.cosine_distance(v1,v2)


# In[11]:


print("Similarity: {:4.2f} %".format(similarity*100))

