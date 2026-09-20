const products = {
    hc_loaf: { name: "Herbes & Cheddar Loaf", price: 12.00, cogs: 2.17, packaging: 0.15, tax_rate: 0.08 },
    cc_loaf: { name: "Cinnamon Cardamom Loaf", price: 9.00, cogs: 1.25, packaging: 0.15, tax_rate: 0.08 },
    hc_roll: { name: "H&C Hand Roll", price: 5.00, cogs: 0.90, packaging: 0.31, tax_rate: 0.08 },
    cc_roll: { name: "C&C Hand Roll", price: 5.00, cogs: 0.41, packaging: 0.31, tax_rate: 0.08 },
    sc_roll: { name: "S&C Hand Roll", price: 5.00, cogs: 1.11, packaging: 0.31, tax_rate: 0.08 },
    cg_cookie: { name: "Chewy Ginger Pack", price: 5.00, cogs: 0.55, packaging: 0.13, tax_rate: 0.08 },
    ss_cookie: { name: "Sugar Sprinkle Pack", price: 5.00, cogs: 0.52, packaging: 0.13, tax_rate: 0.08 },
    vcc_cookie: { name: "Vegan CC Pack", price: 5.00, cogs: 0.70, packaging: 0.13, tax_rate: 0.08 }
};

const marketTbody = document.getElementById('market-tbody');
let currentTotals = {};

function initTable() {
    marketTbody.innerHTML = '';
    for (const [key, p] of Object.entries(products)) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${p.name}</td>
            <td><input type="number" min="0" value="0" class="table-input qty-made" data-key="${key}"></td>
            <td><input type="number" min="0" value="0" class="table-input qty-sold" data-key="${key}"></td>
            <td class="row-rev">$0.00</td>
            <td class="row-cost">$0.00</td>
            <td class="row-profit"><strong>$0.00</strong></td>
        `;
        marketTbody.appendChild(tr);
    }
    
    document.querySelectorAll('.table-input').forEach(input => {
        input.addEventListener('input', calculateLedger);
    });
}

function calculateLedger() {
    let totals = { made: 0, sold: 0, revenue: 0, cost: 0, profit: 0, items: [] };

    marketTbody.querySelectorAll('tr').forEach(tr => {
        const madeInput = tr.querySelector('.qty-made');
        const soldInput = tr.querySelector('.qty-sold');
        const key = madeInput.getAttribute('data-key');
        
        const madeQty = parseInt(madeInput.value) || 0;
        const soldQty = parseInt(soldInput.value) || 0;
        const p = products[key];

        const cost = madeQty * (p.cogs + p.packaging);
        const rev = soldQty * p.price;
        const tax = rev * p.tax_rate;
        const profit = rev - cost - tax;

        tr.querySelector('.row-rev').innerText = `$${rev.toFixed(2)}`;
        tr.querySelector('.row-cost').innerText = `$${cost.toFixed(2)}`;
        tr.querySelector('.row-profit').innerHTML = `<strong>$${profit.toFixed(2)}</strong>`;

        if (madeQty > 0 || soldQty > 0) {
            totals.items.push({ item_key: key, made_qty: madeQty, sold_qty: soldQty });
        }

        totals.made += madeQty;
        totals.sold += soldQty;
        totals.revenue += rev;
        totals.cost += cost;
        totals.profit += profit;
    });

    document.getElementById('total-made').innerText = totals.made;
    document.getElementById('total-sold').innerText = totals.sold;
    document.getElementById('total-revenue').innerText = `$${totals.revenue.toFixed(2)}`;
    document.getElementById('total-cost').innerText = `$${totals.cost.toFixed(2)}`;
    document.getElementById('total-profit').innerText = `$${totals.profit.toFixed(2)}`;
    
    currentTotals = totals;
}

document.getElementById('save-event-btn').addEventListener('click', async () => {
    const eventName = document.getElementById('event-name').value;
    const eventDate = document.getElementById('event-date').value;

    if (!eventName || !eventDate) {
        alert("Please enter an Event Name and Date.");
        return;
    }

    const payload = {
        event_name: eventName,
        event_date: eventDate,
        items: currentTotals.items,
        total_revenue: currentTotals.revenue,
        total_cost: currentTotals.cost,
        total_profit: currentTotals.profit
    };

    try {
        const response = await fetch('/api/markets/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            document.getElementById('save-status').innerText = "Event saved successfully!";
            setTimeout(() => { document.getElementById('save-status').innerText = ""; }, 3000);
        } else {
            console.error("Failed to save event");
        }
    } catch (error) {
        console.error("Connection error:", error);
    }
});

document.addEventListener('DOMContentLoaded', initTable);