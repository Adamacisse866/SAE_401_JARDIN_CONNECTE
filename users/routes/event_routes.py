# routes/event_routes.py
from flask import Blueprint, jsonify
from models.event import Event

event_routes = Blueprint("event_routes", __name__)

@event_routes.route("/api/events", methods=["GET"])
def get_events():
    try:
        events = Event.query.all()
        event_list = [
            {
                "title": event.title,
                "description": event.description,
                "date": event.date,
                "image_url": event.image_url,
                "link": event.link
            }
            for event in events
        ]
        return jsonify(event_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
