import streamlit as st
from urllib.parse import urlparse, unquote
import re

# List of sustainability keywords
ECO_KEYWORDS = [
    "bamboo", "biodegradable", "eco", "eco-friendly", "compostable",
    "sustainable", "reusable", "plastic-free", "organic", "natural", "recyclable"
]

# Step 1: Extract product name from URL
def extract_name_from_link(link):
    try:
        path = urlparse(link).path
        parts = path.split("/")
        slug = next((p for p in parts if "-" in p), None)
        if slug:
            # Clean slug and return
            return re.sub(r'[^a-zA-Z0-9\s]', '', unquote(slug.replace("-", " ")))
        else:
            return None
    except:
        return None

# Step 2: Check for sustainability
def check_sustainability(text):
    if not text:
        return False, []
    found = [k for k in ECO_KEYWORDS if k in text.lower()]
    return len(found) > 0, found

# --- Streamlit UI ---
st.set_page_config(page_title="Eco Product Link Checker", layout="centered")
st.title("🌍 Sustainable Product Link Checker")
st.markdown("Paste an **Amazon/Flipkart/Meesho product link**, and I’ll check if it’s likely eco-friendly.")

# Input
product_link = st.text_input("🔗 Paste product link:")

# Process
if product_link:
    product_name = extract_name_from_link(product_link)

    if product_name:
        st.subheader("🛍 Product Name (From Link)")
        st.write(product_name)

        is_sustainable, keywords = check_sustainability(product_name)

        if is_sustainable:
            st.success(f"✅ Looks sustainable! Found keywords: {', '.join(keywords)}")
        else:
            st.warning("❌ Doesn’t seem sustainable based on the product name.")
    else:
        st.error("⚠️ Couldn’t extract product name from link. Try another one.")

