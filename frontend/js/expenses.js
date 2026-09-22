let expensesData = [];

const expenseForm = document.getElementById('expense-form');
const expensesTbody = document.getElementById('expenses-tbody');

// Set default date to today
document.getElementById('expense-date').valueAsDate = new Date();

async function fetchExpenses() {
    try {
        const response = await fetch('/api/expenses/');
        if (response.ok) {
            expensesData = await response.json();
            renderExpensesTable();
        }
    } catch (error) { console.error("Error:", error); }
}

function renderExpensesTable() {
    expensesTbody.innerHTML = ''; 
    expensesData.forEach(data => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${data.date}</td>
            <td>${data.item_name}</td>
            <td>${data.category}</td>
            <td>$${data.cost.toFixed(2)}</td>
            <td>
                <button onclick="deleteExpense('${data._id}')" class="btn-primary" style="margin-top:0; padding: 4px 8px; background-color: #e74c3c;">X</button>
            </td>
        `;
        expensesTbody.appendChild(row);
    });
}

expenseForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
        date: document.getElementById('expense-date').value,
        item_name: document.getElementById('expense-name').value,
        category: document.getElementById('expense-category').value,
        cost: parseFloat(document.getElementById('expense-cost').value)
    };

    try {
        const response = await fetch('/api/expenses/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            fetchExpenses();
            expenseForm.reset();
            document.getElementById('expense-date').valueAsDate = new Date();
        }
    } catch (error) { console.error("Error:", error); }
});

window.deleteExpense = async (id) => {
    if (!confirm("Delete this expense record?")) return;
    try {
        const response = await fetch(`/api/expenses/${id}`, { method: 'DELETE' });
        if (response.ok) fetchExpenses();
    } catch (error) { console.error("Delete error:", error); }
};

window.addEventListener('refreshExpenses', fetchExpenses);

document.addEventListener('DOMContentLoaded', fetchExpenses);