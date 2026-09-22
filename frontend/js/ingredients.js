let ingredientsData = [];
let editingId = null;

const form = document.getElementById('ingredient-form');
const tbody = document.getElementById('ingredients-tbody');
const submitBtn = document.querySelector('#ingredient-form button[type="submit"]');

// Listen for receipt imports to trigger a refresh
window.addEventListener('refreshIngredients', fetchIngredients);

async function fetchIngredients() {
    try {
        const response = await fetch('/api/ingredients/');
        if (response.ok) {
            ingredientsData = await response.json();
            renderTable();
            window.dispatchEvent(new CustomEvent('catalogUpdated', { detail: ingredientsData }));
        }
    } catch (error) { console.error("Error:", error); }
}

function renderTable() {
    tbody.innerHTML = ''; 
    ingredientsData.forEach(data => {
        // Fallbacks for legacy database entries to prevent .toLocaleString() crashes
        const totalUnits = data.total_units !== undefined ? data.total_units : (data.total_grams || 0);
        const unitCost = data.cost_per_unit !== undefined ? data.cost_per_unit : (data.cost_per_gram || 0);
        const vendorName = data.vendor || 'Unknown';
        const unitMeasure = data.unit_measure || 'g';

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${data.name}</td>
            <td>${vendorName}</td>
            <td>$${data.purchase_price.toFixed(2)}</td>
            <td>${totalUnits.toLocaleString(undefined, { maximumFractionDigits: 2 })} ${unitMeasure}</td>
            <td>$${unitCost.toFixed(5)} / ${unitMeasure}</td>
            <td>
                <button onclick="editIngredient('${data._id}', '${data.name.replace(/'/g, "\\'")}', '${vendorName.replace(/'/g, "\\'")}', ${data.purchase_price}, ${totalUnits}, '${unitMeasure}')" class="btn-secondary" style="margin-top:0; padding: 4px 8px;">Edit</button>
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
        vendor: document.getElementById('item-vendor').value,
        purchase_price: parseFloat(document.getElementById('item-cost').value),
        total_units: parseFloat(document.getElementById('item-units').value),
        unit_measure: document.getElementById('item-unit-type').value
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
        } else {
            const err = await response.json();
            alert(`Failed: ${err.detail}`);
        }
    } catch (error) { console.error("Error:", error); }
});

window.editIngredient = (id, name, vendor, price, units, measure) => {
    document.getElementById('item-name').value = name;
    document.getElementById('item-vendor').value = vendor;
    document.getElementById('item-cost').value = price;
    document.getElementById('item-units').value = units;
    document.getElementById('item-unit-type').value = measure;
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

document.addEventListener('DOMContentLoaded', fetchIngredients);