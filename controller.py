from flask import jsonify, request
from model import get_all_events, add_event, update_event, delete_event

def configure_routes(app):
    @app.route('/api/events', methods=['GET'])
    def handle_get_events():
        events = get_all_events()
        return jsonify([dict(event) for event in events])

    @app.route('/api/events', methods=['POST'])
    def handle_add_event():
        data = request.get_json()
        event_id = add_event(
            data['title'],
            data['start'],
            data.get('end'),
            data.get('description'),
            data.get('color', '#a8d8ea')
        )
        return jsonify({"id": event_id}), 201

    @app.route('/api/events/<int:event_id>', methods=['PUT'])
    def handle_update_event(event_id):
        data = request.get_json()
        update_event(
            event_id,
            data.get('title'),
            data.get('start'),
            data.get('end'),
            data.get('description'),
            data.get('color')
        )
        return jsonify({"message": "Evento aggiornato"}), 200

    @app.route('/api/events/<int:event_id>', methods=['DELETE'])
    def handle_delete_event(event_id):
        delete_event(event_id)
        return jsonify({"message": "Evento eliminato"}), 200