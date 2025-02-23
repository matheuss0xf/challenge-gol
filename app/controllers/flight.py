from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required

from app.services.flight import FlightService

flight_bp = Blueprint('flights', __name__)
flight_service = FlightService()


@flight_bp.route('/flights', methods=['GET'])
@jwt_required()
def get_flights():
    try:
        query_params = {
            'market': request.args.get('market'),
            'flight_date': request.args.get('flight_date', ''),
            'sort': request.args.get('sort', default='year:asc,month:asc'),
        }

        flights = flight_service.search_flights(query_params)
        response = make_response(jsonify(flights))
        return response

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception:
        return jsonify({'error': 'Erro interno no servidor'}), 500
