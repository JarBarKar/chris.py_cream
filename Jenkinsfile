pipeline {
    agent any


    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/*']], extensions: [], 
                userRemoteConfigs: [[credentialsId: 'spm_g2t4', 
                url: 'https://github.com/Alvan-Tan/chris.py_cream.git']]])
                
                script {
                     Author_ID=sh(script: "git show -s --pretty=%an", returnStdout: true).trim()
                     Author_Name=sh(script: "git show -s --pretty=%ae", returnStdout: true).trim()
                }
                echo "${Author_ID} and ${Author_Name}"
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
                python3 course_integration_tests.py
                python3 content_integration_tests.py
                python3 quiz_integration_tests.py
                python3 section_integration_tests.py
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