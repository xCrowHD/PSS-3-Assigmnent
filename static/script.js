let calendar;
let selectedEventId = null;

document.addEventListener('DOMContentLoaded', function() {
  calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
    initialView: 'dayGridMonth',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    events: '/api/events',
    editable: true,
    eventClick: function(info) {
      selectedEventId = info.event.id;
      openEditModal(info.event);
    },
    eventDrop: async function(info) {
      await updateEvent(info.event);
      calendar.refetchEvents();
    },
    eventResize: async function(info) {
      await updateEvent(info.event);
      calendar.refetchEvents();
    },
    eventContent: function(info) {
      return {
        html: `
          <div class="fc-event-content">
            <b>${info.event.title}</b>
            ${info.event.extendedProps.description ? '<br>' + info.event.extendedProps.description : ''}
          </div>
        `
      };
    },
    eventDidMount: function(info) {
      info.el.style.backgroundColor = info.event.backgroundColor;
      info.el.style.borderColor = info.event.backgroundColor;
    }
  });
  calendar.render();

  // Aggiungi event listener per i bottoni colore
  document.querySelectorAll('.color-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      selectColor(this);
    });
  });

  // Aggiungi event listener per il form
  document.getElementById('eventForm').addEventListener('submit', function(e) {
    e.preventDefault();
    saveEvent();
  });
});

function openAddModal() {
  selectedEventId = null;
  document.getElementById('modalTitle').textContent = 'Nuovo Evento';
  document.getElementById('eventForm').reset();
  document.getElementById('deleteButton').style.display = 'none';
  const firstColorBtn = document.querySelector('.color-btn');
  selectColor(firstColorBtn);
  new bootstrap.Modal(document.getElementById('eventModal')).show();
}

function openEditModal(event) {
  document.getElementById('modalTitle').textContent = 'Modifica Evento';
  document.getElementById('eventId').value = event.id;
  document.getElementById('eventTitle').value = event.title;
  document.getElementById('eventStart').value = event.startStr.substring(0, 16);
  document.getElementById('eventEnd').value = event.end ? event.endStr.substring(0, 16) : '';
  document.getElementById('eventDescription').value = event.extendedProps.description || '';
  document.getElementById('deleteButton').style.display = 'block';

  // Seleziona il colore corrente
  const currentColor = event.backgroundColor || '#a8d8ea';
  document.getElementById('eventColor').value = currentColor;
  const colorBtn = document.querySelector(`.color-btn[data-color="${currentColor}"]`);
  if (colorBtn) selectColor(colorBtn);

  new bootstrap.Modal(document.getElementById('eventModal')).show();
}

async function saveEvent() {
  const eventData = {
    title: document.getElementById('eventTitle').value,
    start: document.getElementById('eventStart').value,
    end: document.getElementById('eventEnd').value || null,
    description: document.getElementById('eventDescription').value,
    color: document.getElementById('eventColor').value
  };

  const url = selectedEventId ? `/api/events/${selectedEventId}` : '/api/events';
  const method = selectedEventId ? 'PUT' : 'POST';

  try {
    const response = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(eventData)
    });
    
    if (!response.ok) throw new Error('Errore nel salvataggio');
    
    calendar.refetchEvents();
    bootstrap.Modal.getInstance(document.getElementById('eventModal')).hide();
  } catch (error) {
    console.error("Errore:", error);
    alert("Si è verificato un errore durante il salvataggio");
  }
}

async function updateEvent(event) {
  try {
    const response = await fetch(`/api/events/${event.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: event.title,
        start: event.start.toISOString(),
        end: event.end?.toISOString() || null,
        description: event.extendedProps.description,
        color: event.backgroundColor
      })
    });
    
    if (!response.ok) throw new Error('Errore nell\'aggiornamento');
    
    return await response.json();
  } catch (error) {
    console.error("Errore:", error);
    alert("Si è verificato un errore durante l'aggiornamento");
    throw error;
  }
}

function deleteEvent() {
  if (selectedEventId && confirm('Sei sicuro di voler eliminare questo evento?')) {
    fetch(`/api/events/${selectedEventId}`, { method: 'DELETE' })
      .then(response => {
        if (response.ok) {
          calendar.refetchEvents();
          bootstrap.Modal.getInstance(document.getElementById('eventModal')).hide();
        }
      });
  }
}

function selectColor(btn) {
  document.querySelectorAll('.color-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  document.getElementById('eventColor').value = btn.dataset.color;
}