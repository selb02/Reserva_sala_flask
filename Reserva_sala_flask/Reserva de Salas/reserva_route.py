from flask import Blueprint, request, jsonify
from reserva_model import Reserva
from database import db
import requests

reserva_api = Blueprint("reserva_api", __name__)


def turma_existe(turma_id):
    url = f"https://sistema-escolar-flask.onrender.com/api/turma/{turma_id}"
    resposta = requests.get(url)
    return resposta.ok


@reserva_api.route("/reservas", methods=["POST"])
def adicionar_reserva():
    corpo = request.get_json()
    turma_id = corpo.get("turma_id")

    if not turma_existe(turma_id):
        return jsonify({"erro": "Turma inexistente"}), 400

    nova_reserva = Reserva(
        turma_id=turma_id,
        sala=corpo.get("sala"),
        data=corpo.get("data"),
    )

    db.session.add(nova_reserva)
    db.session.commit()

    return jsonify({"mensagem": "Reserva registrada com sucesso"}), 201


@reserva_api.route("/reservas", methods=["GET"])
def obter_reservas():
    todas_reservas = Reserva.query.all()
    resultado = []

    for r in todas_reservas:
        resultado.append({
            "id": r.id,
            "turma_id": r.turma_id,
            "sala": r.sala,
            "data": r.data,
        })

    return jsonify(resultado), 200


@reserva_api.route("/reservas/<int:codigo_reserva>", methods=["DELETE"])
def remover_reserva(codigo_reserva):
    reserva_encontrada = Reserva.query.get(codigo_reserva)

    if not reserva_encontrada:
        return jsonify({"erro": "Reserva não localizada"}), 404

    db.session.delete(reserva_encontrada)
    db.session.commit()

    return jsonify({"mensagem": "Reserva removida com sucesso"}), 200
