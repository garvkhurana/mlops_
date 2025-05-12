pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'your-ecr-repo-name'
        ECR_REGISTRY = 'aws_account_id.dkr.ecr.us-east-1.amazonaws.com'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        EC2_INSTANCE_IP = 'your-ec2-instance-public-ip'
        EC2_SSH_USER = 'ec2-user'  // Replace if needed
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/garvkhurana/mlops_'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def image = "mlops_app:${IMAGE_TAG}"
                    sh "docker build -t ${image} ."
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials-id'
                ]]) {
                    sh """
                        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                        aws configure set region $AWS_REGION
                        aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
                    """
                }
            }
        }

        stage('Push Image to ECR') {
            steps {
                script {
                    def image = "mlops_app:${IMAGE_TAG}"
                    def fullImage = "${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
                    sh """
                        docker tag ${image} ${fullImage}
                        docker push ${fullImage}
                    """
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                withCredentials([file(credentialsId: 'ec2-ssh-key-id', variable: 'EC2_SSH_KEY_PATH')]) {
                    script {
                        def fullImage = "${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
                        sh """
                            ssh -o StrictHostKeyChecking=no -i $EC2_SSH_KEY_PATH $EC2_SSH_USER@$EC2_INSTANCE_IP << 'EOF'
                                aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
                                docker pull ${fullImage}
                                docker stop garv_container || true
                                docker rm garv_container || true
                                docker run -d --name garv_container -p 5000:5000 ${fullImage}
                            EOF
                        """
                    }
                }
            }
        }
    }
}
