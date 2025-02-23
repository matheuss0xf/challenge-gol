import logging

from flask import Blueprint, jsonify, make_response, request

from app.services.auth import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        logging.error('Nenhum dado fornecido no registro')
        return jsonify({'error': 'Nenhum dado fornecido'}), 400

    required_fields = ['name', 'email', 'password']
    if not all(field in data for field in required_fields):
        logging.error(f'Campos obrigatórios ausentes: {data}')
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    try:
        result = auth_service.register_user(name=data['name'], email=data['email'], password=data['password'])

        if 'error' in result:
            logging.error(f'Erro ao registrar usuário: {result["error"]}')
            return jsonify({'error': result['error']}), 400

        return jsonify(result), 201

    except Exception as e:
        logging.error(f'Erro no servidor durante o registro: {e}')
        return jsonify({'error': 'Erro interno no servidor'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        logging.error('Nenhum dado fornecido no login')
        return jsonify({'error': 'Nenhum dado fornecido'}), 400

    required_fields = ['email', 'password']
    if not all(field in data for field in required_fields):
        logging.error(f'Campos obrigatórios ausentes: {data}')
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400

    try:
        result = auth_service.authenticate_user(email=data['email'], password=data['password'])

        if 'error' in result:
            logging.error(f'Erro ao autenticar usuário: {result["error"]}')
            return jsonify({'error': result['error']}), 401

        response = make_response(jsonify({'user': result.get('user')}))
        response.set_cookie(
            'jwt', result.get('access_token'), httponly=True, secure=True, samesite='Strict', max_age=60 * 60 * 24 * 7
        )

        return response, 200

    except Exception as e:
        logging.error(f'Erro no servidor durante o login: {e}')
        return jsonify({'error': 'Erro interno no servidor'}), 500
