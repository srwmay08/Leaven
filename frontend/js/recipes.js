let currentRecipeIngredients = [];
let globalCatalog = [];
let savedRecipes = [];
let editingRecipeId = null;

// Listen for updates from ingredients.js so dropdowns stay accurate
window.addEventListener('catalogUpdated', (e) => {
    globalCatalog = e.detail;
    renderRecipeTable(); // Recalculate existing rows immediately if prices changed
});

document.addEventListener('DOMContentLoaded', () => {
    const tbody = document.getElementById('recipe-tbody');
    const savedRecipesTbody = document.getElementById('saved-recipes-tbody');
    const addBtn = document.getElementById('add-ingredient-btn');
    const saveBtn = document.getElementById('save-recipe-btn');
    const clearBtn = document.getElementById('clear-recipe-btn');

    // --- 1. Fetch & Render Saved Recipes ---
    async function fetchRecipes() {
        try {
            const response = await fetch('/api/recipes/');
            if (response.ok) {
                savedRecipes = await response.json();
                renderSavedRecipes();
            }
        } catch (error) { console.error("Error fetching recipes:", error); }
    }

    function renderSavedRecipes() {
        savedRecipesTbody.innerHTML = '';
        savedRecipes.forEach(recipe => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${recipe.name}</strong></td>
                <td>${recipe.yield_qty}</td>
                <td>
                    <button onclick="editRecipe('${recipe._id}')" class="btn-secondary" style="margin-top:0; padding: 4px 8px;">Edit</button>
                    <button onclick="deleteRecipe('${recipe._id}')" class="btn-primary" style="margin-top:0; padding: 4px 8px; background-color: #e74c3c;">X</button>
                </td>
            `;
            savedRecipesTbody.appendChild(tr);
        });
    }

    window.editRecipe = (id) => {
        const recipe = savedRecipes.find(r => r._id === id);
        if (!recipe) return;
        
        editingRecipeId = id;
        document.getElementById('recipe-name').value = recipe.name;
        document.getElementById('yield-qty').value = recipe.yield_qty;
        
        // Deep copy the ingredients so we don't accidentally mutate the saved state before saving
        currentRecipeIngredients = JSON.parse(JSON.stringify(recipe.ingredients));
        renderRecipeTable();
        
        saveBtn.innerText = "Update Recipe";
        window.scrollTo({ top: document.getElementById('recipe-name').offsetTop - 50, behavior: 'smooth' });
    };

    window.deleteRecipe = async (id) => {
        if (!confirm("Are you sure you want to delete this recipe?")) return;
        try {
            const response = await fetch(`/api/recipes/${id}`, { method: 'DELETE' });
            if (response.ok) fetchRecipes();
        } catch (error) { console.error("Delete error:", error); }
    };

    // --- 2. Active Recipe Editing Logic ---
    function renderRecipeTable() {
        tbody.innerHTML = '';
        let totalCost = 0;

        currentRecipeIngredients.forEach((ing, index) => {
            const tr = document.createElement('tr');
            
            // Look up the exact cost from the current global catalog
            const catalogItem = globalCatalog.find(c => c.name === ing.name);
            const costPerGram = catalogItem ? catalogItem.cost_per_gram : 0.00; 
            const lineCost = ing.grams * costPerGram;
            
            totalCost += lineCost;

            // Build dynamic dropdown options based on the ingredient catalog
            let optionsHtml = '<option value="">-- Select Ingredient --</option>';
            let foundInCatalog = false;
            
            globalCatalog.forEach(catItem => {
                const selected = (catItem.name === ing.name) ? 'selected' : '';
                if (selected) foundInCatalog = true;
                optionsHtml += `<option value="${catItem.name}" ${selected}>${catItem.name}</option>`;
            });

            // Fallback: If an ingredient is in a recipe but was deleted from the catalog
            if (ing.name && !foundInCatalog) {
                optionsHtml += `<option value="${ing.name}" selected>${ing.name} (Missing from Catalog)</option>`;
            }

            tr.innerHTML = `
                <td>
                    <select class="table-input" style="width: 250px;" onchange="updateIngredient(${index}, 'name', this.value)">
                        ${optionsHtml}
                    </select>
                </td>
                <td><input type="number" step="any" value="${ing.grams}" class="table-input" onchange="updateIngredient(${index}, 'grams', this.value)"></td>
                <td>$${costPerGram.toFixed(4)}</td>
                <td>$${lineCost.toFixed(2)}</td>
                <td><button onclick="removeIngredient(${index})" class="btn-secondary" style="margin-top: 0; padding: 5px 10px;">Remove</button></td>
            `;
            tbody.appendChild(tr);
        });

        updateSummary(totalCost);
    }

    window.updateIngredient = (index, field, value) => {
        if (field === 'grams') value = parseFloat(value) || 0;
        currentRecipeIngredients[index][field] = value;
        renderRecipeTable();
    };

    window.removeIngredient = (index) => {
        currentRecipeIngredients.splice(index, 1);
        renderRecipeTable();
    };

    function updateSummary(totalCost) {
        const yieldQty = parseInt(document.getElementById('yield-qty').value) || 1;
        const salePrice = parseFloat(document.getElementById('sale-price').value) || 0;
        const packaging = parseFloat(document.getElementById('packaging-cost').value) || 0;
        const taxes = parseFloat(document.getElementById('taxes').value) || 0;

        const unitCost = totalCost / yieldQty;
        const estimatedProfit = salePrice - unitCost - packaging - taxes;

        document.getElementById('batch-cost').innerText = `$${totalCost.toFixed(2)}`;
        document.getElementById('unit-cost').innerText = `$${unitCost.toFixed(2)}`;
        document.getElementById('estimated-profit').innerText = `$${estimatedProfit.toFixed(2)}`;
    }

    // --- 3. Form Controls ---
    addBtn.addEventListener('click', () => {
        currentRecipeIngredients.push({ name: '', grams: 0 });
        renderRecipeTable();
    });

    clearBtn.addEventListener('click', () => {
        editingRecipeId = null;
        document.getElementById('recipe-name').value = '';
        document.getElementById('yield-qty').value = 4;
        currentRecipeIngredients = [];
        saveBtn.innerText = "Save Recipe to Database";
        renderRecipeTable();
    });

    document.getElementById('yield-qty').addEventListener('input', () => renderRecipeTable());
    document.getElementById('sale-price').addEventListener('input', () => renderRecipeTable());
    document.getElementById('packaging-cost').addEventListener('input', () => renderRecipeTable());
    document.getElementById('taxes').addEventListener('input', () => renderRecipeTable());

    saveBtn.addEventListener('click', async () => {
        const name = document.getElementById('recipe-name').value;
        const yieldQty = parseInt(document.getElementById('yield-qty').value);

        if (!name || currentRecipeIngredients.length === 0) {
            alert("Recipe needs a name and at least one ingredient.");
            return;
        }

        const payload = {
            name: name,
            yield_qty: yieldQty,
            ingredients: currentRecipeIngredients
        };

        const url = editingRecipeId ? `/api/recipes/${editingRecipeId}` : '/api/recipes/';
        const method = editingRecipeId ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                fetchRecipes();
                clearBtn.click(); // Reset the form after successful save
            } else {
                console.error("Failed to save recipe");
            }
        } catch (error) { console.error("Connection error:", error); }
    });

    // Initialize
    fetchRecipes();
});