from concurrent.futures import process
from flask import Flask, request, jsonify
import json
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from flask_sqlalchemy import SQLAlchemy

from pprint import *

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

k=15

api = Flask(__name__)
api.config["JWT_SECRET_KEY"] = "this-is-lenskart-automation-change-it-later"
api.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(api)
api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(api)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))
  name = db.Column(db.String(1000))
  def __repr__(self):
    return '<User {}, {}, {}>'.format(self.name, self.email, self.password)

# with api.app_context():
#     db.create_all()
@api.route('/register', methods=['GET', 'POST'])
def register():
  name=request.json.get("name", None)
  email=request.json.get("email", None)
  password=request.json.get("password", None)
  
  if name==None or email==None or password==None:
    return {"message":"Fill the form again and completely."}
  prev_user = User.query.filter_by(email=email).first()
  if prev_user:
    return {"message":"User already exist."}
  user = User(name=name, email=email, password = password)
  db.session.add(user)
  db.session.commit()
  return {"message":"Registered Successfully"}


@api.route('/users')
def print_users():
  temp=User.query.all()
  for user in temp:
    print(user)
  return {"message":"printed"}

@api.route('/getPdf', methods=['POST'])
def get_pdf():
  if request.files:
    file = request.files['file']
    print(file) 
    file.save('./uploads/'+file.filename)
    import textract 
    txt=textract.process('./uploads/'+file.filename).decode('UTF-8')
    txt=txt.split('.')
    print(type(txt))
    print(txt)
    new_txt=[(len(txt[i]), txt[i], i) for i in range(len(txt))]
    new_txt.sort()
    new_txt.reverse()
    to_highlight=[0]*len(new_txt)
    for i in range(k):
      to_highlight[new_txt[i][2]]=1


    return {'message': 'Evaluated', 
      'txt': txt,
      'highlight':to_highlight
    }
  elif request.form:
    return {'message': 'request has a form'}, 200
  return {'message':'request is empty'}, 200

def process_pdf(name):
  import textract 
  txt=textract.process(name).decode('UTF-8')
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
  text2=preprocessing(txt)

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
  text1_tfidf_dict = dict.fromkeys(word_Set,0)
  for word in text1:
    text1_tfidf_dict[word]=(text1_tf_dict[word])*(text12_idf_dict[word])
    
  text2_tfidf_dict = dict.fromkeys(word_Set,0)
  for word in text2:
    text2_tfidf_dict[word]=(text2_tf_dict[word])*(text12_idf_dict[word])
  v1= list(text1_tfidf_dict.values())
  v2= list(text2_tfidf_dict.values())
  similarity = 1- nltk.cluster.cosine_distance(v1,v2)
  print("Similarity: {:4.2f} %".format(similarity*100))
  return similarity*100


  