from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "auditoria_mysql")
DB_NAME = os.getenv("DB_NAME", "auditoria_db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Audit(db.Model):
    __tablename__ = 'audits'
    id = db.Column(db.Integer, primary_key=True)
    actor = db.Column(db.String(128), nullable=False)
    action = db.Column(db.String(128), nullable=False)
    detail = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "actor": self.actor,
            "action": self.action,
            "detail": self.detail,
            "created_at": self.created_at.isoformat()
        }

@app.before_first_request
def init_db():
    db.create_all()

LOG_FILE = "/var/log/auditoria.log"

def append_log_line(entry: str):
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(entry + "\n")
    except Exception:
        # no crashes on logging failures
        pass

@app.route("/audit", methods=["POST"])
def audit():
    data = request.get_json(force=True)
    actor = data.get("actor", "unknown")
    action = data.get("action", "unknown")
    detail = data.get("detail", "")
    ts = data.get("timestamp") or datetime.utcnow().isoformat()

    record = Audit(actor=actor, action=action, detail=detail)
    db.session.add(record)
    db.session.commit()

    log_line = f"{ts} | actor={actor} | action={action} | detail={detail}"
    append_log_line(log_line)

    return jsonify({"status": "ok", "id": record.id}), 201

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))