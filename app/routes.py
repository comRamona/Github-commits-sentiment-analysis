import requests
import json
import nltk
import random
import pandas as pd
import numpy as np
from numpy import pi
import sentiments
import bokeh.plotting as bk
from bokeh.embed import autoload_server
from bokeh.document import Document
from bokeh.resources import CDN
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.io import output_file, show
from collections import OrderedDict
from bokeh.charts import Bar, output_file, show
import numpy as np
from alchemyapi import AlchemyAPI
from flask import Flask, render_template, request, jsonify
from forms import LoginForm
from flask_bootstrap import Bootstrap

def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
                           title='Sign In',
                           form=form)

@app.route('/commits', methods=['POST'])
def hello():
    name=request.form['name']
    url2="https://api.github.com/users/"+name+"/repos"
    ram='comRamona'
    #auth=(ram,auth)
    repos = requests.get(url2).json()
    words=""
    tokens=[]
    forbidden=["merge","and","for","from","in","of","pull","request","the","to","__init__","commit","for","html"]
    for repo in repos:
        x=repo['name']
    for repo in repos:
        repo_name=repo['name']
        commit_url="https://api.github.com/repos/"+name+"/"+repo_name+"/commits"
        all=requests.get(commit_url).json()
        for a in all:
            if(type(a) is dict):
                x=str(a['commit']['message'])
                y=nltk.tokenize.regexp_tokenize(x, r'\w+')
                tokens+=y
                words=words+" ".join(y)
    res=""
    score="0"
    tokens = [token.lower() for token in tokens if len(token)>2 and token not in forbidden]
    freq= nltk.FreqDist(tokens).most_common(10)

    xs=[]
    ys=[]
    for (a,b) in freq:
        xs.append(a)
        ys.append(b)
    di = {'values':ys, 'names': xs}
    df = pd.DataFrame(di)
    qq={'a':2}
    output_file("tutorial_sharing.html")
    plot = Bar(df,'names', values='values', title="test chart",xlabel="Words", ylabel="Frequency")
    alchemyapi = AlchemyAPI()
    response = alchemyapi.sentiment('text', words)
    if response['status'] == 'OK':
        res=response['docSentiment']['type']

    if 'score' in response['docSentiment']:
        score=response['docSentiment']['score']
    script, div = components(plot)
    return render_template('commits.html', script=script, div=div,score=score,res=res,name=name)


if __name__ == '__main__':
    app.run(debug=True)