import streamlit as st
import requests
from post_quantum_auth import LatticeAuthenticationSimulator

st.set_page_config(page_title="IoMT Security Monitor", layout="wide")
st.title("5G IoMT Real-Time Security Dashboard")

# Initialize the Post-Quantum Signer in memory
if 'pqc_auth' not in st.session_state:
    st.session_state.pqc_auth = LatticeAuthenticationSimulator()

st.sidebar.header("IoMT Sensor Simulator")
device_id = st.sidebar.text_input("Device ID", "Sensor-ECG-042")
payload_text = st.sidebar.text_input("Encrypted Payload", "LATENT_PAYLOAD_TEST")
simulate_attack = st.sidebar.checkbox("Simulate Quantum Attack (Corrupt Signature)")

if st.sidebar.button("Transmit to 5G Gateway"):
    data_bytes = payload_text.encode('utf-8')
    
    # 1. Generate true signature
    valid_signature = st.session_state.pqc_auth.generate_signature(data_bytes)
    
    # 2. Corrupt the signature if simulating a network attack
    sig_hex = "deadbeef" * 10 if simulate_attack else valid_signature.hex()
    pub_key_hex = st.session_state.pqc_auth.public_key.hex()

    # 3. Transmit over simulated 5G network to FastAPI Gateway
    try:
        response = requests.post(
            "http://127.0.0.1:8000/transmit", 
            json={
                "device_id": device_id, 
                "encrypted_data": payload_text, 
                "signature_hex": sig_hex,
                "public_key_hex": pub_key_hex
            }
        )
        
        if response.status_code == 200:
            st.success(f"Transmission Successful: {response.json()['message']}")
        else:
            st.error(f"ALERT: {response.json()['detail']}")
            
    except requests.exceptions.ConnectionError:
        st.error("Gateway Offline. Is the FastAPI server running in your terminal?")