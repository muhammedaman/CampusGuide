
# CampusGuide 🎓🤖

CampusGuide is an AI-powered college interaction chatbot built using Flask, HTML, CSS, JavaScript, and Google's Gemini AI. It is designed to simplify access to academic information such as attendance, assignments, internal marks, sessional exams, and more — all through an intuitive conversational interface.

> 🌟 Whether you're a student checking attendance or a visitor asking general queries, CampusGuide makes it effortless.

---

## 🧠 Features

- 🔍 **Smart Query Handling** — Predefined intents + Gemini AI for intelligent fallback responses.
- 🗂️ **Academic Info Retrieval** — Fetch real-time data like attendance, assignments, internal marks, etc.
- 💬 **Interactive Frontend** — Clean and responsive chat interface.
- 🔁 **Fallback to Gemini AI** — When no pattern matches, Google Gemini AI generates a relevant response.

---

## 🛠️ Tech Stack

| Component     | Technology                         |
|---------------|------------------------------------|
| Backend       | Python, Flask                      |
| Frontend      | HTML, CSS, JavaScript              |
| AI Engine     | Google Gemini AI (gemini-1.5-flash)|
| Data Format   | JSON (`dataset1.json`)             |
| CORS          | Enabled via `flask_cors`           |
| Credentials   | Etlab portal login (used for academic data fetch) |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/muhammedaman/CampusGuide.git
cd CampusGuide
```

### 2. Set Up Python Environment

Install dependencies (use a virtual environment if preferred):

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, manually install:

```bash
pip install flask flask-cors google-generativeai
```

### 3. Add Your Gemini API Key

In `chat.py`, locate:

```python
genai.configure(api_key="YOUR_API_KEY")
```

Replace `"YOUR_API_KEY"` with your **Gemini API key**. You can get your key here: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

## ▶️ Running the Project

1. Start the Flask server:

```bash
python chat.py
```

2. Open your browser and navigate to:

```
http://127.0.0.1:5000/
```

3. Interact with the chatbot!

---

## 🧩 Structure

```
CampusGuide/
│
├── chat.py               # Flask backend and routing
├── app.js                # Frontend logic for chat interaction
├── website.html          # Main webpage
├── dataset1.json         # Predefined intent patterns & responses
├── attendance.py         # Module to fetch academic data (Etlab)
├── static/               # JS, images
└── templates/
    └── website.html      # HTML template
```

---

## 📚 Dataset Format (dataset1.json)

```json
{
  "intents": [
    {
      "tag": "greeting",
      "patterns": ["Hi", "Hello", "Hey"],
      "responses": ["Hello! How can I help you today?"]
    },
    {
      "tag": "college_name",
      "patterns": ["What is the name of the college?"],
      "responses": ["KMCT College of Engineering, Kozhikode."]
    }
  ]
}
```

You can customize `patterns` and `responses` to match your institution or domain.

---

## 🔐 Handling Login

For academic-related queries (like attendance), users are prompted to enter their **username** and **password**. The backend fetches data using `attendance.py`, which connects to the college's Etlab portal.

If credentials are missing or invalid, the chatbot gracefully asks the user to input them.

---

## 📦 Sample Gemini Fallback

If no intent matches:

```python
response = get_gemini_response("What is cloud computing?")
```

Gemini AI will generate a smart response:

```
"Cloud computing is the delivery of computing services such as storage, processing, and networking over the internet..."
```

---

## 💡 Example Questions

- "Show my attendance"
- "Give me my internal marks"
- "When is the next sessional exam?"
- "Who is the principal?"
- "What is artificial intelligence?" ← (Gemini AI responds)

---

## 🧑‍💻 Contributing

1. Fork the repo
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push and open a PR.

---

## 🪪 License

This project is licensed under the **Apache 2.0 License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Google Generative AI](https://aistudio.google.com/) for the Gemini model.
- KMCT College of Engineering, Kozhikode.
- Etlab portal integration reference.

---

## 📬 Contact

For queries or feedback, reach out via GitHub Issues or contact [@muhammedaman](https://github.com/muhammedaman).

---

> Made with 💙 for student communities.
