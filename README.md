<div align="center">

# 🤖 WhatsApp Financial Data Extraction

### 🧠 Custom NLP / Named Entity Recognition Model

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/spaCy-NLP-09A3D5?style=for-the-badge&logo=spacy&logoColor=white"/>
  <img src="https://img.shields.io/badge/NER-Information%20Extraction-8A2BE2?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Model-V10-00C853?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Completed-00C853?style=for-the-badge"/>
</p>

<p>
  <a href="#-overview">Overview</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-entities">Entities</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-model-development">Model Development</a>
</p>

</div>

---

## ✨ Overview

**WhatsApp Financial Data Extraction** is a custom Natural Language Processing (NLP)
project designed to extract structured financial transfer information from
unstructured WhatsApp-style messages.

The system uses a custom **spaCy Named Entity Recognition (NER)** model to identify:

- 👤 Beneficiary / recipient names
- 🏦 Bank account numbers
- 🔐 IFSC codes
- 💰 Transfer amounts

The extracted information can then be passed to downstream applications for
validation, database storage, Excel generation, approval workflows, and WhatsApp
automation.

---

## 💬 Example

### Input

```text
Please send Rs. 15,500 to Priya Sharma.
Account 445566778899.
IFSC HDFC0001234.

🧠 Model Extraction
{
  "name": "Priya Sharma",
  "account_number": "445566778899",
  "ifsc_code": "HDFC0001234",
  "amount": "15,500"
}

🧠 What Does This Model Do?

The core problem is Information Extraction.

Instead of classifying an entire message into one category, the model identifies
specific pieces of information inside the message.
WhatsApp Message
       │
       ▼
┌─────────────────────────┐
│      spaCy NER Model    │
└────────────┬────────────┘
             │
       Entity Detection
             │
     ┌───────┼────────┐
     ▼       ▼        ▼
   NAME   ACCOUNT    IFSC
             │
             ▼
           AMOUNT
             │
             ▼
      Structured JSON

🎯 Supported Entities
| Entity           | Description                  | Example        |
| ---------------- | ---------------------------- | -------------- |
| `NAME`           | Beneficiary / recipient name | `Priya Sharma` |
| `ACCOUNT_NUMBER` | Bank account number          | `445566778899` |
| `IFSC_CODE`      | Indian Financial System Code | `HDFC0001234`  |
| `AMOUNT`         | Monetary amount              | `15,500`       |

💰 Amount Annotation Rule

The model annotates the numeric monetary value only.
₹5000       → 5000
₹5,000      → 5,000
Rs 5000     → 5000
Rs. 5,000   → 5,000
5000 INR    → 5000
5000 rupees → 5000
25k         → 25k
20.5k       → 20.5k
Currency indicators are intentionally kept outside the AMOUNT entity.
🏗️ Architecture
                    WhatsApp Message
                           │
                           ▼
                 ┌───────────────────┐
                 │    Raw Message    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │   spaCy NER V10   │
                 └─────────┬─────────┘
                           │
                           ▼
             ┌────────────────────────────┐
             │      Entity Extraction     │
             └─────────────┬──────────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
           NAME         ACCOUNT        IFSC
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                         AMOUNT
                           │
                           ▼
                  Structured Output
                           │
                           ▼
                Validation / Normalization
                           │
                           ▼
                  Downstream Application

🔄 Extraction Pipeline
Message
   │
   ▼
Tokenization
   │
   ▼
NER Prediction
   │
   ▼
Entity Detection
   │
   ├── NAME
   ├── ACCOUNT_NUMBER
   ├── IFSC_CODE
   └── AMOUNT
   │
   ▼
Structured JSON
   │
   ▼
Validation


📊 Dataset

The final V10 dataset contains:
| Dataset    | Examples |
| ---------- | -------: |
| Training   |  **254** |
| Validation |   **54** |
| Test       |   **55** |
| Total      |  **363** |

🛠️ Technology Stack
<div align="center">
| Technology      | Purpose                        |
| --------------- | ------------------------------ |
| 🐍 Python       | Core development               |
| 🧠 spaCy        | NLP / NER                      |
| 📊 NumPy        | Numerical processing           |
| 🐼 Pandas       | Data processing                |
| 📈 Scikit-learn | ML utilities / evaluation      |
| 🔧 Git          | Version control                |
| 🐙 GitHub       | Source control & collaboration |
</div>

Possible future components include:

⚡ FastAPI
📱 WhatsApp Business API
🗄️ PostgreSQL
📊 Excel export
🔐 Authentication
👤 Human approval workflow
📝 Audit logging
☁️ Cloud deployment

🎓 Learning Outcomes

This project demonstrates practical experience with:

Natural Language Processing
Named Entity Recognition
Custom spaCy model training
Dataset creation
Entity annotation
Train / validation / test splitting
Model evaluation
Error analysis
Iterative dataset improvement
Information extraction
Model inference
Financial data validation
ML application architecture

👨‍💻 Author
<div align="center">
Muhammad Salim M K

Python Backend Developer | Django | REST APIs | NLP / AI

<p> <a href="https://github.com/saali05"> <img src="https://img.shields.io/badge/GitHub-saali05-181717?style=for-the-badge&logo=github"/> </a> </p> </div>

<div align="center">
⭐ If you find this project useful, consider starring the repository!
WhatsApp → NLP → NER → Structured Financial Data
Built with Python 🐍 + spaCy 🧠

</div> ```