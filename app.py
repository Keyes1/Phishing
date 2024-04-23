from flask import Flask, render_template, request
import google.generativeai as genai
import os
from feature_extract import pred,extract_links
model = genai.GenerativeModel('gemini-pro')

my_api_key_gemini = 'AIzaSyAmulpvGbEpbEISbq_VwhpqZYUfs2pHq8k'

genai.configure(api_key=my_api_key_gemini)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/link_check')
def link_check():
    return render_template('link_check.html')

@app.route('/link_results', methods=['POST'])
def link_results():
    site_url = request.form['site_url']
    site_functionality = request.form['site_functionality']
    # Call your function to generate alternate links
    #links = generate_links(site_url, site_functionality)
    links=["www.fb.com"]
    label = "Alternate links for {} ({})".format(site_url, site_functionality)
    return render_template('link_results.html', links=links, label=label)

@app.route('/quiz')
def quiz():
    question = "What is the capital of France?"
    options = ["Paris", "London", "Berlin", "Madrid"]
    return render_template('quiz.html', question=question, options=options)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    # Handle the submitted answer
    pass


if __name__ == '__main__':
    app.run(debug=True)