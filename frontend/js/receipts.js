const uploadBtn = document.getElementById('upload-receipt-btn');
const receiptInput = document.getElementById('receipt-upload');
const receiptDateInput = document.getElementById('receipt-date');
const receiptVendorInput = document.getElementById('receipt-vendor');
const reviewSection = document.getElementById('receipt-review-section');
const reviewTbody = document.getElementById('receipt-review-tbody');
const confirmImportBtn = document.getElementById('confirm-import-btn');

let parsedReceiptItems = [];

// Default the date picker to today
receiptDateInput.valueAsDate = new Date();

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
            
            // 🚨 DEBUGGING OUTPUT: PRINT TO BROWSER CONSOLE 🚨
            console.log("=== RAW PDF TEXT FROM BACKEND ===");
            console.log(data.raw_text_debug);
            
            parsedReceiptItems = data.items;
            receiptVendorInput.value = data.vendor || "";
            renderReviewTable();
            reviewSection.classList.remove('hidden');
        } else { 
            const err = await response.json();
            alert(`Failed to parse receipt: ${err.detail}`); 
        }
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
            <td>
                <select class="table-input" style="width: 60px;" id="rev-unit-type-${index}">
                    <option value="g" ${item.unit_measure === 'g' ? 'selected' : ''}>g</option>
                    <option value="ea" ${item.unit_measure === 'ea' ? 'selected' : ''}>ea</option>
                </select>
            </td>
            <td><input type="number" step="any" class="table-input" placeholder="Units per item" value="${item.grams_per_unit}" id="rev-units-${index}"></td>
        `;
        reviewTbody.appendChild(tr);
    });
}

confirmImportBtn.addEventListener('click', async () => {
    const checkboxes = document.querySelectorAll('.import-check:checked');
    const itemsToSave = [];
    const receiptDate = receiptDateInput.value;
    const vendor = receiptVendorInput.value || "Unknown Vendor";
    let validationFailed = false;

    if (!receiptDate) return alert("Please select a date for the receipt.");

    checkboxes.forEach(cb => {
        const index = cb.getAttribute('data-index');
        const name = document.getElementById(`rev-name-${index}`).value;
        const totalPrice = parseFloat(document.getElementById(`rev-price-${index}`).value);
        const receiptQty = parseInt(document.getElementById(`rev-qty-${index}`).value) || 1;
        const itemsPerPack = parseInt(document.getElementById(`rev-pack-${index}`).value) || 1;
        const unitType = document.getElementById(`rev-unit-type-${index}`).value;
        const unitsPerItem = parseFloat(document.getElementById(`rev-units-${index}`).value);

        if (!unitsPerItem || unitsPerItem <= 0) {
            validationFailed = true;
            document.getElementById(`rev-units-${index}`).style.borderColor = "red";
        }

        const totalItems = receiptQty * itemsPerPack;
        const unitPrice = totalPrice / totalItems;

        itemsToSave.push({
            name: name.replace(/,\s*\d+\s*(pk|pack).*/i, ''),
            vendor: vendor,
            unit_price: unitPrice,       
            total_price: totalPrice,     
            total_units: unitsPerItem,
            unit_measure: unitType
        });
    });

    if (validationFailed) return alert("Please enter Total Units/Grams for all checked items.");
    if (itemsToSave.length === 0) return alert("No items selected.");

    confirmImportBtn.innerText = "Saving to Ledgers...";

    for (const payload of itemsToSave) {
        // 1. Write Unit Pricing to Ingredients
        await fetch('/api/ingredients/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: payload.name,
                vendor: payload.vendor,
                purchase_price: payload.unit_price,
                total_units: payload.total_units,
                unit_measure: payload.unit_measure
            })
        });

        // 2. Write Ledger Total to Expenses
        await fetch('/api/expenses/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                date: receiptDate,
                item_name: `${payload.name} (${payload.vendor})`,
                category: "Ingredient",
                cost: payload.total_price
            })
        });
    }

    reviewSection.classList.add('hidden');
    receiptInput.value = "";
    confirmImportBtn.innerText = "Confirm & Add to Ledgers";
    
    // Ping other scripts to refresh their tables in the background
    window.dispatchEvent(new Event('refreshIngredients'));
    window.dispatchEvent(new Event('refreshExpenses'));
    alert("Receipt successfully imported to Ingredients and Expenses!");
});