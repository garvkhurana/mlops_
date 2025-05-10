pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'your-ecr-repo-name'
        ECR_REGISTRY = 'aws_account_id.dkr.ecr.us-east-1.amazonaws.com'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        EC2_INSTANCE_IP = 'your-ec2-instance-public-ip'
        EC2_SSH_USER = 'ec2-user'  // or the appropriate username for your EC2 instance
        EC2_SSH_KEY = credentials('ec2-ssh-key-id')  // Replace with your SSH key credentials ID
        AWS_CREDENTIALS = credentials('aws-credentials-id')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/garvkhurana/mlops_'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $garv:$garv_khurana .'
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: "${AWS_CREDENTIALS}"]]) {
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
                sh """
                    docker tag $garv:$garv_khurana $ECR_REGISTRY/$garv:$garv_khurana
                    docker push $ECR_REGISTRY/$garv:$garv_khurana
                """
            }
        }

        stage('Deploy to EC2') {
            steps {
                withCredentials([file(credentialsId: "${EC2_SSH_KEY}", variable: 'EC2_SSH_KEY_PATH')]) {
                    sh """
                        # SSH into EC2 and deploy the Docker container
                        ssh -o StrictHostKeyChecking=no -i $EC2_SSH_KEY_PATH $EC2_SSH_USER@$EC2_INSTANCE_IP << 'EOF'
                            # Pull the latest Docker image from ECR
                            aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
                            docker pull $ECR_REGISTRY/$garv:$garv_khurana

                            # Run the Docker container (stop any previous container first)
                            docker stop garv_container || true
                            docker rm garv_container || true
                            docker run -d --name garv_container -p 5000:5000 $ECR_REGISTRY/$garv:$garv_khurana
                        EOF
                    """
                }
            }
        }
    }
}
