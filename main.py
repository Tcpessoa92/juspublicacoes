from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/consultar-publicacoes', methods=['GET'])
def consultar_publicacoes():
    try:
        nome = request.args.get('nome', 'Thiago Cunha Pessoa')
        oab = request.args.get('oab', '53292')
        uf = request.args.get('uf', 'BA')
        pagina = request.args.get('pagina', 1)
        quantidade = request.args.get('quantidade', 10)

        headers = {
            'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
            'Accept': 'application/json'
        }

        params = {
            'nomeAdvogado': nome,
            'numeroOab': oab,
            'ufOab': uf,
            'pagina': pagina,
            'itensPorPagina': quantidade
        }

        response = requests.get(
            'https://comunicaapi.pje.jus.br/api/v1/comunicacao',
            headers=headers,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        return jsonify(response.json()), response.status_code

    except requests.exceptions.HTTPError as e:
        return jsonify({
            "erro": "Erro HTTP da API CNJ",
            "resposta": response.text,
            "status_code": response.status_code
        }), response.status_code

    except Exception as e:
        return jsonify({
            "erro": "Erro interno no servidor",
            "detalhe": str(e)
        }), 500

@app.route('/')
def index():
    return jsonify({
        "mensagem": "API JusPublicacoes ativa",
        "exemplo": "/consultar-publicacoes?nome=Thiago+Pessoa&oab=53292&uf=BA"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)