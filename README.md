# BlockGuard

**An Offline Framework for Smart-Contract Safety Analysis and Minute-Scale Gas-Fee Forecasting**

---

## Overview

BlockGuard is a comprehensive, self-contained desktop application designed to streamline Ethereum smart-contract development. It seamlessly integrates security analysis and real-time gas fee predictions into a single, intuitive interface. BlockGuard leverages the Slither static analyzer for identifying vulnerabilities and utilizes a lightweight GRU neural network trained on extensive historical Ethereum data to provide accurate minute-scale forecasts of gas fees, all while operating entirely offline.

---

## Features

* **Security Analysis**:

  * Locally analyzes Ethereum smart contracts with the powerful Slither tool.
  * Clearly ranked and detailed explanations of identified vulnerabilities in plain language.
  * Provides recommendations for remediation to enhance smart-contract security.

* **Gas-Fee Prediction**:

  * Real-time Ethereum gas fee predictions using an efficient GRU-based neural network.
  * Minute-scale precision forecasting, enabling developers to optimize deployment timing and cost management.
  * Historical trends and forecast visualization within the intuitive interface.

* **Offline Operation**:

  * Completely offline computation ensures maximum privacy and eliminates any dependency on cloud-based solutions or subscriptions.
  * Secure handling of sensitive source code without risk of external exposure.

* **Interactive UI**:

  * User-friendly, two-tab Streamlit interface.
  * Simultaneously accessible insights on security and gas fees for enhanced workflow efficiency.

---

## Installation

### Prerequisites

* Python 3.8 or higher
* Pip (Python package installer)

### Clone Repository

```bash
git clone https://github.com/Namantyagi2727/BlockGuard
cd BlockGuard
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### Run the Application

```bash
streamlit run app.py
```

### Workflow

1. Launch BlockGuard via the Streamlit application.
2. Upload your Ethereum smart-contract code.
3. Review detailed vulnerability analysis results in the Security Analysis tab.
4. Access and monitor real-time gas fee predictions through the Gas Forecast tab.
5. Utilize provided feedback and insights for contract refinement and optimized deployment.

---

## Directory Structure

```
BlockGuard/
├── app.py                      # Main Streamlit application
├── models/                     # Pre-trained GRU models for gas fee prediction
├── analysis/                   # Static analysis scripts and Slither integration modules
├── data/                       # Historical Ethereum gas fee data for model training
├── utils/                      # Utility scripts and supporting functions
├── docs/                       # Detailed documentation and user guides
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## Contributing

Contributions are highly encouraged! Please follow the outlined steps:

1. Fork the repository
2. Create a dedicated feature branch (`git checkout -b feature-new-feature`)
3. Implement your feature or fix
4. Commit clearly documented changes (`git commit -m 'Implement feature: detailed description'`)
5. Push your changes (`git push origin feature-new-feature`)
6. Open a descriptive Pull Request

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Contact

* **Project Maintainer**: \[Naman Tyagi]
* **GitHub Repository**: \[https://github.com/Namantyagi2727/BlockGuard]

Feel free to open an issue, request features, or contact directly for any questions, feedback, or collaboration opportunities.
