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

        stage('SonarQube Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fastapi-app:latest .'
            }
        }

        stage('Push to Registry') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker tag fastapi-app:latest $DOCKER_USER/fastapi-app:latest
                    docker push $DOCKER_USER/fastapi-app:latest
                    '''
                }
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