from flask import Flask, request, jsonify, abort
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()
DATABASE_URL = os.getenv("POSTGRES_DSN")

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class NoteDB(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    date = Column(Date, nullable=False)

Base.metadata.create_all(bind=engine)

app = Flask(__name__)

@app.route("/notes/", methods=["POST"])
def create_note():
    data = request.get_json()
    if not data or "content" not in data or "date" not in data:
        abort(400, "Invalid request data")

    try:
        note_date = date.fromisoformat(data["date"])
    except ValueError:
        abort(400, "Invalid date format")

    db = SessionLocal()
    try:
        db_note = NoteDB(content=data["content"], date=note_date)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return jsonify({"id": db_note.id, "content": db_note.content, "date": str(db_note.date)}), 201
    finally:
        db.close()

@app.route("/notes/", methods=["GET"])
def get_notes():
    db = SessionLocal()
    try:
        notes = db.query(NoteDB).all()
        return jsonify([
            {"id": note.id, "content": note.content, "date": str(note.date)}
            for note in notes
        ])
    finally:
        db.close()

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    db = SessionLocal()
    try:
        db_note = db.query(NoteDB).filter(NoteDB.id == note_id).first()
        if not db_note:
            abort(404, "Note not found")
        db.delete(db_note)
        db.commit()
        return jsonify({"message": "Note deleted successfully"})
    finally:
        db.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)