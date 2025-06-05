pipeline { 
    agent any
    
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'eng-node-458415-j3'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin/'
    }

    stages {
        stage('Cloning Github repo to Jenkins'){
            steps{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scm
                    // checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github Cred', url: 'https://github.com/JoeUzo/Hotel-Reservation-Predicition.git']])
            }
        }

        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and pushing Docker image to GCR'){
            steps{
                echo 'Building and pushing Docker image to GCR'
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_APP_KEY')]) {
                    sh ''' 
                    export PATH=$PATH:${GCLOUD_PATH}
                    gcloud auth activate-service-account --key-file=${GCP_APP_KEY}
                    gcloud config set project ${GCP_PROJECT}
                    gcloud auth configure-docker --quiet

                    docker build -t gcr.io/${GCP_PROJECT}/hotel-reservation-prediction:latest .
                    docker push gcr.io/${GCP_PROJECT}/hotel-reservation-prediction:latest
                    '''
                }
            }
        }

        stage('Deploying to Google Cloud Run'){
            steps{
                echo 'Deploying to  Google Cloud Run'
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_APP_KEY')]) {
                    sh '''
                    export PATH=$PATH:${GCLOUD_PATH}
                    gcloud auth activate-service-account --key-file=${GCP_APP_KEY}
                    gcloud config set project ${GCP_PROJECT}

                    gcloud run deploy hotel-reservation-prediction \
                    --image=gcr.io/${GCP_PROJECT}/hotel-reservation-prediction:latest \
                    --platform=managed \
                    --region=us-central-1 \
                    --allow=unauthenticated 

                    '''
                }
            }
        }
    }
}