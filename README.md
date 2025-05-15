# Threat Analyzer with Multi-Agent System

This project implements a Threat Analyzer using a multi-agent system. It processes image data, extracts vision analysis, and predicts threat levels using machine learning models such as Gradient Boosting, Logistic Regression, or other classifiers.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Folder Structure](#folder-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Overview
The Threat Analyzer system is designed to:
- Analyze images and extract vision-related insights.
- Use machine learning models to predict threat levels based on extracted features.
- Provide a REST API for uploading images and retrieving predictions.

The system leverages:
- **FastAPI** for the backend.
- **BERT embeddings** for text feature extraction.
- Various machine learning models for classification.

## Features
- Upload images for threat analysis.
- Extract vision analysis and generate embeddings using BERT.
- Predict threat levels using trained machine learning models.
- Support for multiple classifiers (e.g., Gradient Boosting, Logistic Regression, Random Forest).
- REST API for seamless integration with other systems.

## Installation

### Prerequisites
- Python 3.10 or higher
- `pip` or `conda` for package management

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/threat-analyzer.git
    cd threat-analyzer
    ```
2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
5. Access the API documentation at:
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Usage

### 1. Upload an Image for Threat Analysis
Use the `/analyze_image_agent` endpoint to upload an image and get the predicted threat level.

#### Example Request (Using curl):
```bash
curl -X POST "http://127.0.0.1:8000/analyze_image_agent" \
-H "accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "file=@example.jpg" \
-F "request_type=classification"
```

## Endpoints

### 1. `/analyze_image_agent`
- **Method**: POST
- **Description**: Upload an image and get the predicted threat level.
- **Parameters**:
  - `file`: The image file to analyze.
  - `request_type`: The type of request (e.g., classification).
  - `additional_param`: Optional additional parameter.

## Folder Structure
```
Threat_Analyzer_Autogen_Multiagent/
├── app/
│   ├── main.py
│   ├── models/
│   ├── utils/
│   └── ...
├── data/
├── tests/
├── requirements.txt
└── README.md
```

## Technologies Used

### Backend:
- **FastAPI** - For building the REST API.
- **Pillow** - For image processing.

### Machine Learning:
- **scikit-learn** - For training and using classifiers.
- **PyTorch** - For embedding extraction and deep learning models.
- **XGBoost** - For Gradient Boosting.

### Text Embeddings:
- **BERT** - For extracting text embeddings.

### Other Tools:
- **Uvicorn** - ASGI server for FastAPI.
- **Joblib** - For saving and loading models.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

