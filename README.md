<p align="center">
  <img src="https://img.shields.io/badge/ShieldAI-Project-red?style=for-the-badge&logo=target" />
</p>

# <p align="center">🛡️ ShieldAI: Digital Risk Advisory System</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

---

## 📌 Project Vision
**ShieldAI** is a multi-layered security framework designed to bridge the gap between traditional spam filters and advanced threat intelligence. While most systems only scan text, ShieldAI evaluates the **context, metadata, and structural integrity** of digital communications to detect sophisticated fraud.

---

## 🚀 1. Core Modules (Technical Workflow)

> [!IMPORTANT]
> **ShieldAI** uses an **Ensemble Learning** approach to minimize False Negatives by combining semantic AI with deterministic forensic rules.

### **A. The Hybrid Ensemble Engine (`aggregator.py`)**
* **AI Weights (60%):** Utilizes a fine-tuned **DistilBERT Transformer** model to interpret semantic intent.
* **Heuristic Weights (40%):** Employs hard-coded regex and cybersecurity rules to identify "Red Flag" signals.
* **Override Logic:** Critical triggers automatically escalate the score to **CRITICAL**, overriding AI uncertainty.

### **B. Forensic OCR & Image Analysis (`processor.py` & `rules.py`)**
* **EasyOCR Engine:** Extracts text from low-resolution or noisy screenshots.
* **Metadata Inspection:** Scans for "Software" tags (Photoshop/Canva signatures). 
* **Aspect Ratio Analysis:** Detects cropped or irregularly sized images, often used to hide sender information.

### **C. PDF Structural Analysis (`processor.py`)**
* **Metadata Extraction:** Verifies the `Creator` and `Producer` fields.
* **Anomaly Detection:** Flags documents created by anonymous report generators or those with structural inconsistencies.

---

## 📂 2. Detailed File Structure

```text
AI_Digital_Risk_Advisory_System/
├── app.py                  # Main Orchestrator: Sidebar & Navigation logic
├── Pages/
│   ├── Analyze.py     # Deep Engine: Multi-tab UI (Text/PDF/Image)
│   ├── History.py     # Logs: SQLite connector for historical review
│   └── Analytics.py   # Insights: Plotly-powered risk trend visualization
├── scripts/
│   ├── model_inference.py  # Deep Learning: DistilBERT Transformer management
│   ├── rules.py            # Heuristics: Regex patterns & Metadata checks
│   ├── aggregator.py       # Logic: The Hybrid Mathematical Engine
│   ├── processor.py        # Forensics: EasyOCR & PyMuPDF integration
│   └── database.py         # Persistence: SQLite CRUD Operations
├── Models/                 # Storage: Local pre-trained model weights
└── requirements.txt        # Dependencies: Required Python libraries 
```
---

## 🛠️ 3. Installation Guide
Environment Setup
Bash
# 1. Create virtual environment
```text
python -m venv .venv
```

# 2. Activate environment (Windows)
```
.\venv\Scripts\activate
```

# 3. Activate environment (Mac/Linux)
```
source .venv/bin/activate
```
Library Installation
[!NOTE]
This project utilizes torch and transformers. A stable internet connection is required for the initial setup to fetch the Spam-Bert-Uncased weights (approx. 260MB).

Bash
```
pip install -r requirements.txt
```
📊 4. Database Schema
<table align="center">
<tr>
<th>Table Name</th>
<th>Columns</th>
<th>Primary Purpose</th>
</tr>
<tr>
<td><b>history</b></td>
<td>timestamp, content_snippet, risk_score, risk_level</td>
<td>Stores past scan results for trend analysis and audit trails.</td>
</tr>
</table>

📜 5. MIT License
Copyright (c) 2026 Rihan786-ctrl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

<p align="center"><i>Developed for 3rd Year (AI & Data Science) Capstone Project</i></p>
