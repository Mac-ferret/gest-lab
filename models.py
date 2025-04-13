from flask import Blueprint, request, jsonify
from .models import db, Fascicolo
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('main', __name__)

# Route GET per tutti i fascicoli
@bp.route("/api/fascicoli", methods=["GET"])
def get_fascicoli():
    fascicoli = Fascicolo.query.order_by(Fascicolo.id).all()
    return jsonify([f.to_dict() for f in fascicoli])

# Route POST per creare un nuovo fascicolo
@bp.route("/api/fascicoli", methods=["POST"])
def create_fascicolo():
    data = request.json
    try:
        nuovo_fascicolo = Fascicolo.from_dict(data)
        db.session.add(nuovo_fascicolo)
        db.session.commit()
        return jsonify(nuovo_fascicolo.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

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
