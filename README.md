# IoMT Project

A Python-based security prototype for Internet of Medical Things (IoMT) systems that simulates secure medical data transmission over a 5G gateway using post-quantum authentication and an encryption-inspired latent-space pipeline.

## Overview

This project demonstrates a lightweight IoMT architecture where:

- a medical sensor device generates payloads,
- a Web-based dashboard simulates transmission,
- a FastAPI gateway validates the payload using a post-quantum signature,
- and a circuit-breaker-style response is triggered if the signature is invalid.

The repository combines:

- post-quantum digital signature verification with `oqs`,
- a Streamlit monitoring dashboard,
- a simulated medical data encryption workflow using a convolutional autoencoder and chaos-based key generation,
- a FastAPI validator for secure payload routing.

## Project Structure

- `api_gateway.py` — FastAPI validation gateway that verifies incoming data signatures.
- `dashboard.py` — Streamlit dashboard used to simulate sensor transmission.
- `post_quantum_auth.py` — demo of lattice-based post-quantum signature generation/verification.
- `core_crypto.py` — chaotic key generation and latent-space encryption simulation.
- `.gitignore` — repository ignore rules for local environment files.

## Key Features

- 5G IoMT transmission simulation
- Post-quantum signature verification using ML-DSA
- Real-time security dashboard using Streamlit
- Invalid signature handling with a circuit-breaker response
- Experimental encryption pipeline based on a convolutional autoencoder and chaotic key generation

## Architecture Flow

1. A sensor device generates a payload in the Streamlit dashboard.
2. The payload is signed using a post-quantum signature.
3. The signed payload is sent to the FastAPI gateway.
4. The gateway verifies the signature and key.
5. If verification fails, the gateway refuses the request and raises an error.

## Requirements

This project is built in Python and requires:

- Python 3.9+
- `fastapi`
- `uvicorn`
- `streamlit`
- `torch`
- `numpy`
- `oqs` / OQS Python bindings for post-quantum signature support

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/kyathamkarthik/IoMT_Project-.git
   cd IoMT_Project-
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install fastapi uvicorn streamlit torch numpy
   ```

   If your environment requires the OQS Python binding, install the matching package for your setup (for example, the OQS Python library compatible with your Python version and operating system).

## Running the Project

### Start the gateway

```bash
uvicorn api_gateway:app --host 127.0.0.1 --port 8000 --reload
```

### Launch the dashboard

```bash
streamlit run dashboard.py
```

### Run the standalone authentication demo

```bash
python post_quantum_auth.py
```

### Run the encryption simulation

```bash
python core_crypto.py
```

## Notes

This repository is intended as an educational and research-oriented prototype for exploring secure IoMT communication with post-quantum cryptography concepts. It is not intended to be a production-grade medical device security implementation.

## License

This project does not currently include a license file. If you intend to publish or share it publicly, consider adding an appropriate open-source license.
