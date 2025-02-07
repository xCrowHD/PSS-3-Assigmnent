let calendar;
let selectedEventId = null;
let studyChart;

document.addEventListener('DOMContentLoaded', function() {
  // Inizializza il calendario
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
    datesSet: function(info) {
      updateStudyChart();
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

  // Aggiungi event listener per il form dell'evento
  document.getElementById('eventForm').addEventListener('submit', function(e) {
    e.preventDefault();
    saveEvent();
  });

  // Carica le categorie per il dropdown e la sidebar
  loadCategories();

  // Gestione del form per aggiungere categoria
  document.getElementById('categoryForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const name = document.getElementById('newCategory').value.trim();
    if (!name) return;
    try {
      const response = await fetch('/api/categories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name })
      });
      if (response.ok) {
        document.getElementById('newCategory').value = '';
        loadCategories();
      }
    } catch (error) {
      console.error('Errore nell\'aggiunta della categoria', error);
    }
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

  // Imposta la categoria selezionata nel dropdown
  const eventCategory = event.extendedProps.category;
  const select = document.getElementById('eventCategory');
  if (eventCategory) {
    for (let option of select.options) {
      if (option.textContent === eventCategory) {
        select.value = option.value;
        break;
      }
    }
  } else {
    select.value = "";
  }

  new bootstrap.Modal(document.getElementById('eventModal')).show();
}

async function saveEvent() {
  const eventData = {
    title: document.getElementById('eventTitle').value,
    start: document.getElementById('eventStart').value,
    end: document.getElementById('eventEnd').value || null,
    description: document.getElementById('eventDescription').value,
    color: document.getElementById('eventColor').value,
    category_id: document.getElementById('eventCategory').value || null
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
        start: event.start.toISOString().slice(0, 16),
        end: event.end?.toISOString().slice(0, 16) || null,
        description: event.extendedProps.description,
        color: event.backgroundColor,
        category_id: event.extendedProps.category_id || null
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

async function loadCategories() {
  try {
    const response = await fetch('/api/categories');
    const categories = await response.json();
    // Popola il dropdown per la selezione categoria nel form evento
    const select = document.getElementById('eventCategory');
    select.innerHTML = '<option value="">Seleziona categoria</option>';
    categories.forEach(cat => {
      const option = document.createElement('option');
      option.value = cat.id;
      option.textContent = cat.name;
      select.appendChild(option);
    });
    // Popola la lista nella sidebar
    const catList = document.getElementById('categoryList');
    if (catList) {
      catList.innerHTML = '';
      categories.forEach(cat => {
        const li = document.createElement('li');
        li.textContent = cat.name;
        li.className = 'list-group-item';
        catList.appendChild(li);
      });
    }
  } catch (error) {
    console.error('Errore nel caricamento delle categorie', error);
  }
}

function updateStudyChart() {
  // Imposta l'endpoint per ottenere i dati aggregati per categoria
  let endpoint = '/api/study_summary';

  // Ottieni le date di inizio e fine della vista corrente
  const activeStart = calendar.view.activeStart.toISOString().split('T')[0];
  const activeEnd = calendar.view.activeEnd.toISOString().split('T')[0];
  console.log("----------------");
  console.log(activeStart);
  console.log(activeEnd);

  // Fai la richiesta per ottenere i dati
  fetch(`${endpoint}?start=${activeStart}&end=${activeEnd}`)
    .then(response => response.json())
    .then(data => {
      // Prepara i dati per il grafico a torta
      const categories = Object.keys(data);  // Le categorie (come filosofia, storia, ecc.)
      const hours = categories.map(category => data[category]);  // Le ore corrispondenti ad ogni categoria

      // Se il grafico esiste già, aggiorna i dati
      if (studyChart) {
        studyChart.data.labels = categories;
        studyChart.data.datasets[0].data = hours;
        studyChart.update();
      } else {
        // Crea un nuovo grafico a torta
        const ctx = document.getElementById('studyChart').getContext('2d');
        studyChart = new Chart(ctx, {
          type: 'pie',
          data: {
            labels: categories,
            datasets: [{
              label: 'Ore di studio per categoria',
              data: hours,
              backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(153, 102, 255, 0.6)', 'rgba(255, 159, 64, 0.6)', 
                                 'rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)', 'rgba(255, 205, 86, 0.6)']
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'top',
              },
              tooltip: {
                callbacks: {
                  label: function(tooltipItem) {
                    return tooltipItem.label + ': ' + tooltipItem.raw + ' ore';
                  }
                }
              }
            }
          }
        });
      }
    });
}

