from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do MySQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pw@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o SQLAlchemy
db = SQLAlchemy(app)

# Modelo do Banco de Dados
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Message {self.name}>'

# Criando o Banco de Dados
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/send', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Salvando a mensagem no banco de dados
    new_message = Message(name=name, email=email, message=message)
    db.session.add(new_message)
    db.session.commit()

    # Redirecionar para a página de confirmação passando os dados
    return redirect(url_for('message_received', message=message))

@app.route('/message_received')
def message_received():
    message = request.args.get('message')
    return render_template('message_received.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
