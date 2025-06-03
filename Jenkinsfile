pipeline { 
    agent any
    
    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Cloning GitHub Repo to Jenkins') {
            steps {
                echo 'Clone GitHub repository to Jenkins...'
                checkout scm
            }
        }

        stage('Setting up Python Virtual Environment and Installing Dependencies') {
            steps {
                echo 'Clone GitHub repository to Jenkins...'
                sh '''
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -e .
                '''
            }
        }
    }
}