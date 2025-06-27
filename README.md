# Hotel Reservation MLOps Project

This project is an end-to-end MLOps solution for a hotel reservation prediction task. The goal is to predict whether a hotel booking will be canceled or not based on various features of the reservation. The project includes data ingestion, preprocessing, model training, and a Flask web application for inference.

## Project Structure

```
.
├── app.py                  # Flask application for serving the model
├── requirements.txt        # Project dependencies
├── Dockerfile              # Dockerfile for the main application
├── Jenkinsfile             # Jenkins pipeline configuration
├── custom_jenkins/         # Dockerfile for a custom Jenkins image
├── pipeline/               # Main training pipeline
│   └── training_pipeline.py
├── src/                    # Source code for different project modules
│   ├── data_ingestion.py
│   ├── data_preprocessing.py
│   └── model_training.py
├── templates/              # HTML templates for the Flask app
│   └── index.html
├── static/                 # Static files (CSS) for the Flask app
│   └── style.css
├── artifacts/              # Stores raw data, processed data, and trained models
├── config/                 # Configuration files
├── notebook/               # Jupyter notebook for exploratory data analysis
└── ...
```

## Features

- **Data Ingestion**: Ingests data from a specified source.
- **Data Preprocessing**: Cleans and preprocesses the data, including handling categorical features and splitting the data into training and testing sets.
- **Model Training**: Trains a LightGBM (LGBM) model on the preprocessed data.
- **MLflow Integration**: Uses MLflow for experiment tracking and model management.
- **Flask Web Application**: A simple web interface to interact with the trained model and get predictions.
- **CI/CD Pipeline**: Includes a `Jenkinsfile` for automating the build, test, and deployment process.
- **Dockerization**: `Dockerfile` is provided to containerize the application.

## Getting Started

### Prerequisites

- Python 3.x
- Docker
- Jenkins (optional, for CI/CD)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Training Pipeline

To run the complete training pipeline, which includes data ingestion, preprocessing, and model training, execute the following command:

```bash
python pipeline/training_pipeline.py
```

This will:
1.  Ingest the raw data into the `artifacts/raw` directory.
2.  Preprocess the data and save it to the `artifacts/process` directory.
3.  Train the model and save the final `lgbm_model.pkl` to the `artifacts/models` directory.

### Running the Flask Application

Once the model is trained, you can start the Flask web application to serve predictions.

```bash
python app.py
```

The application will be available at `http://localhost:8080`. You can open this URL in your browser to access the prediction interface.

## Model

The model used in this project is a **LightGBM Classifier**. It is trained to predict the `booking_status` (Canceled or Not Canceled). The trained model is saved as `lgbm_model.pkl` in the `artifacts/models/` directory.

## CI/CD with Jenkins

A `Jenkinsfile` is included to set up a CI/CD pipeline. This pipeline can be configured to automatically:
- Build a Docker image for the application.
- Run tests.
- Deploy the application.

A `Dockerfile` for a custom Jenkins image with necessary tools is also provided in the `custom_jenkins` directory.
