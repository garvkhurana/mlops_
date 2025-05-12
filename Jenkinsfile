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
                    if (isUnix()) {
                        sh "docker build -t ${image} ."
                    } else {
                        bat "docker build -t ${image} ."
                    }
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([[ 
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws'
                ]]) {
                    script {
                        if (isUnix()) {
                            sh """
                                aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                            """
                        } else {
                            bat """
                                aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                            """
                        }
                    }
                }
            }
        }

        stage('Push Image to ECR') {
            steps {
                script {
                    def image = "url:${IMAGE_TAG}"
                    def fullImage = "${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
                    if (isUnix()) {
                        sh """
                            docker tag ${image} ${fullImage}
                            docker push ${fullImage}
                        """
                    } else {
                        bat """
                            docker tag ${image} ${fullImage}
                            docker push ${fullImage}
                        """
                    }
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
                        
                        // Use SSH to deploy Docker image on EC2
                        if (isUnix()) {
                            sh """
                                ssh -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} ${EC2_USER}@${EC2_INSTANCE_IP} "
                                sudo apt-get update -y && 
                                sudo apt-get install -y docker.io awscli && 
                                sudo systemctl start docker && 
                                sudo systemctl enable docker && 
                                aws ecr get-login-password --region ${AWS_REGION} | sudo docker login --username AWS --password-stdin ${ECR_REGISTRY} && 
                                docker pull ${fullImage} && 
                                docker stop garv_container 2>/dev/null && 
                                docker rm garv_container 2>/dev/null && 
                                docker run -d --name garv_container -p 5000:5000 ${fullImage}"
                            """
                        } else {
                            bat """
                                ssh -o StrictHostKeyChecking=no -i %SSH_KEY_PATH% %EC2_USER%@${EC2_INSTANCE_IP} ^
                                "sudo apt-get update -y && ^
                                sudo apt-get install -y docker.io awscli && ^
                                sudo systemctl start docker && ^
                                sudo systemctl enable docker && ^
                                aws ecr get-login-password --region ${AWS_REGION} | sudo docker login --username AWS --password-stdin ${ECR_REGISTRY} && ^
                                docker pull ${fullImage} && ^
                                docker stop garv_container 2>/dev/null && ^
                                docker rm garv_container 2>/dev/null && ^
                                docker run -d --name garv_container -p 5000:5000 ${fullImage}"
                            """
                        }
                    }
                }
            }
        }
    }
}
