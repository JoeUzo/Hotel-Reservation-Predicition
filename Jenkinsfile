pipeline { 
    agent any

    stages {
        stage('Cloning GitHub Repo to Jenkins') {
            steps {
                echo 'Clone GitHub repository to Jenkins...'
                checkout scm
            }
        }
    }
}