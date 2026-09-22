import re
import io
from fastapi import APIRouter, UploadFile, File, HTTPException
from pdfminer.high_level import extract_text

router = APIRouter()

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB size limit guardrail

def calculate_grams_per_unit(name: str):
    weight_match = re.search(r'([\d\.]+)\s*(oz|ounce|lbs|lb|pound)s?', name, re.IGNORECASE)
    if not weight_match:
        return ""
        
    weight_val = float(weight_match.group(1))
    unit = weight_match.group(2).lower()
    
    if unit in ['oz', 'ounce']:
        base_grams = weight_val * 28.3495
    elif unit in ['lb', 'lbs', 'pound']:
        base_grams = weight_val * 453.592
    else:
        base_grams = 0.0

    if base_grams > 0:
        return round(base_grams, 2)
    return ""

def parse_sams_club(text):
    items = []
    
    # SPLIT BY ITEM NUMBER: This bypasses all line-break/formatting issues.
    # Sam's Club items are always preceded by a 5 to 15 digit item code.
    chunks = re.split(r'\b\d{5,15}\b', text)
    
    for chunk in chunks[1:]:
        if "SUBTOTAL" in chunk.upper():
            chunk = chunk[:chunk.upper().find("SUBTOTAL")]
            
        name = "Unknown Item"
        price = 0.0
        qty = 1
        
        lines = [line.strip() for line in chunk.split('\n') if line.strip()]
        
        for line in lines:
            clean_line = re.sub(r'^[\s\|]+', '', line).strip()
            
            if re.search(r'[A-Za-z]', clean_line) and not re.search(r'^\d+\s+AT', clean_line, re.I) and "FOR" not in clean_line.upper():
                name_candidate = re.sub(r'\s+[A-Za-z\u039F\u03BF]$', '', clean_line).strip()
                if not re.match(r'^\d{2}/\d{2}/\d{2}', name_candidate) and name_candidate != "TM":
                    name = name_candidate
                    break
                    
        qty_match = re.search(r'(\d+)\s+AT', chunk, re.IGNORECASE)
        if qty_match:
            qty = int(qty_match.group(1))
            
        chunk_without_deals = re.sub(r'\d+\s+FOR\s+\d+\.\d{2}', '', chunk, flags=re.IGNORECASE)
        prices = re.findall(r'(\d+\.\d{2})', chunk_without_deals)
        if prices:
            price = float(prices[-1])
            
        if price > 0 and name != "Unknown Item":
            unit_measure = "g"
            units = calculate_grams_per_unit(name)
            
            if "CAGEFREE" in name.replace(" ", "").upper() or "EGG" in name.upper():
                units = 60
                unit_measure = "ea"
            elif "DZ" in name.upper():
                dz_match = re.search(r'(\d+)\s*DZ', name, re.IGNORECASE)
                if dz_match:
                    units = int(dz_match.group(1)) * 12
                    unit_measure = "ea"
                    
            items.append({
                "name": name,
                "purchase_price": price,
                "receipt_qty": qty,
                "packs": 1,
                "grams_per_unit": units if units else "",
                "unit_measure": unit_measure
            })
            
    return items

def parse_standard_receipt(text):
    items = []
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for i, line in enumerate(lines):
        qty_match = re.search(r'^(.*?)(?:\|?\s*)Qty\s*(\d+)', line, re.IGNORECASE)
        
        if qty_match:
            pre_text = qty_match.group(1).strip()
            pre_text = re.sub(r'^[\|\s]+', '', pre_text).strip()
            
            qty = int(qty_match.group(2))
            
            if len(pre_text) > 3:
                name = pre_text
            else:
                name = lines[i-1] if i > 0 else "Unknown Item"
                name = re.sub(r'^[\|\s]+', '', name).strip()
                
                if len(name) < 15 and i > 1:
                    prev_name = re.sub(r'^[\|\s]+', '', lines[i-2]).strip()
                    name = f"{prev_name} {name}"
            
            price = 0.0
            price_match = re.search(r'\$\s*([\d\.]+)', line)
            if not price_match and i + 1 < len(lines):
                price_match = re.search(r'\$\s*([\d\.]+)', lines[i+1])
            
            if price_match:
                price = float(price_match.group(1))

            units = calculate_grams_per_unit(name)
            pack_match = re.search(r'(\d+)\s*(pk|pack)s?', name, re.IGNORECASE)
            packs = int(pack_match.group(1)) if pack_match else 1
            
            unit_measure = "g"
            if "EGG" in name.upper() or "DZ" in name.upper():
                unit_measure = "ea"
                dz_match = re.search(r'(\d+)\s*DZ', name, re.IGNORECASE)
                if dz_match:
                    units = int(dz_match.group(1)) * 12
                elif not units:
                    units = 1 

            items.append({
                "name": name,
                "purchase_price": price,
                "receipt_qty": qty,
                "packs": packs,
                "grams_per_unit": units if units else "",
                "unit_measure": unit_measure
            })
    return items

@router.post("/parse")
async def parse_receipt(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Must be a PDF file.")

    content = bytearray()
    while chunk := await file.read(1024 * 1024):
        content.extend(chunk)
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 5MB.")

    try:
        # pdfminer handles stubborn browser-generated encodings
        text = extract_text(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read PDF: {str(e)}")

    print("\n" + "="*50)
    print(f"RAW TEXT EXTRACTED FROM: {file.filename}")
    print("="*50)
    print(repr(text))
    print("="*50 + "\n")

    text_normalized = text.lower().replace(" ", "").replace("\n", "")
    filename_lower = file.filename.lower()
    
    if "sams" in filename_lower or "sam's" in text_normalized or "sams" in text_normalized or "tc#" in text_normalized:
        items = parse_sams_club(text)
        vendor = "Sam's Club"
    else:
        items = parse_standard_receipt(text)
        vendor = "Unknown Vendor"

    return {"vendor": vendor, "items": items, "raw_text_debug": text}