pipeline {
    agent {
        kubernetes {
            label 'dind-agent'
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: dind
    image: drpsychick/dind-buildx-helm
    alwaysPull: true
    securityContext:
      privileged: true
    volumeMounts:
    - mountPath: /var/run
      name: docker-sock
  volumes:
  - name: docker-sock
    emptyDir: {}
"""
        }
    }
    stages {
         stage('Run Tests and Build Docker Image') {
            steps {
                container('dind') {
                    script {
                        sh 'dockerd &'
                        sh 'sleep 5'
                        sh 'docker build -t milk49/profile-app:latest .'
                        sh 'docker run milk49/profile-app:latest test.py'
                        echo 'passed test'
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                container('dind') {
                    script {
                        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                            docker push milk49/profile-app:latest
                            '''
                        }
                    }
                }
            }
        }
        stage('Build and push helm chart') {
            steps {
                container('dind') {
                    script {
                        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                            helm package helmapp
                            helm push helmapp-0.1.0.tgz  oci://registry-1.docker.io/milk49
                            helm package helmdb
                            helm push helmdb-0.1.0.tgz  oci://registry-1.docker.io/milk49
                            '''
                        }
                    }
                }
            }
       }
    }
       post {
        failure {
            emailext (
                to: 'milk49@walla.co.il',
                subject: "Failed: ${currentBuild.fullDisplayName}",
                body: "The build failed. Please check the Jenkins build log for details.",
                attachLog: true,
            )
        }
    }
}
