pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'registry.digitalocean.com'
        DOCKER_REPO_BACKEND = 'lead-generation-app-registry/backend'
        DOCKER_REPO_FRONTEND = 'lead-generation-app-registry/frontend'
        DOCKER_CREDENTIALS_ID = 'do-registry-credentials'
        SSH_CREDENTIALS_ID = 'droplet-ssh-credentials'
        DROPLET_IP = '159.89.4.217'
        DROPLET_USER = 'root'
        PROJECT_DIR = 'spotify-leads-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/consolenine/lead-generation-app.git'
            }
        }

        stage('Build Backend Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_REPO_BACKEND}:latest", './backend')
                }
            }
        }

        stage('Build Frontend Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_REPO_FRONTEND}:latest", './frontend')
                }
            }
        }

        stage('Login to DigitalOcean Registry') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS_ID}") {
                        echo 'Logged in to DigitalOcean Registry'
                    }
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_REPO_BACKEND}:latest").push()
                        docker.image("${DOCKER_REPO_FRONTEND}:latest").push()
                    }
                }
            }
        }

        stage('Deploy to DigitalOcean') {
            steps {
                sshagent (credentials: ["${SSH_CREDENTIALS_ID}"]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${DROPLET_USER}@${DROPLET_IP} << EOF
                    cd ${PROJECT_DIR}
                    docker-compose down
                    docker-compose pull
                    docker-compose up -d
                    EOF
                    """
                }
            }
        }
    }
}
