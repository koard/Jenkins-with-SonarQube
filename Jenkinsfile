pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonarqube_token') 
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/koard/Jenkins-with-SonarQube.git'
            }
        }

        stage('Setup Python & Install Dependencies') {
            agent {
                docker {
                    image 'python:3.11'
                }
            }
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install pytest pytest-cov
                '''
            }
        }

        stage('Run Tests & Generate Coverage') {
            agent {
                docker {
                    image 'python:3.11'
                }
            }
            steps {
                sh '''
                . venv/bin/activate
                export PYTHONPATH=$PWD
                pytest --maxfail=1 --disable-warnings -q --cov=app --cov-report=xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            def scannerHome = tool 'sonar-scanner' // 'Sonarscanner' คือชื่อที่ตั้งไว้ใน Jenkins > Manage Jenkins > Tools
            withSonarQubeEnv() { // หรือใส่ชื่อ server เช่น withSonarQubeEnv('MySonarQube')
            sh "${scannerHome}/bin/sonar-scanner"
            }
        }


        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fastapi-app:latest .'
            }
        }

        stage('Deploy Container') {
            steps {
                sh 'docker run -d -p 8000:8000 fastapi-app:latest'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
    }
}