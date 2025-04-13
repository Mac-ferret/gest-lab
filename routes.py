from flask import Blueprint, request, jsonify
from .models import db, Fascicolo
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

bp = Blueprint('main', __name__)

# Route GET per tutti i fascicoli
@bp.route("/api/fascicoli", methods=["GET"])
def get_fascicoli():
    fascicoli = Fascicolo.query.order_by(Fascicolo.id).all()
    return jsonify([f.to_dict() for f in fascicoli])

# Route POST per creare un nuovo fascicolo
@bp.route("/fascicoli", methods=["POST"])
def crea_fascicolo():
    data = request.json

    # Usa data_apertura o data corrente
    data_apertura = data.get("data_apertura")
    if data_apertura:
        apertura = datetime.strptime(data_apertura, "%Y-%m-%d").date()
    else:
        apertura = date.today()

    anno = apertura.year
    mese = apertura.month
    trimestre = (mese - 1) // 3 + 1

    # Conta quanti fascicoli esistono per quel trimestre e anno
    esistenti = Fascicolo.query.filter(
        db.extract("year", Fascicolo.data_apertura) == anno,
        ((db.extract("month", Fascicolo.data_apertura) - 1) // 3 + 1) == trimestre
    ).count()

    numero_progressivo = esistenti + 1
    progressivo = f"{trimestre:02d}/{anno}-{numero_progressivo}"

    # Crea fascicolo con progressivo
    nuovo_fascicolo = Fascicolo.from_dict(data)
    nuovo_fascicolo.progressivo = progressivo

    db.session.add(nuovo_fascicolo)
    db.session.commit()

    return jsonify(nuovo_fascicolo.to_dict()), 201


# Route PUT per aggiornare un fascicolo
@bp.route("/api/fascicoli/<int:id>", methods=["PUT"])
def update_fascicolo(id):
    fascicolo = Fascicolo.query.get_or_404(id)
    data = request.json
    try:
        for key, value in data.items():
            if hasattr(fascicolo, key):
                setattr(fascicolo, key, value)
        db.session.commit()
        return jsonify(fascicolo.to_dict())
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Route DELETE per eliminare un fascicolo
@bp.route("/api/fascicoli/<int:id>", methods=["DELETE"])
def delete_fascicolo(id):
    fascicolo = Fascicolo.query.get_or_404(id)
    try:
        db.session.delete(fascicolo)
        db.session.commit()
        return jsonify({"message": "Fascicolo eliminato."})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
