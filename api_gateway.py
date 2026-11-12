from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import oqs

app = FastAPI(title="IoMT 5G Gateway")

class IoMTPayload(BaseModel):
    device_id: str
    encrypted_data: str
    signature_hex: str
    public_key_hex: str

@app.post("/transmit")
def receive_medical_data(payload: IoMTPayload):
    signature_bytes = bytes.fromhex(payload.signature_hex)
    public_key_bytes = bytes.fromhex(payload.public_key_hex)
    data_bytes = payload.encrypted_data.encode('utf-8')
    
    # Initialize Lattice Verifier
    verifier = oqs.Signature("ML-DSA-65")
    
    try:
        # Verify the post-quantum signature against the payload
        is_valid = verifier.verify(data_bytes, signature_bytes, public_key_bytes)
    except Exception:
        is_valid = False
    finally:
        verifier.free()
        
    if not is_valid:
        # AUTONOMOUS CIRCUIT BREAKER TRIPPED
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="CIRCUIT BREAKER TRIPPED: Quantum Signature Invalid or Corrupted Payload."
        )
        
    return {"status": "Success", "message": "Payload verified and securely routed."}