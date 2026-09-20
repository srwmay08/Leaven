let ingredientsData = [];
let editingId = null;

const form = document.getElementById('ingredient-form');
const tbody = document.getElementById('ingredients-tbody');
const submitBtn = document.querySelector('#ingredient-form button[type="submit"]');

async function fetchIngredients() {
    try {
        const response = await fetch('/api/ingredients/');
        if (response.ok) {
            ingredientsData = await response.json();
            renderTable();
            // Broadcast update to recipes
            window.dispatchEvent(new CustomEvent('catalogUpdated', { detail: ingredientsData }));
        }
    } catch (error) { console.error("Error:", error); }
}

function renderTable() {
    tbody.innerHTML = ''; 
    ingredientsData.forEach(data => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${data.name}</td>
            <td>$${data.purchase_price.toFixed(2)}</td>
            <td>${data.total_grams.toLocaleString(undefined, { maximumFractionDigits: 2 })}</td>
            <td>${data.cost_per_gram.toFixed(5)}</td>
            <td>
                <button onclick="editIngredient('${data._id}', '${data.name.replace(/'/g, "\\'")}', ${data.purchase_price}, ${data.total_grams})" class="btn-secondary" style="margin-top:0; padding: 4px 8px;">Edit</button>
                <button onclick="deleteIngredient('${data._id}')" class="btn-primary" style="margin-top:0; padding: 4px 8px; background-color: #e74c3c;">X</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        name: document.getElementById('item-name').value,
        purchase_price: parseFloat(document.getElementById('item-cost').value),
        total_grams: parseFloat(document.getElementById('item-grams').value)
    };

    const url = editingId ? `/api/ingredients/${editingId}` : '/api/ingredients/';
    const method = editingId ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (response.ok) {
            fetchIngredients();
            form.reset();
            editingId = null;
            submitBtn.innerText = "Save Ingredient";
        }
    } catch (error) { console.error("Error:", error); }
});

window.editIngredient = (id, name, price, grams) => {
    document.getElementById('item-name').value = name;
    document.getElementById('item-cost').value = price;
    document.getElementById('item-grams').value = grams;
    editingId = id;
    submitBtn.innerText = "Update Ingredient";
    window.scrollTo({ top: document.getElementById('item-name').offsetTop - 50, behavior: 'smooth' });
};

window.deleteIngredient = async (id) => {
    if (!confirm("Delete this ingredient?")) return;
    try {
        const response = await fetch(`/api/ingredients/${id}`, { method: 'DELETE' });
        if (response.ok) fetchIngredients();
    } catch (error) { console.error("Delete error:", error); }
};

// --- PDF Parsing & Pack Logic ---
const uploadBtn = document.getElementById('upload-receipt-btn');
const receiptInput = document.getElementById('receipt-upload');
const reviewSection = document.getElementById('receipt-review-section');
const reviewTbody = document.getElementById('receipt-review-tbody');
const confirmImportBtn = document.getElementById('confirm-import-btn');

let parsedReceiptItems = [];

uploadBtn.addEventListener('click', async () => {
    const file = receiptInput.files[0];
    if (!file) return alert("Select a PDF file first.");

    const formData = new FormData();
    formData.append("file", file);
    uploadBtn.innerText = "Scanning...";
    
    try {
        const response = await fetch('/api/receipts/parse', { method: 'POST', body: formData });
        if (response.ok) {
            const data = await response.json();
            parsedReceiptItems = data.items;
            renderReviewTable();
            reviewSection.classList.remove('hidden');
        } else { alert("Failed to parse receipt."); }
    } catch (error) { console.error(error); } 
    finally { uploadBtn.innerText = "Scan Receipt"; }
});

function renderReviewTable() {
    reviewTbody.innerHTML = '';
    
    parsedReceiptItems.forEach((item, index) => {
        const isLikelyPersonal = /tissue|wiper|paper|cleaner|detergent/i.test(item.name);
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="text-align: center;">
                <input type="checkbox" class="import-check" data-index="${index}" ${!isLikelyPersonal ? 'checked' : ''}>
            </td>
            <td><input type="text" class="table-input" style="width: 100%;" value="${item.name}" id="rev-name-${index}"></td>
            <td><input type="number" step="0.01" class="table-input" style="width: 60px;" value="${item.purchase_price}" id="rev-price-${index}"></td>
            <td><input type="number" min="1" class="table-input" style="width: 50px;" value="${item.receipt_qty}" id="rev-qty-${index}"></td>
            <td><input type="number" min="1" class="table-input" style="width: 50px;" value="${item.packs}" id="rev-pack-${index}"></td>
            <td><input type="number" step="any" class="table-input" placeholder="Grams PER ITEM" value="${item.grams_per_unit}" id="rev-grams-${index}"></td>
        `;
        reviewTbody.appendChild(tr);
    });
}

confirmImportBtn.addEventListener('click', async () => {
    const checkboxes = document.querySelectorAll('.import-check:checked');
    const itemsToSave = [];
    let validationFailed = false;

    checkboxes.forEach(cb => {
        const index = cb.getAttribute('data-index');
        const name = document.getElementById(`rev-name-${index}`).value;
        const totalPrice = parseFloat(document.getElementById(`rev-price-${index}`).value);
        const receiptQty = parseInt(document.getElementById(`rev-qty-${index}`).value) || 1;
        const itemsPerPack = parseInt(document.getElementById(`rev-pack-${index}`).value) || 1;
        const gramsPerItem = parseFloat(document.getElementById(`rev-grams-${index}`).value);

        if (!gramsPerItem || gramsPerItem <= 0) {
            validationFailed = true;
            document.getElementById(`rev-grams-${index}`).style.borderColor = "red";
        }

        // Divide to find the true cost of exactly 1 unit
        const totalItems = receiptQty * itemsPerPack;
        const unitPrice = totalPrice / totalItems;

        itemsToSave.push({
            name: name.replace(/,\s*\d+\s*(pk|pack).*/i, ''),
            purchase_price: unitPrice,
            total_grams: gramsPerItem
        });
    });

    if (validationFailed) return alert("Please enter Grams Per Item for all checked items.");
    if (itemsToSave.length === 0) return alert("No items selected.");

    confirmImportBtn.innerText = "Saving...";

    for (const payload of itemsToSave) {
        await fetch('/api/ingredients/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
    }

    reviewSection.classList.add('hidden');
    receiptInput.value = "";
    confirmImportBtn.innerText = "Confirm & Add to Ingredients";
    fetchIngredients(); 
});

document.addEventListener('DOMContentLoaded', fetchIngredients);