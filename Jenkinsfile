pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'garv'
        ECR_REGISTRY = '970547369783.dkr.ecr.us-east-1.amazonaws.com'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        EC2_INSTANCE_IP = '54.81.45.32'
        EC2_SSH_USER = 'ubuntu'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/garvkhurana/mlops_'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def image = "url:${IMAGE_TAG}"
                    bat "docker build -t ${image} ."
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([[ 
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws'
                ]]) {
                    bat """
                        aws configure set aws_access_key_id %AWS_ACCESS_KEY_ID%
                        aws configure set aws_secret_access_key %AWS_SECRET_ACCESS_KEY%
                        aws configure set region ${AWS_REGION}
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                    """
                }
            }
        }

        stage('Push Image to ECR') {
            steps {
                script {
                    def image = "url:${IMAGE_TAG}"
                    def fullImage = "${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
                    bat """
                        docker tag ${image} ${fullImage}
                        docker push ${fullImage}
                    """
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                withCredentials([sshUserPrivateKey(
                    credentialsId: 'jenkins_user',
                    keyFileVariable: 'SSH_KEY_PATH',
                    usernameVariable: 'EC2_USER'
                )]) {
                    script {
                        def fullImage = "${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
                        bat """
                            ssh -o StrictHostKeyChecking=no -i %SSH_KEY_PATH% %EC2_USER%@${EC2_INSTANCE_IP} ^
                                "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY} &&
                                docker pull ${fullImage} &&
                                docker stop garv_container || true &&
                                docker rm garv_container || true &&
                                docker run -d --name garv_container -p 5000:5000 ${fullImage}"
                        """
                    }
                }
            }
        }
    }
}
