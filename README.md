<div align="center">

# 🛡️ SecurePrompt

### Adaptive Prompt Injection Detection & LLM Security Framework

*A production-ready AI security framework for detecting Prompt Injection, Jailbreaks, Prompt Leakage, and adversarial attacks on Large Language Models using DistilBERT, Ensemble Learning, Hard Negative Mining, and Explainable AI.*

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red.svg)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

</div>

---

# 📌 Overview

**SecurePrompt** is an AI Security Framework designed to protect Large Language Models (LLMs) against malicious prompts such as:

- Prompt Injection
- Jailbreak Attacks
- Prompt Leakage
- Instruction Override
- Roleplay Attacks
- Adversarial Prompts

The project combines modern Natural Language Processing (NLP), Transformer-based models, traditional Machine Learning, and Explainable AI to build a multi-layer defense system for LLM applications.

---

# ✨ Key Features

## 🛡️ Security

- Prompt Injection Detection
- Jailbreak Detection
- Prompt Leakage Detection
- Instruction Override Detection
- Adversarial Prompt Detection

---

## 🤖 Machine Learning

- DistilBERT Fine-Tuning
- Ensemble Learning
- TF-IDF + Logistic Regression Baseline
- Feature Engineering
- Hard Negative Mining
- Hard Positive Mining
- Model Versioning

---

## 📊 Explainability

- Prediction Confidence
- Feature Importance
- Explainable Predictions
- Error Analysis

---

## 🚀 Backend

- FastAPI REST API
- Model Serving
- Prediction Pipeline
- JSON API Responses

---

## 📈 Evaluation

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix
- ROC-AUC
- Adversarial Evaluation

---

# 🏗️ System Architecture

```text
                         User Prompt
                              │
                              ▼
                     Input Validation
                              │
                              ▼
                     Feature Extraction
                              │
                              ▼
                 ┌─────────────────────┐
                 │   DistilBERT Model  │
                 └─────────────────────┘
                              │
                 ┌─────────────────────┐
                 │ TF-IDF Classifier   │
                 └─────────────────────┘
                              │
                              ▼
                     Ensemble Engine
                              │
                              ▼
                 Explainability Module
                              │
                              ▼
                    Risk Score Generation
                              │
                              ▼
                     Final Classification
```

---

# 📂 Project Structure

```text
SecurePrompt/
│
├── training_env/
│   ├── compiled_security_model_distilbert/
│   ├── compiled_security_model_distilbert_v2/
│   ├── compiled_security_model_distilbert_v3/
│   ├── compiled_security_model_distilbert_v4/
│   │
│   ├── exports/
│   │
│   ├── 01_model_builder.ipynb
│   ├── 02_distilbert_training.ipynb
│   ├── 03_finetune_patch.ipynb
│   ├── 04_hard_negative_mining.ipynb
│   ├── 05_feature_engineering.ipynb
│   ├── 06_ensemble.ipynb
│   ├── 07_distilbert_v4_hardtrained.ipynb
│   ├── 08_adversarial_eval.ipynb
│   │
│   ├── evaluation_report.json
│   ├── hard_negatives.csv
│   ├── hard_positives.csv
│   └── requirements.txt
│
├── backend/
│
├── frontend/
│
├── models/
│
└── README.md
```

---

# ⚙️ Machine Learning Pipeline

```text
Dataset
   │
   ▼
Data Cleaning
   │
   ▼
Tokenization
   │
   ▼
Feature Engineering
   │
   ▼
DistilBERT Fine-Tuning
   │
   ▼
Validation
   │
   ▼
Hard Negative Mining
   │
   ▼
Retraining
   │
   ▼
Ensemble Learning
   │
   ▼
Adversarial Evaluation
   │
   ▼
Model Export
   │
   ▼
FastAPI Deployment
```

---

# 🧠 Model Evolution

| Version | Description |
|----------|-------------|
| v1 | Initial DistilBERT Classifier |
| v2 | Fine-Tuned Model |
| v3 | Improved Dataset & Training |
| v4 | Final Production Model |

---

# 🛠️ Technology Stack

## Programming

- Python

---

## Machine Learning

- PyTorch
- Hugging Face Transformers
- Scikit-learn
- NumPy
- Pandas

---

## NLP

- DistilBERT
- Tokenization
- Text Classification
- Prompt Classification

---

## Backend

- FastAPI
- Uvicorn
- Pydantic

---

## Visualization

- Matplotlib
- SHAP
- Seaborn

---

# 🔬 Research Concepts

This project explores several modern AI Security concepts:

- Prompt Injection Detection
- Prompt Leakage Detection
- Jailbreak Detection
- Transformer Fine-Tuning
- Ensemble Learning
- Explainable AI (XAI)
- Hard Negative Mining
- Feature Engineering
- Adversarial Evaluation
- Secure LLM Deployment

---

# 📊 Model Evaluation

The framework evaluates model performance using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix
- Failure Analysis

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/yourusername/SecurePrompt.git
```

---

## Navigate

```bash
cd SecurePrompt
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Training Workflow

```text
01_model_builder.ipynb
          │
          ▼
02_distilbert_training.ipynb
          │
          ▼
03_finetune_patch.ipynb
          │
          ▼
04_hard_negative_mining.ipynb
          │
          ▼
05_feature_engineering.ipynb
          │
          ▼
06_ensemble.ipynb
          │
          ▼
07_distilbert_v4_hardtrained.ipynb
          │
          ▼
08_adversarial_eval.ipynb
```

---

# 🌟 Core Capabilities

✅ Prompt Injection Detection

✅ Jailbreak Detection

✅ Prompt Leakage Detection

✅ Transformer Fine-Tuning

✅ Ensemble Prediction

✅ Explainable AI

✅ Hard Negative Mining

✅ FastAPI Backend

✅ Production Model Export

---

# 📈 Future Improvements

The roadmap for SecurePrompt includes:

- Continual Learning
- Concept Drift Detection
- Adaptive Ensemble Learning
- Online Hard Negative Mining
- Multi-turn Prompt Injection Detection
- Self-Healing Security Framework
- Retrieval-Augmented Detection
- LLM Guardrails Integration

---

# 🤝 Contributing

Contributions are welcome.

If you would like to improve SecurePrompt:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

Please ensure your code follows project conventions and includes appropriate documentation.

---

# 📚 Learning Outcomes

This project demonstrates practical implementation of:

- Natural Language Processing (NLP)
- Transformer Models
- Prompt Injection Detection
- AI Security
- Explainable AI
- Model Training
- Model Evaluation
- Backend API Development
- Production ML Systems
- MLOps Fundamentals

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 🙏 Acknowledgements

This project is built using the open-source ecosystem:

- Hugging Face Transformers
- PyTorch
- FastAPI
- Scikit-learn
- NumPy
- Pandas
- Matplotlib

Special thanks to the AI Security and Open Source communities for advancing research in LLM safety.

---

<div align="center">

## ⭐ If you find this project useful, consider giving it a Star!

**SecurePrompt — Building Safer AI Systems Through Intelligent Prompt Security**

</div>
