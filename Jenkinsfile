pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '**']], extensions: [], 
                userRemoteConfigs: [[credentialsId: 'jenkin_private_key', 
                url: 'https://github.com/JarBarKar/chris.py_cream.git']]])
            }
        }
//         stage('Code Analysis') {
//             steps {
//             sh '''
//             python3 -m venv env
//             source env/bin/activate
//             pip3 install flake8
//             flake8 app.py
//             '''
//             }
//         }
        stage('Unit Test') {
              steps {
                sh '''
                python3 -m venv env
                source env/bin/activate
                pip3 install -r requirements.txt
                python3 content_integration_tests.py
                '''
            }
              post {
                always {
                        junit '**/test-reports/*.xml'
                    }
                }
        } 
    }
}

