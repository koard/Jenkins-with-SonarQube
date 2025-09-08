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
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner'
                    withSonarQubeEnv() {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }


        stage('Build Docker Image') {
            agent {
                docker {
                    image 'docker:latest'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh 'docker build -t fastapi-app:latest .'
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                docker run -d \
                  -p 8080:8000 \  # เปลี่ยนพอร์ต host:container ตามต้องการ
                  -e ENV_NAME=production \  # เพิ่ม environment variable
                  --name fastapi-app \
                  fastapi-app:latest
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
    }
}