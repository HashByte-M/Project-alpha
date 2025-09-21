# server.py
import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

# 1. Initialize the Flask App
app = Flask(__name__)
# Allow requests from our front-end (Cross-Origin Resource Sharing)
CORS(app)

# 2. Configure the Gemini API
# IMPORTANT: Set your API key as an environment variable for security.
# In your terminal, run: set GOOGLE_API_KEY="your_api_key_here" (Windows)
# or: export GOOGLE_API_KEY="your_api_key_here" (Mac/Linux)
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("API Key not found. Please set the GOOGLE_API_KEY environment variable.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

# 3. Create an API Endpoint for AI Analysis
@app.route('/analyze-correlation', methods=['POST'])
def analyze_correlation():
    if not model:
        return jsonify({"error": "Gemini model is not configured"}), 500

    # Get the data sent from the front-end
    data = request.json
    param1 = data.get('param1')
    param2 = data.get('param2')
    correlation = data.get('correlation')

    if not all([param1, param2, correlation]):
        return jsonify({"error": "Missing parameters"}), 400

    # Create a prompt for the AI model
    prompt = f"""
    As a research hydrologist, analyze the relationship between two parameters: '{param1}' and '{param2}'.
    The calculated Pearson correlation coefficient is: **{correlation:.2f}**.

    Provide a scientific interpretation of this relationship in one concise paragraph:
    1.  Explain the correlation (strength and direction).
    2.  Explain the likely physical or chemical reasons for this relationship in a water system.
    3.  Briefly state the implications for water resource monitoring.
    """

    try:
        # Call the Gemini API
        response = model.generate_content(prompt)
        return jsonify({"analysis": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. Run the Flask App
if __name__ == '__main__':
    # Runs on http://127.0.0.1:5000
    app.run(debug=True, port=5000)