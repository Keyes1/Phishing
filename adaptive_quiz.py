import random
import matplotlib.pyplot as plt

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

# Lists to keep track of used questions for each area
used_questions = {area: [] for area in areas}

# Lists to keep track of correct and incorrect answers for each area
correct_answers = [0, 0, 0, 0]
incorrect_answers = [0, 0, 0, 0]

# Function to display options for the question
def display_options(options):
    for option in options:
        print(option)

# Main quiz loop
total_questions = 0
while total_questions < 10:
    # Choose a random area based on priorities
    chosen_area = random.choices(areas, weights=[1 + priorities[i] for i in range(len(areas))])[0]
    
    # Select a question from the chosen area that hasn't been used before
    remaining_questions = [question for question in beginner_questions[chosen_area] if question not in used_questions[chosen_area]]
    if remaining_questions:
        question_obj = random.choice(remaining_questions)
        used_questions[chosen_area].append(question_obj)
        total_questions += 1  # Increment total questions asked
    else:
        continue
    
    question = question_obj["question"]
    options = question_obj["options"]
    answer = question_obj["answer"].lower()  # Convert the answer to lowercase for case-insensitive comparison
    
    # Print the question and options
    print("\nQuestion:", question)
    display_options(options)
    
    # Get user input for answer
    user_answer = input("Your answer (Enter A, B, or C): ").strip().lower()
    
    # Check if the answer is correct
    if user_answer == answer:
        print("Correct!")
        correct_answers[areas.index(chosen_area)] += 1
    else:
        print("Incorrect!")
        incorrect_answers[areas.index(chosen_area)] += 1
        priorities[areas.index(chosen_area)] += 1

# Pie chart for area-wise incorrect answers
plt.figure(figsize=(10, 5))
plt.pie(incorrect_answers, labels=areas, autopct='%1.1f%%', startangle=140)
plt.title('Area-wise Incorrect Answers')
plt.axis('equal')
plt.show()

# Pie chart for overall performance
total_correct = sum(correct_answers)
total_incorrect = sum(incorrect_answers)
plt.figure(figsize=(5, 5))
plt.pie([total_correct, total_incorrect], labels=['Correct', 'Incorrect'], autopct='%1.1f%%', startangle=140)
plt.title('Overall Performance')
plt.axis('equal')
plt.show()