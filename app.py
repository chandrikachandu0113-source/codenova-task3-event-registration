
from flask import Flask, render_template, request, jsonify
from database import get_connection, initialize_database
from datetime import date
import re

app = Flask(__name__)

# Create database tables if they don't exist
initialize_database()


@app.route("/")
def home():
    connection = get_connection()
    events = connection.execute("""
        SELECT e.*,
        (SELECT COUNT(*) FROM registrations r
         WHERE r.event_id = e.id) AS registered
        FROM events e
        ORDER BY e.event_date
    """).fetchall()
    connection.close()

    return render_template("index.html", events=events)


@app.route("/api/events")
def get_events():
    connection = get_connection()

    events = connection.execute("""
        SELECT e.*,
        (SELECT COUNT(*) FROM registrations r
         WHERE r.event_id = e.id) AS registered
        FROM events e
        ORDER BY e.event_date
    """).fetchall()

    connection.close()

    return jsonify([dict(event) for event in events])


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid request."}), 400

    event_id = data.get("event_id")
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()

    if not event_id or not name or not email:
        return jsonify({
            "error": "All fields are required."
        }), 400

    if len(name) > 100:
        return jsonify({
            "error": "Name must be 100 characters or less."
        }), 400

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return jsonify({
            "error": "Enter a valid email address."
        }), 400

    try:
        event_id = int(event_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid event."}), 400

    connection = get_connection()

    try:
        event = connection.execute(
            "SELECT * FROM events WHERE id = ?",
            (event_id,)
        ).fetchone()

        if event is None:
            return jsonify({"error": "Event not found."}), 404

        if event["event_date"] < date.today().isoformat():
            return jsonify({
                "error": "Registration for this event has closed."
            }), 400

        count = connection.execute("""
            SELECT COUNT(*) FROM registrations
            WHERE event_id = ?
        """, (event_id,)).fetchone()[0]

        if count >= event["capacity"]:
            return jsonify({
                "error": "This event is fully booked."
            }), 400

        connection.execute("""
            INSERT INTO registrations
            (event_id, participant_name, email)
            VALUES (?, ?, ?)
        """, (event_id, name, email))

        connection.commit()

        return jsonify({
            "message": "Registration successful!"
        }), 201

    except Exception as error:
        connection.rollback()

        if "UNIQUE constraint failed" in str(error):
            return jsonify({
                "error": "You are already registered for this event."
            }), 409

        app.logger.exception("Registration failed")
        return jsonify({
            "error": "Registration failed. Please try again."
        }), 500

    finally:
        connection.close()


@app.route("/admin")
def admin():
    connection = get_connection()

    registrations = connection.execute("""
        SELECT r.id, r.participant_name, r.email,
               r.registered_at, e.title, e.event_date
        FROM registrations r
        JOIN events e ON r.event_id = e.id
        ORDER BY r.registered_at DESC
    """).fetchall()

    connection.close()

    return render_template(
        "admin.html",
        registrations=registrations
    )


if __name__ == "__main__":
    app.run(debug=True)
