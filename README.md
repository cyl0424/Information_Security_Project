# Max pooling using Homomorphic Encryption

## Project Overview

This project focuses on developing a privacy-preserving max pooling function using homomorphic encryption. While the technique has applications in IoT, particularly for smart CCTV systems, our implementation specifically addresses the creation and demonstration of the max pooling function under encrypted conditions.

## Project Team
- 김가경 (20102101)
- 추유림 (20102124)

## Project Idea

### Main Idea: Security of IoT
IoT devices are internet-connected objects like security cameras, smart refrigerators, and WiFi-enabled automobiles. Securing these devices ensures they do not introduce threats into a network. Common IoT security threats include firmware vulnerability exploits, credential-based attacks, on-path attacks, and physical hardware-based attacks.

### Project Scope
Our project focuses on implementing the max pooling function using homomorphic encryption, demonstrating the ability to process encrypted data effectively. This method can be extended to IoT applications, such as smart CCTV systems, but the current scope is limited to the function's implementation and testing.

## Project Plan

### Step 1: Encrypt Raw Data
Sensitive raw data, such as people's faces and motions, will be encrypted to protect sensitive information.

### Step 2: Training AI Models
An AI model will be trained using homomorphic encryption operations. Specifically, a CNN model will use max pooling with homomorphic operations to detect anomalous behavior while the data remains encrypted.

### Step 3: Max Pooling
Max pooling reduces feature map dimensionality by selecting the maximum value in each patch, retaining key features, and discarding less significant details. It enhances translation invariance and reduces computational complexity in video analysis, thereby improving the robustness of anomaly detection.

## Implementation Steps

### Step 1: Data Conversion
Convert matrix data into a format suitable for piheaan, ensuring data can be processed within the constraints of homomorphic encryption.

### Step 2: Data Encryption
Encrypt the converted data using piheaan, preparing it for secure transmission and processing.

### Step 3: Max Pooling Function Implementation
Implement the max pooling function using built-in homomorphic encryption functions to process and analyze encrypted data efficiently.

### Step 4: Approximate Max Value Function
Develop a function to find the approximate max value using homomorphic encryption operations, ensuring efficient anomaly detection while maintaining data privacy.

## Environment Setup
This project is a Flask web application that uses the following packages:

- Flask
- Flask-WTF
- Pillow
- NumPy
- WTForms
- Werkzeug
- PI-HEaan
  
### Step 1. Clone the Repository

First, clone the repository to your local machine using the following command:

```bash
git clone https://github.com/cyl0424/Information_Security_Project.git
cd Information_Security_Project
```

### Step 2. Install Python

This project uses Python 3.10. If Python is not installed, please download and install Python 3.10 from the [official Python website](https://www.python.org/downloads/release/python-3100/).

### Step 3. Set Up Virtual Environment

Using a virtual environment allows you to isolate the dependencies of your project. Set up and activate a virtual environment with the following commands:

```bash
# Create a virtual environment
python3.10 -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate

# Activate the virtual environment (macOS/Linux)
source venv/bin/activate
```

### Step 4. Install Packages

To install the required packages, use the `requirements.txt` file. Run the following command:

```bash
pip install -r requirements.txt
```

### Step 5. Run the Application

With the virtual environment activated, run the Flask application. Execute the following command in the directory where the `app.py` file (or the entry point of your application) is located:

```bash
python app.py
```

Once the application is running, open your browser and go to `http://127.0.0.1:5000/` to view it.

## Demonstration
- Set up the testing environment (requirements.txt)
- Upload image(test image is provided) and configure window size and stride values (recommend a window and stride size of 2)
  <img width="733" alt="스크린샷 2024-05-31 오후 6 39 13" src="https://github.com/cyl0424/Information_Security_Project/assets/63573867/91513774-28d0-4f6b-848b-404b47199df0">
- Check and compare results using sorting and approximate max methods
  <img width="733" alt="스크린샷 2024-05-31 오후 6 39 46" src="https://github.com/cyl0424/Information_Security_Project/assets/63573867/78c693e1-9ddb-4fd9-997a-28d563753357">
  <img width="733" alt="스크린샷 2024-05-31 오후 6 39 58" src="https://github.com/cyl0424/Information_Security_Project/assets/63573867/805a319b-1f17-4efa-b67c-c70fcd161f55">
  <img width="733" alt="스크린샷 2024-05-31 오후 6 40 12" src="https://github.com/cyl0424/Information_Security_Project/assets/63573867/c28eaec8-1316-47bf-a3e9-bd7d2a34325c">




## Limitations
- The approximate max function sometimes produces reversed results compared to sorting.
- Execution time for the approximate max function is longer than expected.

## References
- Lee, J. W., Kang, H., Lee, Y., Choi, W., Eom, J., Deryabin, M., ... & No, J. S. (2022). Privacy-preserving machine learning with fully homomorphic encryption for deep neural network. iEEE Access, 10, 30039-30054.
- Al Badawi, A., Bates, J., Bergamaschi, F., Cousins, D. B., Erabelli, S., Genise, N., ... & Zucca, V. (2022, November). Openfhe: Open-source fully homomorphic encryption library. In Proceedings of the 10th Workshop on Encrypted Computing & Applied Homomorphic Cryptography (pp. 53-63).
- Marcolla, C., Sucasas, V., Manzano, M., Bassoli, R., Fitzek, F. H., & Aaraj, N. (2022). Survey on fully homomorphic encryption, theory, and applications. Proceedings of the IEEE, 110(10), 1572-1609.
- Lee, H., Choi, J., & Lee, Y. (2023). Approximating Max Function in Fully Homomorphic Encryption. Electronics, 12(7), 1724.
- Banerjee, B., & Murino, V. (2017, March). Efficient pooling of image based CNN features for action recognition in videos. In 2017 IEEE international conference on acoustics, speech and signal processing (ICASSP) (pp. 2637-2641). IEEE.
- Hijazi, N. M., Aloqaily, M., Guizani, M., Ouni, B., & Karray, F. (2023). Secure federated learning with fully homomorphic encryption for iot communications. IEEE Internet of Things Journal.
- https://www.cloudflare.com/ko-kr/learning/security/glossary/iot-security/
- https://cheapsslsecurity.com/blog/iot-security-understanding-pki-role-in-securing-internet-of-things/
- https://www.cryptolab.co.kr/en/products-en/understanding-he/
- https://www.ssl2buy.com/wiki/homomorphic-encryption
- https://www.intel.com/content/www/us/en/developer/tools/homomorphic-encryption/overview.html
- https://blog.openmined.org/ckks-explained-part-1-simple-encoding-and-decoding/
