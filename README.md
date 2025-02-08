# Planner di Studio - MVC

## Struttura del Progetto
```
/static/
  ├── script.js
  ├── style.css
/templates/
  ├── index.html
backend.py
controller.py
model.py
```

## Introduzione
L'applicazione sviluppata è un planner di studio progettato seguendo l'architettura **Model-View-Controller (MVC)**. Questo sistema permette agli utenti di organizzare e gestire le proprie sessioni di studio attraverso un'interfaccia interattiva basata su un calendario, con la possibilità di categorizzare eventi e visualizzare statistiche sulle ore di studio.

## Architettura MVC
L'architettura dell'applicazione è suddivisa in tre componenti principali:
- **Model:** Gestisce l'accesso ai dati e le operazioni sul database.
- **View:** Si occupa dell'interfaccia utente e della presentazione dei dati.
- **Controller:** Contiene la logica dell'applicazione e gestisce le richieste dell'utente.

## Componenti principali

### Model (`model.py`)
Il modello gestisce:
- La connessione al database SQLite.
- La creazione delle tabelle necessarie per memorizzare gli eventi di studio e le categorie.
- Le operazioni CRUD (Create, Read, Update, Delete) sugli eventi e sulle categorie.
- Il calcolo delle ore di studio suddivise per categoria.

### View (`index.html`)
La parte **View** utilizza:
- **FullCalendar** per la gestione del calendario.
- **Bootstrap** per migliorare il layout e l'usabilità.
- **Chart.js** per la visualizzazione delle statistiche di studio.
- Un **modale** per aggiungere e modificare gli eventi.

### Controller (`controller.py`)
Il **Controller** gestisce:
- Le API RESTful per il recupero, l'aggiunta, la modifica e l'eliminazione di eventi.
- La gestione delle categorie.
- Il calcolo delle ore totali di studio suddivise per categoria.

Il file `backend.py` si occupa di:
- Configurare l'app Flask.
- Includere e avviare le rotte definite nel controller.
- Gestire la creazione delle tabelle del database se non esistono.
- Avviare il server.

## Funzionalità dell'Applicazione
- **Aggiunta di eventi di studio** con titolo, data e categoria.
- **Gestione delle categorie** per organizzare meglio le sessioni di studio.
- **Modifica ed eliminazione degli eventi**.
- **Visualizzazione delle statistiche** sulle ore di studio per categoria.
- **Calcolo delle ore totali di studio per categoria** in un determinato intervallo di tempo.
- **Interazione con il backend tramite API RESTful**, consentendo future integrazioni con altre applicazioni o frontend.

## Tecnologie Utilizzate
- **Flask** per il backend.
- **SQLite** per la memorizzazione dei dati.
- **FullCalendar** per la gestione del calendario.
- **Bootstrap** per la grafica e la responsività.
- **Chart.js** per i grafici delle statistiche.
- **API RESTful** per la comunicazione tra frontend e backend.

## Installazione e Avvio
1. Clonare il repository:
   ```sh
   git clone https://github.com/tuo-repo/planner-mvc.git
   cd planner-mvc
   ```
2. Installare le dipendenze:
   ```sh
   pip install flask
   ```
3. Avviare il server Flask:
   ```sh
   python backend.py
   ```
4. Aprire il browser e accedere a `http://127.0.0.1:5000`

## Conclusioni
L'applicazione è strutturata in modo modulare seguendo il pattern MVC, il che permette una separazione chiara tra dati, logica e interfaccia utente. Grazie all'uso di tecnologie moderne, il planner di studio offre un'esperienza utente interattiva e funzionale.

## Possibili miglioramenti futuri
- Aggiunta di un sistema di notifiche.
- Sincronizzazione con Google Calendar.
- Miglioramento della gestione degli utenti con autenticazione.

---

Questa bozza ti sembra adatta? Vuoi aggiungere o modificare qualcosa?

