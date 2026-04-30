import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import re

# ---------------- DATABASE CONNECTION ----------------
conn = psycopg2.connect(
    dbname="crm_db",
    user="postgres",
    password="hari@123",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# ---------------- FASTAPI APP ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST MODEL ----------------
class ChatInput(BaseModel):
    message: str


# ---------------- AI EXTRACTION ----------------
def extract_data(text):
    text_lower = text.lower()

    # -------- DOCTOR EXTRACTION --------
    match = re.search(r"dr\.?\s*([A-Za-z]+)", text, re.IGNORECASE)

    doctor = ""
    if match:
        doctor = "Dr " + match.group(1).strip()

    # -------- SENTIMENT --------
    sentiment = "Neutral"
    if "negative" in text_lower:
        sentiment = "Negative"
    elif "positive" in text_lower:
        sentiment = "Positive"

    # -------- MATERIALS --------
    materials = "Brochure" if "brochure" in text_lower else ""

    # -------- FOLLOW-UP --------
    followup = "Follow up next week" if "follow" in text_lower else ""

    # -------- OUTCOMES --------
    outcomes = "Outcome discussed" if "outcome" in text_lower else ""

    # -------- TOPICS --------
    match_topics = re.search(r"discussed (.*?)(\.|$)", text, re.IGNORECASE)
    topics = "Discussed " + match_topics.group(1).strip() if match_topics else ""

    # -------- RETURN --------
    return {
        "doctor": doctor,
        "interaction_type": "Meeting",
        "attendees": "",
        "topics": topics,
        "materials": materials,
        "sentiment": sentiment,
        "outcomes": outcomes,
        "followup": followup,
        "ai_followup": "Suggested: Schedule follow-up meeting",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M")
    }


# ---------------- DB HELPER ----------------
def get_last_interaction():
    cursor.execute("""
        SELECT id, doctor, interaction_type, attendees, topics,
               materials, sentiment, outcomes, followup,
               ai_followup, date, time
        FROM interactions
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    if not row:
        return None

    return {
        "id": row[0],
        "doctor": row[1],
        "interaction_type": row[2],
        "attendees": row[3],
        "topics": row[4],
        "materials": row[5],
        "sentiment": row[6],
        "outcomes": row[7],
        "followup": row[8],
        "ai_followup": row[9],
        "date": row[10],
        "time": row[11]
    }


# ---------------- TOOL 1: LOG INTERACTION ----------------
def log_interaction_tool(data):
    try:
        cursor.execute("""
            INSERT INTO interactions
            (doctor, interaction_type, attendees, topics, materials,
             sentiment, outcomes, followup, ai_followup, date, time)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data["doctor"],
            data["interaction_type"],
            data["attendees"],
            data["topics"],
            data["materials"],
            data["sentiment"],
            data["outcomes"],
            data["followup"],
            data["ai_followup"],
            data["date"],
            data["time"]
        ))

        conn.commit()
        return "Interaction logged successfully"

    except Exception as e:
        conn.rollback()
        return f"Database error: {str(e)}"


# ---------------- TOOL 2: EDIT INTERACTION ----------------
def edit_interaction_tool(message):
    last = get_last_interaction()
    if not last:
        return {}

    msg = message.lower()
    updates = {}
    values = []

    # -------- DOCTOR --------
    match = re.search(r"dr\.?\s*([A-Za-z]+)", message, re.IGNORECASE)
    if match:
        updates["doctor"] = "Dr " + match.group(1).strip()

 # -------- SENTIMENT --------
    if any(word in msg for word in ["negative", "bad", "not interested"]):
        updates["sentiment"] = "Negative"

    elif any(word in msg for word in ["positive", "good", "interested"]):
        updates["sentiment"] = "Positive"

    elif any(word in msg for word in ["neutral", "ok", "average"]):
        updates["sentiment"] = "Neutral"
    # -------- FOLLOWUP --------
    if "follow" in msg:
        updates["followup"] = "Follow-up updated"

    # If nothing to update
    if not updates:
        return last

    # -------- BUILD QUERY DYNAMICALLY --------
    set_clause = ", ".join([f"{key}=%s" for key in updates.keys()])
    values = list(updates.values())
    values.append(last["id"])

    query = f"UPDATE interactions SET {set_clause} WHERE id=%s"

    cursor.execute(query, values)
    conn.commit()

    # return merged result (important for frontend)
    last.update(updates)
    return last


# ---------------- TOOL 3: HISTORY ----------------
def get_history_tool():
    cursor.execute("""
        SELECT doctor, topics, sentiment, date
        FROM interactions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    if not rows:
        return "No interactions found"

    history = ""
    for i, row in enumerate(rows, 1):
        history += f"""
Interaction {i}
Doctor: {row[0]}
Topics: {row[1]}
Sentiment: {row[2]}
Date: {row[3]}
--------------------
"""
    return history


# ---------------- TOOL 4: SUMMARY ----------------
def summarize_tool():
    last = get_last_interaction()
    if not last:
        return "No interaction available"

    summary = "Summary: "

    if last["topics"]:
        summary += last["topics"] + ". "

    if last["sentiment"] == "Positive":
        summary += "HCP showed positive interest. "
    elif last["sentiment"] == "Negative":
        summary += "HCP showed concerns. "

    if last["materials"]:
        summary += "Materials shared included. "

    if last["followup"]:
        summary += "Follow-up required. "

    return summary


# ---------------- TOOL 5: FOLLOW-UP ----------------
def followup_tool():
    last = get_last_interaction()
    if not last:
        return "No data for follow-up"

    sentiment = last["sentiment"]

    if sentiment == "Positive":
        return "Follow-up: Schedule product demo next week"
    elif sentiment == "Negative":
        return "Follow-up: Address concerns and re-engage in 2 weeks"
    else:
        return "Follow-up: Share additional information and reconnect"


# ---------------- ROUTER ----------------
def langgraph_agent(message):
    msg = message.lower()

    if any(word in msg for word in ["edit", "change", "update", "modify"]):
        return edit_interaction_tool(message), "Interaction updated"

    elif "history" in msg:
        return {}, get_history_tool()

    elif "summary" in msg:
        return {}, summarize_tool()

    elif "follow" in msg:
        return {}, followup_tool()

    else:
        data = extract_data(message)
        log_interaction_tool(data)
        return data, "Interaction logged successfully"


# ---------------- API ----------------
@app.get("/")
def home():
    return {"message": "Backend running"}

@app.post("/chat")
def chat(data: ChatInput):
    ai_output, tool_output = langgraph_agent(data.message)

    return {
        "ai_extracted": ai_output,
        "tool_result": tool_output
    }