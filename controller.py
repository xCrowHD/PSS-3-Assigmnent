from flask import jsonify, request
from model import (get_all_events, add_event, update_event, delete_event, 
                   get_all_categories, add_category, 
                   get_daily_study_summary, get_weekly_study_summary, get_monthly_study_summary)

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
            data.get('color', '#a8d8ea'),
            data.get('category_id')
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
            data.get('color'),
            data.get('category_id')
        )
        return jsonify({"message": "Evento aggiornato"}), 200

    @app.route('/api/events/<int:event_id>', methods=['DELETE'])
    def handle_delete_event(event_id):
        delete_event(event_id)
        return jsonify({"message": "Evento eliminato"}), 200

    # Endpoints per le categorie
    @app.route('/api/categories', methods=['GET'])
    def handle_get_categories():
        categories = get_all_categories()
        return jsonify([dict(cat) for cat in categories])

    @app.route('/api/categories', methods=['POST'])
    def handle_add_category():
        data = request.get_json()
        category_id = add_category(data['name'])
        return jsonify({"id": category_id, "name": data['name']}), 201

    @app.route('/api/study_summary/daily', methods=['GET'])
    def handle_daily_study_summary():
        start = request.args.get('start')
        end = request.args.get('end')
        summary = get_daily_study_summary(start, end)
        return jsonify([dict(row) for row in summary])

    @app.route('/api/study_summary/weekly', methods=['GET'])
    def handle_weekly_study_summary():
        start = request.args.get('start')
        end = request.args.get('end')
        summary = get_weekly_study_summary(start, end)
        return jsonify([dict(row) for row in summary])

    @app.route('/api/study_summary/monthly', methods=['GET'])
    def handle_monthly_study_summary():
        start = request.args.get('start')
        end = request.args.get('end')
        summary = get_monthly_study_summary(start, end)
        return jsonify([dict(row) for row in summary])

