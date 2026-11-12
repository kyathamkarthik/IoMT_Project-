import oqs

class LatticeAuthenticationSimulator:
    def __init__(self, algorithm="ML-DSA-65"):
        self.algorithm = algorithm
        self.signer = oqs.Signature(self.algorithm)
        self.public_key = self.signer.generate_keypair()
        
    def generate_signature(self, message: bytes):
        print(f"Generating Post-Quantum Signature using {self.algorithm}...")
        return self.signer.sign(message)
        
    def verify_gateway_access(self, message: bytes, signature: bytes, public_key: bytes):
        print("Gateway: Verifying Post-Quantum Signature...")
        return self.signer.verify(message, signature, public_key)

    def cleanup(self):
        self.signer.free()

# 1. Simulate the IoMT Sensor Payload
iomt_device_id = "Sensor-ECG-042"
medical_payload = b"ENCRYPTED_LATENT_PAYLOAD_FROM_CAE"

print(f"--- IoMT Device: {iomt_device_id} ---")
pqc_auth = LatticeAuthenticationSimulator()

pq_signature = pqc_auth.generate_signature(medical_payload)
print(f"Signature generated successfully. Length: {len(pq_signature)} bytes")

print("\n--- Transmitting over 5G Network ---")
print("...")

print("\n--- 5G Edge Gateway ---")
gateway_verification = pqc_auth.verify_gateway_access(
    medical_payload, 
    pq_signature, 
    pqc_auth.public_key
)

if gateway_verification:
    print("STATUS: Access Granted. Signature is valid and anti-quantum secure.")
else:
    print("STATUS: Access Denied. Signature verification failed.")

pqc_auth.cleanup()