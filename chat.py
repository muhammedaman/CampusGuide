from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
import random
import google.generativeai as genai
from attendance import fetch_etlab_data  # Import attendance function

# Configure Gemini AI
genai.configure(api_key="AIzaSyCpfg6SaInRfG1eEd8KJySc4vghLdJ4jI0")
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
CORS(app)

# Load dataset1.json safely
try:
    with open("dataset1.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        intents = data.get("intents", [])  # Ensure it's a list
except Exception as e:
    print(f"Error loading intents file: {e}")
    intents = []  # Fallback empty list

def find_intent(message):
    """Find predefined intent responses"""
    if not isinstance(intents, list):
        print("Error: 'intents' should be a list.")
        return None

    for intent in intents:
        if not isinstance(intent, dict):
            continue  # Skip if intent is not a dictionary

        patterns = intent.get("patterns", [])
        if not isinstance(patterns, list):
            continue  # Skip if patterns are missing or incorrect

        for pattern in patterns:
            if pattern.lower() in message.lower():
                return intent.get("responses", [])

    return None  # No matching intent

def get_gemini_response(message):
    """Generate response using Gemini AI"""
    try:
        response = model.generate_content(message)
        return response.text if response and hasattr(response, "text") else "I'm not sure how to respond."
    except Exception as e:
        print(f"Error with Gemini AI: {e}")
        return "I'm sorry, I couldn't process your request."

def format_multiline_response(response_text):
    """Split response into line-by-line format."""
    return [{"text": line.strip()} for line in response_text.split("\n") if line.strip()]

@app.route("/")
def index():
    return render_template("website.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        message = data.get("message")
        username = data.get("username")
        password = data.get("password")

        if not message:
            return jsonify({"error": "Invalid or missing 'message' in the request JSON."}), 400

        print(f"🔹 Received message: {message}")

        # 📌 Handle attendance request
        if "attendance" in message.lower():
            if not username or not password:
                return jsonify({"answer": "Please provide your username and password to fetch attendance.", "ask_credentials": True})

            etlab_data = fetch_etlab_data(username, password)
            if "error" in etlab_data:
                return jsonify({"answer": etlab_data["error"]})

            print("✅ Fetched Attendance Data:", etlab_data["attendance"])

            attendance_data = etlab_data["attendance"][0]
            student_info = {
                "UNi Reg No": attendance_data.get("UNi Reg No", "N/A"),
                "Roll No": attendance_data.get("Roll No", "N/A"),
                "Name": attendance_data.get("Name", "N/A"),
                "Total": attendance_data.get("Total", "N/A"),
                "Percentage": attendance_data.get("Percentage", "N/A"),
            }

            subjects = [
                {"Subject": key, "Attendance": value}
                for key, value in attendance_data.items()
                if key not in {"UNi Reg No", "Roll No", "Name", "Total", "Percentage"}
            ]

            return jsonify({
                "answer": "Here is your attendance:",
                "student_info": student_info,
                "subjects": subjects
            })

        # 📌 Handle assignments request
        if "assignment" in message.lower():
            if not username or not password:
                return jsonify({"answer": "Please provide your username and password to fetch assignments.", "ask_credentials": True})

            etlab_data = fetch_etlab_data(username, password)
            if "error" in etlab_data:
                return jsonify({"answer": etlab_data["error"]})

            print("✅ Fetched Assignments Data:", etlab_data["assignments"])

            return jsonify({
                "answer": "Here are your assignments:",
                "assignments": etlab_data["assignments"]
            })

        # 📌 Handle sessional exam request
        if any(keyword in message.lower() for keyword in ["session test", "session exam", "sessional exam schedule"]):
            if not username or not password:
                return jsonify({
                    "answer": "Please provide your username and password to fetch session test details.", 
                    "ask_credentials": True
                })

            etlab_data = fetch_etlab_data(username, password)
            if "error" in etlab_data:
                return jsonify({"answer": etlab_data["error"]})

            session_tests = etlab_data.get("sessional_exams", [])

            if not session_tests:
                return jsonify({"answer": "No session test details found."})

            formatted_session_tests = [
                {
                    "Subject": test.get("Subject", "N/A"),
                    "Exam": test.get("Exam", "N/A"),
                    "Maximum Marks": test.get("Maximum Marks", "N/A"),
                    "Marks Obtained": test.get("Marks Obtained", "N/A")
                }
                for test in session_tests
            ]

            return jsonify({
                "answer": "Here are your session test details:",
                "sessional_exams": formatted_session_tests
            })

        # 📌 Handle module test request
        if "module test" in message.lower():
            if not username or not password:
                return jsonify({"answer": "Please provide your username and password to fetch module test details.", "ask_credentials": True})

            etlab_data = fetch_etlab_data(username, password)
            if "error" in etlab_data:
                return jsonify({"answer": etlab_data["error"]})

            module_tests = [
                {
                    "Subject": test.get("Subject", "N/A"),
                    "Exam": test.get("Exam", "N/A"),
                    "Maximum Marks": test.get("Maximum Marks", "N/A"),
                    "Marks Obtained": test.get("Marks Obtained", "N/A")
                }
                for test in etlab_data.get("module_tests", [])
            ]

            return jsonify({"answer": "Here are your module test details:", "module_tests": module_tests})

        # 📌 Handle general chatbot queries
        response = find_intent(message)

        if response:
            print(f"✅ Matched intent response: {response}")
            return jsonify({"answer": random.choice(response)})

        print("❌ No matching intent found, using Gemini AI")
        gemini_reply = get_gemini_response(message)

        if not gemini_reply or "Error" in gemini_reply:
            print("⚠️ Gemini AI failed, sending default response")
            gemini_reply = "I'm sorry, but I couldn't generate a response."

        return jsonify({"answer": gemini_reply})

    except Exception as e:
        print(f"❌ Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
