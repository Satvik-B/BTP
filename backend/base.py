from concurrent.futures import process
from flask import Flask, request, jsonify
import json
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from flask_sqlalchemy import SQLAlchemy
from lexrank import LexRank
from lexrank.mappings.stopwords import STOPWORDS
from path import Path


documents = None
lexrank = None

from pprint import *

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

api = Flask(__name__)
# api.config["JWT_SECRET_KEY"] = "this-is-lenskart-automation-change-it-later"
# api.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# jwt = JWTManager(api)
# api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(api)



# class User(db.Model):
#   id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
#   email = db.Column(db.String(100), unique=True)
#   password = db.Column(db.String(100))
#   name = db.Column(db.String(1000))
#   def __repr__(self):
#     return '<User {}, {}, {}>'.format(self.name, self.email, self.password)

# with api.app_context():
#     db.create_all()
# @api.route('/register', methods=['GET', 'POST'])
# def register():
#   name=request.json.get("name", None)
#   email=request.json.get("email", None)
#   password=request.json.get("password", None)
  
#   if name==None or email==None or password==None:
#     return {"message":"Fill the form again and completely."}
#   prev_user = User.query.filter_by(email=email).first()
#   if prev_user:
#     return {"message":"User already exist."}
#   user = User(name=name, email=email, password = password)
#   db.session.add(user)
#   db.session.commit()
#   return {"message":"Registered Successfully"}


# @api.route('/users')
# def print_users():
#   temp=User.query.all()
#   for user in temp:
#     print(user)
#   return {"message":"printed"}

@api.route('/getPdf', methods=['POST'])
def get_pdf():
  if request.files:
    file = request.files['file']
    print(file) 
    file.save('./uploads/'+file.filename)
    
    import textract 
    
    txt=textract.process('./uploads/'+file.filename).decode('UTF-8')
        
    sentences=get_sentences(txt)
    to_highlight=process_sentences(sentences)
    
    import os
    os.remove('./uploads/'+file.filename)
    
    return {'message': 'Evaluated', 
      'txt': sentences,
      'highlight':to_highlight
    }
  elif request.form:
    return {'message': 'request has a form'}, 200
  return {'message':'request is empty'}, 200

def get_sentences(text):
  sentences = []
  txt = text.replace("\n  \n", "\n\n")
  temp = txt.split('\n\n')
  for para in temp:
    para=para.strip()
    para = para.split('.')
    for i in range(len(para)):
      if len(para[i])!=0:
        para[i]=para[i]+". "
      sentences.append(para[i])
    sentences.append("\n\n")
  return sentences
  
def process_sentences(sentences):
  count=0
  for line in sentences:
    if len(line)!=0 and line!="\n\n":
      count+=1
  k = (int)(0.1*count)
  global documents
  global lexrank
  if documents == None:
    documents_dir = Path('./training')
    documents = []
    for file_path in documents_dir.files('*.txt'):
      with file_path.open(mode='rt', encoding='utf-8') as f:
        line = [f1.split('\t')[0] for f1 in f.readlines()]
        documents.append(line)
    lexrank = LexRank(documents, stopwords=STOPWORDS)
  scores_cont = lexrank.rank_sentences(sentences, threshold = None, fast_power_method=True)
  new_txt=[(scores_cont[i], sentences[i], i) for i in range(len(sentences))]
  new_txt.sort()
  new_txt.reverse()
  to_highlight=[0]*len(new_txt)
  for i in range(k):
    to_highlight[new_txt[i][2]]=1
  return to_highlight