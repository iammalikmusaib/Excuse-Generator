from flask import Flask, jsonify, request, render_template
import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Configure Flask application
app = Flask(__name__, template_folder='templates', static_folder='static')

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

# Retrieve API key from environment variables
API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

if not API_KEY:
    logging.error("API Key not found. Please set GOOGLE_GEMINI_API_KEY in your .env file.")
    raise ValueError("API Key not found. Please set GOOGLE_GEMINI_API_KEY in your .env file.")

genai.configure(api_key=API_KEY)

@app.route('/')
def home():
    logging.debug("Rendering the homepage.")
    # Render the HTML frontend
    return render_template('index.html')

@app.route('/generate_excuse', methods=['POST'])
def generate_excuse():
    try:
        # Get the input topic from the user
        data = request.json
        topic = data.get('topic', 'something')

        logging.debug(f"Received topic: {topic}")

        # Prompt for the Gemini model
        prompt = f"Generate in 30 words a professional and in human words,use emotions, creative and realistic way excuse about {topic}."
        logging.debug(f"Constructed prompt: {prompt}")

        # Generate content using the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        logging.debug(f"Model response: {response}")

        # Extract the text response
        excuse = response.text.strip() if response.text else "No excuse generated."
        logging.info(f"Generated excuse: {excuse}")

        return jsonify({"excuse": excuse})

    except Exception as e:
        # Handle any errors
        logging.error(f"Error during excuse generation: {e}")
        return jsonify({"error": f"Failed to generate excuse. Error: {str(e)}"}), 500

if __name__ == '__main__':
    logging.info("Starting the Flask application.")
    app.run(debug=True)
