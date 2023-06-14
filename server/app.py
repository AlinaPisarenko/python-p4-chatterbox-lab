from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import desc


from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

print(app.json.compact)

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.get('/messages')
def get_messages():
    messages = Message.query.order_by(desc('created_at'))
    return [msg.to_dict() for msg in messages]

@app.post('/messages')
def create_message():
    message = Message(**request.json)
    db.session.add(message)
    db.session.commit()
    return message.to_dict(), 201

@app.patch('/messages/<int:id>')
def update_message(id):
    message = Message.query.get_or_404(id)
    print(message)
    print(request.json['body'])
    if 'body' in request.json:
        message.body = request.json['body']
    db.session.commit()
    return message.to_dict(), 200

@app.delete('/messages/<int:id>')
def delete_messages(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return ''

if __name__ == '__main__':
    app.run(port=5555)
