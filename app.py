from flask import Flask, render_template, request
import google.generativeai as genai
import os
from link_match import extract_links
from feature_extract import pred
model = genai.GenerativeModel('gemini-pro')

my_api_key_gemini = 'AIzaSyAmulpvGbEpbEISbq_VwhpqZYUfs2pHq8k'

genai.configure(api_key=my_api_key_gemini)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("check.html")

@app.route("/recommendation",methods=["POST"]) 
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
        return render_template("response.html", output="Sorry, but we didn't get an answer to that!")
    
if __name__ == "__main__":
  app.run(debug=True)