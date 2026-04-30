import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [msg, setMsg] = useState("");
  const [chat, setChat] = useState([]);

  const [formData, setFormData] = useState({
    doctor: "",
    interaction_type: "",
    attendees: "",
    topics: "",
    sentiment: "",
    materials: "",
    outcomes: "",
    followup: "",
    ai_followup: "",
    date: "",
    time: ""
  });

  const send = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        message: msg
      });

      console.log("BACKEND RESPONSE:", res.data); // 🔍 DEBUG

      const data = res.data.ai_extracted;

      // ✅ ALWAYS update if data exists
     if (data) {
        setFormData((prev) => ({
  ...prev,
  ...data,
  doctor: data.doctor || prev.doctor
}));
      }

      // ✅ Chat update (safe)
      setChat((prev) => [
        ...prev,
        { type: "user", text: msg },
        { type: "bot", text: res.data.tool_result }
      ]);

      setMsg("");
    } catch (error) {
      console.error("ERROR:", error);
    }
  };

  return (
    <div className="container">

      {/* LEFT FORM */}
      <div className="form-section">
        <h2>Log HCP Interaction</h2>

        <div className="card">
          <h4>Interaction Details</h4>

          {/* HCP Name */}
          <label>HCP Name</label>
          <input value={formData.doctor || ""} placeholder="HCP Name" readOnly />

          {/* Interaction Type */}
          <label>Interaction Type</label>
          <input value={formData.interaction_type || ""} placeholder="Interaction Type" readOnly />

          {/* Date & Time */}
          <div className="row">
            <label>Date </label>

            <input value={formData.date || ""} readOnly />
            <label>Time </label>
            <input value={formData.time || ""} readOnly />
          </div>

          {/* Attendees */}
          <label>Attendees</label>
          <input value={formData.attendees || ""} placeholder="Attendees" readOnly />

          {/* Topics */}
          <label>Topics Discussed</label>
          <textarea value={formData.topics || ""} placeholder="Topics Discussed" readOnly />

          {/* Materials */}
          <label>Materials Shared</label>
          <input value={formData.materials || ""} placeholder="Materials Shared" readOnly />

          {/* Sentiment */}

          <label>Observed / Inferred HCP Sentiment</label>
          <div className="radio-group">
            <label>
              <input type="radio" checked={formData.sentiment === "Positive"} readOnly />
              😃 Positive
            </label>
            <label>
              <input type="radio" checked={formData.sentiment === "Neutral"} readOnly />
              🙂 Neutral
            </label>
            <label>
              <input type="radio" checked={formData.sentiment === "Negative"} readOnly />
              😔 Negative
            </label>
          </div>

          {/* Outcomes */}
          <label>Outcomes</label>
          <textarea value={formData.outcomes || ""} placeholder="Outcomes" readOnly />

          {/* Follow-up */}
          <label>Follow-up Actions</label>
          <textarea value={formData.followup || ""} placeholder="Follow-up Actions" readOnly />

          {/* AI Suggested Follow-up */}
          <textarea value={formData.ai_followup || ""} placeholder="AI Suggested Follow-up" readOnly />
        </div>
      </div>

      {/* RIGHT CHAT */}
      <div className="chat-section">
        <div className="chat-card">
          <h3>🤖 AI Assistant</h3>

          <div className="chat-box">
            {chat.map((c, i) => (
              <div key={i} className={c.type === "user" ? "user-msg" : "bot-msg"}>
                {c.text}
              </div>
            ))}
          </div>

          <textarea
            className="chat-input"
            value={msg}
            onChange={(e) => setMsg(e.target.value)}
            placeholder="Describe interaction..."
          />

          <button onClick={send}>Log</button>
        </div>
      </div>

    </div>
  );
}

export default App;
