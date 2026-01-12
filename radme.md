import streamlit as st
from fpdf import FPDF

# --- Calculation Logic ---
RATES = {"Base Plate": 250, "Rail": 850, "End Clamp": 45, "Mid Clamp": 40, "Fasteners": 15}

def calculate_solar(num_panels, st_type):
    if st_type == "Rooftop (RCC)":
        rows = 2 if num_panels > 4 else 1
        cols = (num_panels // rows) + (num_panels % rows > 0)
        base_plates = (rows + 1) * (cols + 1)
    else:
        rows = 2
        cols = num_panels // 2
        base_plates = num_panels * 2
    
    items = {
        "Base Plate": base_plates,
        "Rail": (num_panels // 2) * 2,
        "End Clamp": 4,
        "Mid Clamp": (num_panels - 1) * 2 if num_panels > 1 else 0,
        "Fasteners": base_plates * 4
    }
    total = sum(items[name] * RATES[name] for name in items)
    return items, total, rows, cols

# --- UI ---
st.title("☀️ Solar AI Dashboard")
client_name = st.text_input("Customer Name:", "Walking Client")
panels = st.number_input("Total Panels:", min_value=1, value=10)
st_type = st.selectbox("Structure Type:", ["Rooftop (RCC)", "Ground Mount"])

if st.button("Generate Plan"):
    items, total, r, c = calculate_solar(panels, st_type)
    st.success(f"Total Cost: ₹{total:,}")
    
    # Simple Layout Visual
    st.write(f"Layout: {r} Rows x {c} Columns")
    grid = ("🟦 " * c + "\n\n") * r
    st.text(grid)
    
    st.table(list(items.items()))
