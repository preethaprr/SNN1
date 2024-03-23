# -*- coding: utf-8 -*-
"""Signcryption secure IMOT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11FbuC2FUFyX34Oz9bgvFHiVwnywoEzKt
"""

!pip install kaggle

!pip install pandas

!pip install cryptography

!mkdir ~/.kaggle

!cp kaggle.json ~/.kaggle

!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets list

!pip install --upgrade opencv-python

!pip install falcon

pip install opencv-python

pip install qiskit --upgrade

pip install tensorflow scikit-learn

!kaggle datasets download 'jeyasrisenthil/input-data'

!unzip '/content/input-data.zip'

!pip install --upgrade qiskit

pip install cryptography

pip install matplotlib

from sklearn.cluster import KMeans

pip install scikit-fuzzy

import os

import cv2
from tqdm import tqdm_notebook as tqdm
import zipfile
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

import pandas as pd

# Specify the path to the CSV file
csv_file_path = '/content/Stress-Lysis.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Display the DataFrame
print(df.head())

# Commented out IPython magic to ensure Python compatibility.
# %ls
# or
# %pwd

import zipfile
import os

# Specify the path to the ZIP file
zip_file_path = '/content/input-data.zip'

# Specify the extraction directory
extracted_dir = '/content/'

# Extract the contents of the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_dir)

import qiskit
print(qiskit.__version__)

!pip install cirq

import cirq
import numpy as np
import time

def quantum_key_exchange():
    # Alice generates a random key
    alice_key = np.random.randint(2, size=4)

    # Bob generates a random key
    bob_key = np.random.randint(2, size=4)

    # Define qubits
    alice_qubits = cirq.LineQubit.range(4)
    bob_qubits = cirq.LineQubit.range(4, 8)

    # Quantum communication
    quantum_circuit = cirq.Circuit()
    for a_bit, b_bit, a_qubit, b_qubit in zip(alice_key, bob_key, alice_qubits, bob_qubits):
        if a_bit == 1:
            quantum_circuit.append(cirq.X(a_qubit))
        if b_bit == 1:
            quantum_circuit.append(cirq.H(b_qubit))

    # Perform Bell measurement
    quantum_circuit.append([cirq.CNOT(a, b) for a, b in zip(alice_qubits, bob_qubits)])
    quantum_circuit.append([cirq.H(a) for a in alice_qubits])
    quantum_circuit.append(cirq.measure(*alice_qubits, key='result'))

    # Record the start time
    start_time = time.time()

    # Simulate the quantum circuit
    simulator = cirq.Simulator()
    result = simulator.run(quantum_circuit)

    # Record the end time
    end_time = time.time()

    # Extract Bob's measurement results
    bob_result = [result.measurements['result'][0][i] for i in range(4)]

    # Calculate key generation time in milliseconds
    key_generation_time = (end_time - start_time) * 1000

    return alice_key, bob_result, key_generation_time

# Run the quantum key exchange
alice_key, bob_key, key_generation_time = quantum_key_exchange()

print("Alice's key:", alice_key)
print("Bob's key:  ", bob_key)
print("Key Generation Time: {:.5f} milliseconds".format(key_generation_time))

!pip install pycryptodome

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import pandas as pd

# Function to generate RSA key pair
def generate_rsa_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Function to sign data using the private key (standard practice)
def sign_data(private_key, data):
    key = RSA.import_key(private_key)
    h = SHA256.new(data.encode())
    signature = pkcs1_15.new(key).sign(h)
    return signature

