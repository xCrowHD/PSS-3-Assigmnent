from flask import Flask, render_template
from model import create_tables, DATABASE
import os

app = Flask(__name__)

# Importa le route dal controller
from controller import configure_routes
configure_routes(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Se il database non esiste, crea le tabelle
    if not os.path.exists(DATABASE):
        create_tables()
    
    app.run(debug=True)
