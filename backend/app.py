from flask import Flask, render_template, request, jsonify
from database import get_db_connection
import os
import requests

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)


@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message", "")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Save user message
    cursor.execute("""
    INSERT INTO messages
    (conversation_id, sender, message_text)
    VALUES (?,?,?)
    """, (1, "User", user_message))

    conn.commit()

    rasa_url = os.environ.get("RASA_URL", "http://localhost:5005").rstrip("/")

    try:
        rasa_response = requests.post(
            f"{rasa_url}/webhooks/rest/webhook",
            json={
                "sender": "user",
                "message": user_message
            },
            timeout=30,
        )
        rasa_response.raise_for_status()
        rasa_data = rasa_response.json()

        if rasa_data and rasa_data[0].get("text"):
            bot_response = rasa_data[0]["text"]
        else:
            bot_response = "Sorry, I could not understand your query."
    except (requests.RequestException, ValueError):
        app.logger.exception("Unable to get a response from Rasa")
        bot_response = "The chatbot service is temporarily unavailable. Please try again."

    # Save bot response
    cursor.execute("""
    INSERT INTO messages
    (conversation_id, sender, message_text)
    VALUES (?,?,?)
    """, (1, "Bot", bot_response))

    conn.commit()
    conn.close()

    return jsonify({
        "response": bot_response
    })


@app.route("/admin")
def admin_dashboard():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM intents")
    total_intents = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM responses")
    total_responses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM conversations")
    total_conversations = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_intents=total_intents,
        total_responses=total_responses,
        total_conversations=total_conversations,
        total_messages=total_messages
    )


@app.route("/admin/intents")
def view_intents():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM intents")

    intents = cursor.fetchall()

    conn.close()

    return render_template(
        "intents.html",
        intents=intents
    )


@app.route("/admin/responses")
def view_responses():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT response_id,
           intent_id,
           response_text
    FROM responses
    """)

    responses = cursor.fetchall()

    conn.close()

    return render_template(
        "responses.html",
        responses=responses
    )


@app.route("/admin/conversations")
def view_conversations():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT conversation_id,
           user_id,
           start_time
    FROM conversations
    """)

    conversations = cursor.fetchall()

    conn.close()

    return render_template(
        "conversations.html",
        conversations=conversations
    )


@app.route("/admin/messages")
def view_messages():

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT message_id,
           conversation_id,
           sender,
           message_text,
           timestamp
    FROM messages
    ORDER BY message_id DESC
    """)

    messages = cursor.fetchall()

    conn.close()

    return render_template(
        "messages.html",
        messages=messages
    )

@app.route("/admin/analytics")
def analytics():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM intents")
    total_intents = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM responses")
    total_responses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM conversations")
    total_conversations = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "analytics.html",
        total_intents=total_intents,
        total_responses=total_responses,
        total_conversations=total_conversations,
        total_messages=total_messages
    )

if __name__ == "__main__":
    app.run(debug=True)
