// frontend/js/ingredients.js

// Array to hold the local state (mirroring the database)
let ingredientsData = [];

// DOM Elements
const form = document.getElementById('ingredient-form');
const tbody = document.getElementById('ingredients-tbody');

// Handle Form Submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Capture the inputs based on the spreadsheet columns[cite: 1]
    const item = document.getElementById('item-name').value;
    const cost = parseFloat(document.getElementById('item-cost').value);
    const grams = parseFloat(document.getElementById('item-grams').value);
    
    // Calculate the $/G locally for immediate UI update[cite: 1]
    const costPerGram = cost / grams;

    const payload = {
        name: item,
        purchase_price: cost,
        total_grams: grams,
        cost_per_gram: costPerGram
    };

    // Note: Replace this with the actual fetch() call to the FastAPI backend 
    // try {
    //     const response = await fetch('http://localhost:8000/api/ingredients', { ... });
    // }

    // Simulating a successful backend save by adding to local state and re-rendering
    ingredientsData.push(payload);
    renderTable();
    form.reset();
});

// Render the data into the HTML table
function renderTable() {
    tbody.innerHTML = ''; // Clear existing rows

    ingredientsData.forEach(data => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${data.name}</td>
            <td>$${data.purchase_price.toFixed(2)}</td>
            <td>${data.total_grams.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 2 })}</td>
            <td>${data.cost_per_gram.toFixed(5)}</td>
        `;
        
        tbody.appendChild(row);
    });
}

// Initial render (this would normally be a GET request to fetch existing DB records)
renderTable();