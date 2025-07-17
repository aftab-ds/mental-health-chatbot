Aura 💖 - Your AI Mental Health Companion
A compassionate and intelligent chatbot designed to provide a safe space for users to express their feelings and receive empathetic support. Built with Google's Gemini, LangGraph, and Streamlit.

Note: You should replace the image URL above with a real screenshot of your application.

📋 About The Project
Aura is an agentic AI chatbot designed to act as a first point of contact for individuals seeking to talk about their well-being. The core of the application is an intelligent agent that first classifies the user's initial statement into one of three categories: General, Emergency, or Mental Health.

If the issue is General, Aura provides a standard disclaimer and recommends consulting a doctor.

If it's an Emergency, Aura gives immediate instructions to contact emergency services.

If it's a Mental Health concern, Aura transitions into a caring, conversational companion, offering an empathetic ear, asking gentle questions, and providing safe, general coping strategies and resources.

This project serves as a practical example of building stateful, agentic applications using modern AI tools.

✨ Features
Symptom Triage: Intelligently routes users based on their initial input.

Empathetic AI Companion: Provides a non-judgmental, conversational space for mental health topics.

Emergency Redirection: Clear and immediate guidance for critical situations.

Built with Modern Tech: Leverages the power of large language models (LLMs) and state machines for robust conversation flow.

User-Friendly Interface: A clean and simple chat interface built with Streamlit.

🛠️ Built With
Streamlit - For the web application framework.

LangGraph - For building the stateful, multi-agent application.

LangChain - For LLM integration and core components.

Google Gemini - As the core language model.

🚀 Getting Started
To get a local copy up and running, follow these simple steps.

Prerequisites
Python 3.8 or later

A Google API Key with the Gemini API enabled. You can get one from the Google AI Studio.

Installation
Clone the repository:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

Install the required packages:

pip install -r requirements.txt

Set up your API Key locally:

Create a new directory in your project folder named .streamlit.

Inside this new directory, create a file named secrets.toml.

Add your Google API key to this file as shown below:

GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

Usage
Run the Streamlit application from your terminal:

streamlit run app.py

Your browser should automatically open to the chatbot interface.

☁️ Deployment
This application is ready to be deployed on Streamlit Community Cloud.

Push your code to a public GitHub repository.

IMPORTANT: Ensure you have deleted the .streamlit/secrets.toml file from the repository before pushing. Never expose your secret keys publicly.

Sign up for Streamlit Community Cloud and link your GitHub account.

Create a "New app" and select your repository.

Add your Google API Key in the advanced settings under the "Secrets" section. The format should be the same as your secrets.toml file.

Click "Deploy!" and your app will be live.

⚠️ Disclaimer
Aura is an AI assistant and is not a substitute for professional medical advice, diagnosis, or treatment. It is designed for supportive and informational purposes only. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. If you are in a crisis or believe you may have an emergency, please contact your local emergency services immediately.

📄 License
Distributed under the MIT License. See LICENSE for more information.

🙏 Acknowledgements
The teams behind Streamlit, LangChain, and Google Gemini for their incredible tools.

The open-source community.
