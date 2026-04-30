# AI-First CRM HCP Module

## 📌 Project Overview

This project is an AI-driven Customer Relationship Management (CRM) system designed for logging Healthcare Professional (HCP) interactions.

Instead of manually filling forms, users interact with an AI chatbot that automatically extracts relevant details and fills the interaction form.

---

## 🚀 Key Features

* 🤖 Chat-based interaction logging
* 🧾 Automatic form filling using AI
* ✏️ Edit interactions via chatbot
* 📜 View interaction history
* 🧠 AI-generated summaries
* 📅 AI-suggested follow-up actions

---

## 🧩 Tech Stack

### Frontend

* React.js
* CSS (Google Inter Font)

### Backend

* FastAPI (Python)

### AI / Agent

* LangGraph (rule-based simulation)
* Groq LLM (gemma2-9b-it model - optional integration)

### Database

* PostgreSQL

---

## 🛠️ Project Structure

```
ai-crm-hcp-module/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   ├── public/
│   ├── package.json
│
├── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

### 2️⃣ Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on:

```
http://localhost:3000
```

---

### 3️⃣ Database Setup (PostgreSQL)

1. Create database:

```
crm_db
```

2. Run this SQL query:

```sql
CREATE TABLE interactions (
    id SERIAL PRIMARY KEY,
    doctor TEXT,
    interaction_type TEXT,
    attendees TEXT,
    topics TEXT,
    materials TEXT,
    sentiment TEXT,
    outcomes TEXT,
    followup TEXT,
    ai_followup TEXT,
    date TEXT,
    time TEXT
);
```

---

## 🧠 LangGraph Agent & Tools

The system simulates a LangGraph agent that routes user input to different tools.

### 🔧 Tools Implemented

1. **Log Interaction Tool**

   * Extracts structured data from chat input
   * Stores interaction in database

2. **Edit Interaction Tool**

   * Updates last interaction using chat commands

3. **Get History Tool**

   * Retrieves all past interactions

4. **Summarize Tool**

   * Generates summary of last interaction

5. **Follow-up Tool**

   * Suggests next actions based on sentiment

---

## 💬 Example Input

```
Met Dr Ravi and discussed insulin. sentiment was positive and shared brochure
```

---

## 📋 Example Output (Auto-filled Form)

* HCP Name: Dr Ravi
* Interaction Type: Meeting
* Topics: Discussed insulin
* Sentiment: Positive
* Materials: Brochure
* Date & Time: Auto-generated

---

## 🎯 Objective

To demonstrate how AI can replace manual CRM workflows using conversational interfaces, improving efficiency and usability for field representatives.

---

## 🎥 Demo Requirements

* Chat-based logging
* Form auto-fill
* Edit via chatbot
* Show history
* Summary generation
* Follow-up suggestions

---

## 📌 Conclusion

This project showcases an AI-first approach to CRM systems by combining conversational AI, backend processing, and structured data storage.

---

## 👩‍💻 Author

Harini Meena