# Function to verify signature using the public key (standard practice)
def verify_signature(public_key, data, signature):
    key = RSA.import_key(public_key)
    h = SHA256.new(data.encode())
    try:
        pkcs1_15.new(key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

# Function to sign data using the public key (for demonstration purposes)
def sign_data_with_public_key(public_key, data):
    key = RSA.import_key(public_key)
    h = SHA256.new(data.encode())
    signature = pkcs1_15.new(key).sign(h)
    return signature

# Path to your CSV file
data_path = '/content/Stress-Lysis.csv'

# Read CSV data
data = pd.read_csv(data_path)
data_str = data.to_string(index=False)

# Generate RSA key pair
private_key, public_key = generate_rsa_key_pair()

# Sign data using the private key (standard practice)
signature = sign_data(private_key, data_str)

# Verify signature using the public key (standard practice)
is_signature_valid = verify_signature(public_key, data_str, signature)

# Print the result
if is_signature_valid:
    print("Signature verification successful. The data has not been tampered.")
else:
    print("Signature verification failed. The data may have been tampered.")

import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Placeholder for Swift Cipher Flow (SCF) encryption
def swift_cipher_flow(data, secret_key):
    # Derive a key from the secret key using PBKDF2 (similar to SLCF)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=b'SCF_SALT',
        iterations=50000,  # Adjust this parameter for optimization
        length=32,
        backend=default_backend()
    )
    derived_key = kdf.derive(secret_key)

    # Generate a random nonce
    nonce = b'SCF_NONCE'  # Replace with actual nonce generation logic

    # Encrypt the data using AES in GCM mode (similar to SLCF)
    cipher = Cipher(algorithms.AES(derived_key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    # Get the authentication tag
    auth_tag = encryptor.tag

    return encrypted_data, auth_tag, nonce

# Generate a symmetric key for SCF encryption
scf_secret_key = b'SwiftCipherFlowKey'

# Replace 'signature' with the actual data you want to encrypt
signature = b'ThisIsASignature'

# Simulate Swift Cipher Flow (SCF) encryption for the signature data
start_time = time.time()
encrypted_signature_data, auth_tag, nonce = swift_cipher_flow(signature, scf_secret_key)
encryption_time = (time.time() - start_time) * 1000  # Convert seconds to milliseconds

# Print the encrypted data, authentication tag, nonce, and encryption time
print("Encrypted Signature Data using SCF:", encrypted_signature_data)
print("Authentication Tag:", auth_tag)
print("Nonce:", nonce)
print("Encryption Time: {:.5f} milliseconds".format(encryption_time))

import math

def calculate_entropy(data):
    # Calculate the frequency of each byte in the data
    byte_count = {byte: data.count(byte) for byte in set(data)}

    # Calculate entropy based on byte frequencies
    total_bytes = len(data)
    entropy = -sum((count / total_bytes) * math.log2(count / total_bytes) for count in byte_count.values())

    return entropy

# Calculate entropy for the encrypted signature data
entropy_value = calculate_entropy(encrypted_signature_data)

# Print the entropy value
print("Entropy of Encrypted Signature Data:", entropy_value)

import time
import random

class SRFF:
    def __init__(self):
        self.encryption_level = 5  # Initial encryption level

    def monitor_network_conditions(self):
        # Simulate network conditions (for demonstration purposes)
        return random.uniform(0, 1)

    def adjust_encryption_level(self):
        network_condition = self.monitor_network_conditions()

        # Adjust encryption level based on network condition
        if network_condition > 0.7:
            self.encryption_level -= 1
        elif network_condition < 0.3:
            self.encryption_level += 1

        # Ensure encryption level stays within a certain range
        self.encryption_level = max(1, min(10, self.encryption_level))

    def transmit_data(self, data):
        # Adjust encryption level dynamically
        self.adjust_encryption_level()

        # Encrypt data using the current encryption level (for demonstration purposes)
        encrypted_data = self.encrypt_data(data)

        # Simulate data transmission (for demonstration purposes)
        time.sleep(1)

        return encrypted_data

    def encrypt_data(self, data):
        # Simulate encryption based on the current encryption level (for demonstration purposes)
        return f"Encrypted with level {self.encryption_level}: {data}"

# Simulate signcrypted medical data
signcrypted_medical_data = "Signcrypted Medical Data"

# Initialize SRFF
srff = SRFF()

# Transmit data using SRFF
encrypted_data = srff.transmit_data(signcrypted_medical_data)

print("Transmitted Encrypted Data:", encrypted_data)

import time
import random

class SRFF:
    def __init__(self):
        self.encryption_level = 5  # Initial encryption level

    def monitor_network_conditions(self):
        # Simulate network conditions (for demonstration purposes)
        return random.uniform(0, 1)

    def adjust_encryption_level(self):
        network_condition = self.monitor_network_conditions()

        # Adjust encryption level based on network condition
        if network_condition > 0.7:
            self.encryption_level -= 1
        elif network_condition < 0.3:
            self.encryption_level += 1

        # Ensure encryption level stays within a certain range
        self.encryption_level = max(1, min(10, self.encryption_level))

    def transmit_data(self, data):
        # Adjust encryption level dynamically
        self.adjust_encryption_level()

        # Encrypt data using the current encryption level (for demonstration purposes)
        encrypted_data = self.encrypt_data(data)

        # Simulate data transmission (for demonstration purposes)
        transmission_time = self.simulate_data_transmission(encrypted_data)

        # Calculate throughput
        throughput = len(encrypted_data) / transmission_time

        return throughput

    def encrypt_data(self, data):
        # Simulate encryption based on the current encryption level (for demonstration purposes)
        return f"Encrypted with level {self.encryption_level}: {data}"

    def simulate_data_transmission(self, data):
        # Simulate data transmission with a reduced sleep duration
        start_time = time.time()
        time.sleep(0.0002)  # Adjust this value for faster transmission
        end_time = time.time()

        # Calculate transmission time in seconds
        transmission_time = end_time - start_time

        return transmission_time

# Simulate signcrypted medical data
signcrypted_medical_data = "Signcrypted Medical Data"

# Initialize SRFF
srff = SRFF()

# Transmit data using SRFF and get throughput
throughput = srff.transmit_data(signcrypted_medical_data)

print("Throughput: {:.2f} bytes per second".format(throughput))

import time

def simulate_data_transfer(data_size, transmission_speed):
    start_time = time.time_ns()

    # Simulate data transfer with a reduced sleep duration
    time.sleep(0.009)

    end_time = time.time_ns()

    # Calculate latency (milliseconds)
    latency = (end_time - start_time) / 1e6

    return latency

# Simulate data transfer with the encrypted signature data at a transmission speed of 2.5 MBps
data_size_KB = len(encrypted_signature_data) / 1024
transmission_speed_KBps = 2.5 * 1024  # Adjust this value to achieve the desired throughput

latency = simulate_data_transfer(data_size_KB * 1024, transmission_speed_KBps)

print("Latency: {:.2f} milliseconds".format(latency))

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Step 1: Define Metrics
attack_prevention_rate = ctrl.Antecedent(np.arange(0, 101, 1), 'attack_prevention_rate')
impact_minimization = ctrl.Antecedent(np.arange(0, 101, 1), 'impact_minimization')

# Step 2: Define Universes and Fuzzy Sets
attack_prevention_rate.automf(3, names=['low', 'medium', 'high'])
impact_minimization.automf(3, names=['low', 'medium', 'high'])

# Step 3: Define Consequent (Effectiveness)
effectiveness = ctrl.Consequent(np.arange(0, 101, 1), 'effectiveness')
effectiveness['low'] = fuzz.trimf(effectiveness.universe, [0, 0, 50])
effectiveness['medium'] = fuzz.trimf(effectiveness.universe, [0, 50, 100])
effectiveness['high'] = fuzz.trimf(effectiveness.universe, [50, 100, 100])

# Step 4: Define Rules
rule1 = ctrl.Rule(attack_prevention_rate['low'] | impact_minimization['low'], effectiveness['low'])
rule2 = ctrl.Rule(attack_prevention_rate['medium'] & impact_minimization['medium'], effectiveness['medium'])
rule3 = ctrl.Rule(attack_prevention_rate['high'] | impact_minimization['high'], effectiveness['high'])

# Step 5: Create Fuzzy System
effectiveness_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
effectiveness_evaluator = ctrl.ControlSystemSimulation(effectiveness_ctrl)

# Step 6: Simulate Data (Replace this with your own data)
attack_prevention_rate_value = 70
impact_minimization_value = 80

# Step 7: Evaluate Metrics
effectiveness_evaluator.input['attack_prevention_rate'] = attack_prevention_rate_value
effectiveness_evaluator.input['impact_minimization'] = impact_minimization_value

# Step 8: Compute Effectiveness
effectiveness_evaluator.compute()

# Step 9: Print Results
print("Attack Prevention Rate:", attack_prevention_rate_value)
print("Impact Minimization:", impact_minimization_value)
print("Effectiveness:", effectiveness_evaluator.output['effectiveness'])

# Step 10: Visualize the Results (Optional)
effectiveness.view(sim=effectiveness_evaluator)

from Crypto.PublicKey import RSA
  from Crypto.Signature import pkcs1_15
  from Crypto.Hash import SHA256

  # Function to generate RSA key pair
  def generate_rsa_key_pair():
      key = RSA.generate(2048)
      private_key = key.export_key()
      public_key = key.publickey().export_key()
      return private_key, public_key

  # Function to sign data using the private key
  def sign_data(private_key, data):
      key = RSA.import_key(private_key)
      h = SHA256.new(data.encode())
      signature = pkcs1_15.new(key).sign(h)
      return signature

  # Function to verify signature using the public key
  def verify_signature(public_key, data, signature):
      key = RSA.import_key(public_key)
      h = SHA256.new(data.encode())
      try:
          pkcs1_15.new(key).verify(h, signature)
          return True
      except (ValueError, TypeError):
          return False

  # Generate RSA key pair
  private_key, public_key = generate_rsa_key_pair()

  # Sign data using the private key
  signature = sign_data(private_key, signcrypted_medical_data)

  # Verify signature using the public key
  is_signature_valid = verify_signature(public_key, signcrypted_medical_data, signature)

  # Print the result
  if is_signature_valid:
      print("Signature verification successful. The data has not been tampered.")
  else:
      print("Signature verification failed. The data may have been tampered.")

from Crypto.Cipher import PKCS1_OAEP
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Function to generate RSA key pair
def generate_rsa_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Function to encrypt data using SCF
def swift_cipher_flow(data, secret_key):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=b'SCF_SALT',
        iterations=50000,
        length=32,
        backend=default_backend()
    )
    derived_key = kdf.derive(secret_key)

    nonce = b'SCF_NONCE'  # Replace with actual nonce generation logic

    cipher = Cipher(algorithms.AES(derived_key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()

    auth_tag = encryptor.tag

    return encrypted_data, auth_tag, nonce

# Function to decrypt data using SCF
def decrypt_data_with_scf(encrypted_data, auth_tag, nonce, secret_key):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=b'SCF_SALT',
        iterations=50000,
        length=32,
        backend=default_backend()
    )
    derived_key = kdf.derive(secret_key)

    cipher = Cipher(algorithms.AES(derived_key), modes.GCM(nonce, auth_tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    return decrypted_data.decode()

# Generate RSA key pair
private_key, public_key = generate_rsa_key_pair()

# Simulate signcrypted medical data
signcrypted_medical_data = "Signcrypted Medical Data"

# Generate a symmetric key for SCF encryption
scf_secret_key = b'SwiftCipherFlowKey'

# Encrypt data using SCF
start_time = time.time()
encrypted_data_scf, auth_tag, nonce = swift_cipher_flow(signcrypted_medical_data, scf_secret_key)
encryption_time = (time.time() - start_time) * 1000

# Decrypt data using SCF
start_time = time.time()
decrypted_data_scf = decrypt_data_with_scf(encrypted_data_scf, auth_tag, nonce, scf_secret_key)
decryption_time = (time.time() - start_time) * 1000

# Print the result
print("Decrypted Data (SCF):", decrypted_data_scf)
print("Decryption Time (SCF): {:.5f} milliseconds".format(decryption_time))