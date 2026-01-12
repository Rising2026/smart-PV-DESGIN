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
import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="SolarPro AI", layout="wide")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar (Settings) ---
with st.sidebar:
    st.title("⚙️ Project Settings")
    company_name = st.text_input("Your Company Name", "Rising Solar Solutions")
    profit_margin = st.slider("Profit Margin (%)", 5, 50, 20)
    st.divider()
    st.info("💡 Tip: Margin set karne se cost auto-adjust ho jayegi.")

# --- Header ---
st.title(f"☀️ {company_name}: AI Estimator")
c1, c2, c3 = st.columns(3)

with c1:
    client = st.text_input("Customer Name", "Walking Client")
with c2:
    panels = st.number_input("Total Panels", min_value=1, value=10)
with c3:
    panel_watt = st.selectbox("Panel Wattage", [440, 540, 550, 600])

# --- Calculations ---
system_size = (panels * panel_watt) / 1000
base_cost = panels * 25000  # Rough estimate per panel including structure
total_with_margin = base_cost + (base_cost * (profit_margin / 100))

# --- Dashboard Layout ---
st.divider()
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("System Size", f"{system_size} kWp")
col_m2.metric("Total Quotation", f"₹{total_with_margin:,.0f}")
col_m3.metric("Annual Savings", f"₹{system_size * 1200 * 8:,.0f}") # Approx savings

# --- Visual Layout ---
st.subheader("🛠️ Installation Blueprint")
rows = 2 if panels > 4 else 1
cols = (panels // rows) + (panels % rows > 0)

# Creating a visual grid
grid_html = "".join([f'<div style="display:flex; gap:10px; margin-bottom:10px;">' + 
                     "".join(['<div style="width:60px; height:100px; background-color:#1a73e8; border:2px solid #fff; border-radius:5px;"></div>' for _ in range(cols)]) + 
                     '</div>' for _ in range(rows)])

st.markdown(f'<div style="background-color:#2c3e50; padding:30px; border-radius:15px; display:inline-block;">{grid_html}</div>', unsafe_allow_html=True)

# --- Material List (BOM) ---
st.subheader("📦 Bill of Materials")
bom_data = {
    "Component": ["Solar Panels", "Mounting Structure", "Inverter", "DC Wire (m)", "Earthing Kit"],
    "Qty": [panels, f"{rows}x{cols} Grid", "1 Unit", panels * 5, "2 Sets"],
    "Spec": [f"{panel_watt}W Mono Perc", "Hot Dip Galvanized", f"{system_size}kW String", "4sq mm", "Copper Bonded"]
}
st.table(pd.DataFrame(bom_data))

if st.button("📥 Prepare Final Quotation"):
    st.balloons()
    st.success(f"Quotation for {client} is ready! (PDF Feature coming next)")
