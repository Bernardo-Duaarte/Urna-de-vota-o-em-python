from flask import Blueprint, request, jsonify, Response
from models import db, Candidato, Voto, Eleitor
from sqlalchemy import func
import json

routes = Blueprint("routes", __name__)

def validar_cpf(cpf):
    return cpf.isdigit() and len(cpf) == 11 and not all(d == cpf[0] for d in cpf)

def validar_nome(nome):
    return len(nome.replace(" ", "")) >= 2 and all(c.isalpha() or c.isspace() for c in nome)


@routes.route("/cadastrar", methods=["POST"])
def cadastrar():
    data = request.get_json()
    cpf = data.get("cpf")
    nome = data.get("nome")

    if not cpf or not nome:
        return jsonify({"erro": "Informe 'cpf' e 'nome'."}), 400

    if not validar_cpf(cpf):
        return jsonify({"erro": "CPF inválido."}), 400

    if not validar_nome(nome):
        return jsonify({"erro": "Nome inválido."}), 400

    if Eleitor.query.filter_by(cpf=cpf).first():
        return jsonify({"erro": "CPF já cadastrado."}), 400

    novo_eleitor = Eleitor(cpf=cpf, nome=nome)
    db.session.add(novo_eleitor)
    db.session.commit()

    return jsonify({"mensagem": "Eleitor cadastrado com sucesso."}), 201


@routes.route("/votar", methods=["POST"])
def votar():
    data = request.get_json()
    cpf = data.get("cpf")
    candidato_id = data.get("candidato_id")

    if not cpf or not candidato_id:
        return jsonify({"erro": "Informe 'cpf' e 'candidato_id'."}), 400

    eleitor = Eleitor.query.filter_by(cpf=cpf).first()
    if not eleitor:
        return jsonify({"erro": "CPF não cadastrado."}), 403

    if eleitor.votou:
        return jsonify({"erro": "Eleitor já votou."}), 403

    candidato = db.session.get(Candidato, candidato_id)
    if not candidato:
        return jsonify({"erro": "Candidato não encontrado."}), 404

    novo_voto = Voto(candidato_id=candidato.id)
    db.session.add(novo_voto)

    # Marca como votou
    eleitor.votou = True
    db.session.commit()

    return jsonify({"mensagem": f"Voto registrado para {candidato.nome}."}), 200


@routes.route("/resultados", methods=["GET"])
def resultados():
    resultados = (
        db.session.query(
            Candidato.id,
            Candidato.nome,
            func.count(Voto.id).label("votos")
        )
        .outerjoin(Voto, Voto.candidato_id == Candidato.id)
        .group_by(Candidato.id)
        .order_by(Candidato.id.asc())  # <-- Ordena por ID crescente
        .all()
    )

    resposta = [
        {"id": id, "nome": nome, "votos": votos}
        for id, nome, votos in resultados
    ]

    return Response(
        json.dumps({"resultados": resposta}, indent=2, ensure_ascii=False),
        mimetype="application/json"
    )


@routes.route("/candidatos", methods=["GET"])
def listar_candidatos():
    candidatos = Candidato.query.order_by(Candidato.id).all()
    return jsonify([{"id": c.id, "nome": c.nome} for c in candidatos])
