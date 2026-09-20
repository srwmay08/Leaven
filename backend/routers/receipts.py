import re
import io
from fastapi import APIRouter, UploadFile, File, HTTPException
import PyPDF2

router = APIRouter()

def calculate_grams_per_unit(name: str):
    # 1. Detect Base Weight (oz or lbs)
    weight_match = re.search(r'([\d\.]+)\s*(oz|ounce|lbs|lb|pound)s?', name, re.IGNORECASE)
    if not weight_match:
        return ""
        
    weight_val = float(weight_match.group(1))
    unit = weight_match.group(2).lower()
    
    # 2. Convert to Grams
    if unit in ['oz', 'ounce']:
        base_grams = weight_val * 28.3495
    elif unit in ['lb', 'lbs', 'pound']:
        base_grams = weight_val * 453.592
    else:
        base_grams = 0.0

    if base_grams > 0:
        return round(base_grams, 2)
    return ""


@router.post("/parse")
async def parse_receipt(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Must be a PDF file.")

    content = await file.read()
    
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read PDF: {str(e)}")

    lines = [line.strip() for line in text.split('\n') if line.strip()]
    items = []

    for i, line in enumerate(lines):
        # Anchored Regex: Forces capture of any text on the exact same line BEFORE "Qty"
        qty_match = re.search(r'^(.*?)(?:\|?\s*)Qty\s*(\d+)', line, re.IGNORECASE)
        
        if qty_match:
            pre_text = qty_match.group(1).strip()
            # Strip all leading pipes and spaces
            pre_text = re.sub(r'^[\|\s]+', '', pre_text).strip()
            
            qty = int(qty_match.group(2))
            
            # If there's text before "Qty" on the same line, that is the item
            if len(pre_text) > 3:
                name = pre_text
            else:
                # Fall back to the line above
                name = lines[i-1] if i > 0 else "Unknown Item"
                name = re.sub(r'^[\|\s]+', '', name).strip()
                
                # Stitch PyPDF2 line breaks back together (e.g. "tissues/box")
                if len(name) < 15 and i > 1:
                    prev_name = re.sub(r'^[\|\s]+', '', lines[i-2]).strip()
                    name = f"{prev_name} {name}"
            
            # Find price on current or next line
            price = 0.0
            price_match = re.search(r'\$\s*([\d\.]+)', line)
            if not price_match and i + 1 < len(lines):
                price_match = re.search(r'\$\s*([\d\.]+)', lines[i+1])
            
            if price_match:
                price = float(price_match.group(1))

            # Run the auto-conversion engine
            grams_per_unit = calculate_grams_per_unit(name)
            
            # Auto-detect packs (e.g., "2 pk") to pass to the frontend
            pack_match = re.search(r'(\d+)\s*(pk|pack)s?', name, re.IGNORECASE)
            packs = int(pack_match.group(1)) if pack_match else 1

            items.append({
                "name": name,
                "purchase_price": price,
                "receipt_qty": qty,
                "packs": packs,
                "grams_per_unit": grams_per_unit 
            })

    return {"items": items}