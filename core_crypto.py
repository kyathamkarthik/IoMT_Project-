import torch
import torch.nn as nn
import numpy as np
import torch.optim as optim

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

class IoMT_CAE(nn.Module):
    def __init__(self):
        super(IoMT_CAE, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=16, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv1d(in_channels=16, out_channels=32, kernel_size=3, stride=2, padding=1),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose1d(in_channels=32, out_channels=16, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.ConvTranspose1d(in_channels=16, out_channels=1, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid()
        )
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return encoded, decoded

class ChaosGenerator(nn.Module):
    def __init__(self, input_size, key_length):
        super(ChaosGenerator, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, key_length),
            nn.Tanh()
        )
    def forward(self, chaos_seed):
        return self.net(chaos_seed)

class ChaosDiscriminator(nn.Module):
    def __init__(self, key_length):
        super(ChaosDiscriminator, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(key_length, 64),
            nn.LeakyReLU(0.2),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
    def forward(self, key):
        return self.net(key)

def generate_logistic_chaos(seed, r=3.99, size=1):
    chaos_seq = np.zeros(size)
    x = seed
    for i in range(size):
        x = r * x * (1 - x)
        chaos_seq[i] = x
    return torch.tensor(chaos_seq, dtype=torch.float32).unsqueeze(0).to(device)

cae_model = IoMT_CAE().to(device)
key_gen = ChaosGenerator(input_size=1, key_length=32).to(device)
discriminator = ChaosDiscriminator(key_length=32).to(device)

opt_gen = optim.Adam(key_gen.parameters(), lr=0.001)
opt_cae = optim.Adam(cae_model.parameters(), lr=0.001)
loss_fn_cae = nn.MSELoss()

print("Starting IoMT Encryption Pipeline Simulation...")
dummy_medical_data = torch.randn((1, 1, 128)).to(device) 
chaos_seed = generate_logistic_chaos(seed=0.45, size=1)

opt_gen.zero_grad()
generated_key = key_gen(chaos_seed)
expanded_key = generated_key.repeat(1, 32).view(1, 32, 32) 

opt_cae.zero_grad()
encoded_payload, decoded_payload = cae_model(dummy_medical_data)
encrypted_latent_space = encoded_payload * expanded_key 
reconstructed_payload = cae_model.decoder(encrypted_latent_space)

loss_cae = loss_fn_cae(reconstructed_payload, dummy_medical_data)
loss_cae.backward()
opt_cae.step()

print("Encryption Simulation Successful.")
print(f"Original Payload Shape: {dummy_medical_data.shape}")
print(f"Encrypted Latent State Shape: {encrypted_latent_space.shape}")
print(f"CAE Reconstruction Loss: {loss_cae.item():.4f}")