from flask import Flask, render_template
from model import create_table, DATABASE  # Importa DATABASE
import os  # Importa il modulo os per verificare l'esistenza del file

app = Flask(__name__)

# Importa le route dal controller
from controller import configure_routes
configure_routes(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Verifica se il database esiste
    if not os.path.exists(DATABASE):
        create_table()
    
    app.run(debug=True)