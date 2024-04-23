from flask import Flask, render_template, request
import google.generativeai as genai
import os
from feature_extract import pred,extract_links
model = genai.GenerativeModel('gemini-pro')

my_api_key_gemini = 'AIzaSyAmulpvGbEpbEISbq_VwhpqZYUfs2pHq8k'

genai.configure(api_key=my_api_key_gemini)
'''
def  recommendation():
    user_url = request.form.get("url")
    user_need = request.form.get("need")
    prediction=pred(user_url)
    try:
        query = "Give me alternate websites to use for "+user_need+" in the format of www.domain_name.com"
        response = model.generate_content(query)
        links=extract_links(response.text)
        links.insert(0,prediction)
        if response.text:
            return render_template("response.html", output=links)
        else:
            return render_template("response.html", output="Sorry, but we didn't get an answer to that!")
    except Exception as e:
        return render_template("response.html", output="Sorry, but we didn't get an answer to that!")
'''


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
    prediction=pred(site_url)
    try:
        query = "Give me alternate websites to use for "+site_functionality+" in the format of www.domain_name.com"
        response = model.generate_content(query)
        links=extract_links(response.text)
        links.insert(0,prediction)
    except Exception as e:
        links=["Sorry Sar Kitiyilla"]
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