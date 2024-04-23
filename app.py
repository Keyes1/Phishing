import google.generativeai as genai
import os
from feature_extract import pred,extract_links
from flask import Flask, render_template, request, redirect, url_for
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import random


total_questions=0
Jyu=0

my_api_key_gemini = 'AIzaSyAmulpvGbEpbEISbq_VwhpqZYUfs2pHq8k'
model = genai.GenerativeModel('gemini-pro')
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
    prediction=pred(site_url)
    try:
        query = "Give me alternate websites to use for "+site_functionality+" in the format of www.domain_name.com"
        response = model.generate_content(query)
        links=extract_links(response.text)
    except Exception as e:
        links=["Sorry Sar Kitiyilla"]
    label = "Alternate links for {} ({})".format(site_url, site_functionality)
    return render_template('link_results.html', links=links, label=label, prediction=prediction)

# Define the cybersecurity areas and their priorities
areas = ["Network Security", "Encryption", "Web Security", "Malware Analysis"]
priorities = [0, 0, 0, 0]

# Define beginner-level questions and answers for each area
beginner_questions = {
    "Network Security": [
        {"question": "What is a firewall used for?", "options": ["A. To control incoming and outgoing network traffic", "B. To monitor keyboard inputs", "C. To play games"], "answer": "A"},
        {"question": "What does HTTPS stand for?", "options": ["A. HyperText Transfer Protocol Secure", "B. HyperText Transfer Protocol Standard", "C. HyperText Secure Protocol"], "answer": "A"},
        {"question": "What is a router?", "options": ["A. A device that forwards data packets between computer networks", "B. A device for printing documents", "C. A type of keyboard"], "answer": "A"}
    ],
    "Encryption": [
        {"question": "What is RSA encryption?", "options": ["A. Asymmetric encryption algorithm", "B. Random symmetric algorithm", "C. Fast encryption method"], "answer": "A"},
        {"question": "What is symmetric encryption?", "options": ["A. Encryption using different keys", "B. Encryption using a single key", "C. No encryption"], "answer": "B"},
        {"question": "What is a key length in encryption?", "options": ["A. Length of the message", "B. Length of the password", "C. Number of bits in a key"], "answer": "C"}
    ],
    "Web Security": [
        {"question": "What is Cross-Site Scripting (XSS)?", "options": ["A. Injection attack where malicious scripts are injected into websites", "B. Attack on a physical cross-site", "C. Secure authentication protocol"], "answer": "A"},
        {"question": "What is phishing?", "options": ["A. A fraudulent attempt to obtain sensitive information by disguising as a trustworthy entity", "B. Fishing in the sea", "C. A technique to catch malware"], "answer": "A"},
        {"question": "What is malware?", "options": ["A. Malicious software designed to harm or exploit computers", "B. A type of hardware component", "C. A software to secure networks"], "answer": "A"}
    ],
    "Malware Analysis": [
        {"question": "What is a virus?", "options": ["A. Malicious software that replicates itself", "B. A good software", "C. A hardware component"], "answer": "A"},
        {"question": "What is a trojan?", "options": ["A. Malware disguised as legitimate software", "B. Software that cleans viruses", "C. A type of horse"], "answer": "A"},
        {"question": "What is ransomware?", "options": ["A. Malicious software that encrypts files and demands payment for decryption", "B. A security software", "C. A type of hardware"], "answer": "A"}
    ]
}

# Brief descriptions of each area
area_descriptions = {
    "Network Security": "Network security involves protecting computer networks from unauthorized access or misuse.",
    "Encryption": "Encryption is the process of converting data into a form that cannot be easily understood by unauthorized people.",
    "Web Security": "Web security focuses on protecting websites and web applications from various types of cyber threats.",
    "Malware Analysis": "Malware analysis involves studying, identifying, and understanding the behavior of malicious software."
}

# Lists to keep track of used questions for each area
used_questions = {area: [] for area in areas}

# Lists to keep track of correct and incorrect answers for each area
correct_answers = [0, 0, 0, 0]
incorrect_answers = [0, 0, 0, 0]

# Function to display options for the question
def display_options(options):
    option_list = []
    for option in options:
        option_list.append(option)
    return option_list

# Route for the quiz page
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global total_questions, correct_answers, incorrect_answers, priorities, question_obj, chosen_area, Jyu

    if request.method == 'POST':
        # Get the user's answer from the form
        user_answer = request.form['answer']

        # Check if the answer is correct
        if user_answer == question_obj["answer"].upper():
            correct_answers[areas.index(chosen_area)] += 1
            Jyu += 1
        else:
            incorrect_answers[areas.index(chosen_area)] += 1
            priorities[areas.index(chosen_area)] += 1

        # Move to the next question
        total_questions += 1
        if total_questions < 8:
            return redirect(url_for('quiz'))
        else:
            # Render the result page with pie charts
            return redirect(url_for('result'))

    # Choose a random area based on priorities
    chosen_area = random.choices(areas, weights=[1 + priorities[i] for i in range(len(areas))])[0]

    # Select a question from the chosen area that hasn't been used before
    remaining_questions = beginner_questions[chosen_area]

    if len(remaining_questions)>0:
        question_obj = random.choice(remaining_questions)
        beginner_questions[chosen_area].remove(question_obj)
    question = question_obj["question"]
    options = display_options(question_obj["options"])

    return render_template('quiz.html', question=question, options=options)


# Route for the result page
@app.route('/result', methods=['GET'])
def result():
    global total_questions, Jyu
    # Pie chart for area-wise incorrect answers
    plt.figure(figsize=(10, 5))
    
    # Filter out areas with 0 incorrect answers
    filtered_areas = [area for area, count in zip(areas, incorrect_answers) if count != 0]
    filtered_incorrect_answers = [count for count in incorrect_answers if count != 0]
    
    plt.pie(filtered_incorrect_answers, labels=filtered_areas, autopct=lambda pct: f"{pct:.0f}%" if pct > 0 else "", startangle=90)
    plt.title('Area-wise Incorrect Answers')
    plt.axis('equal')  # Ensures the pie chart is drawn as a circle

    # Save the pie chart as a PNG image
    area_wise_pie = io.BytesIO()
    plt.savefig(area_wise_pie, format='png', bbox_inches='tight')
    area_wise_pie.seek(0)
    area_wise_pie_url = base64.b64encode(area_wise_pie.getvalue()).decode('utf-8')

    # Pie chart for overall performance
    plt.figure(figsize=(5, 5))
    total_incorrect = sum(filtered_incorrect_answers)


    if total_questions > 0:
        correct_percentage = (Jyu / total_questions) * 100
        incorrect_percentage = 100 - correct_percentage
        plt.pie([correct_percentage, incorrect_percentage], labels=['Correct', 'Incorrect'], autopct='%1.1f%%', startangle=90)
    else:
        plt.pie([1], labels=['No Data'], autopct='')
        
    plt.title('Overall Performance')
    plt.axis('equal')  # Ensures the pie chart is drawn as a circle

    # Save the pie chart as a PNG image
    overall_pie = io.BytesIO()
    plt.savefig(overall_pie, format='png', bbox_inches='tight')
    overall_pie.seek(0)
    overall_pie_url = base64.b64encode(overall_pie.getvalue()).decode('utf-8')

    # Close the figures to free up memory
    plt.close('all')

    return render_template('result.html', area_descriptions=area_descriptions, area_wise_pie_url=area_wise_pie_url, overall_pie_url=overall_pie_url)

if __name__ == '__main__':
    app.run(debug=True)
    print()