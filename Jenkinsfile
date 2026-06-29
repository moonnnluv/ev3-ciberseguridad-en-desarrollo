pipeline {
    agent any

    environment {
        IMAGE_NAME = "ep3-flask"
        CONTAINER_NAME = "ep3-flask-container"
        APP_PORT = "5000"
        ZAP_REPORT = "zap-report.html"
    }

    stages {

        stage('Build') {
            steps {
                echo 'Construyendo la imagen Docker de la app Flask...'
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
            }
        }

        stage('Test') {
            steps {
                echo 'Corriendo tests automatizados dentro de un contenedor temporal...'
                sh "docker run --rm ${IMAGE_NAME}:latest python -m pytest test_app.py -v"
            }
        }

        stage('Security Scan (OWASP ZAP)') {
            steps {
                echo 'Levantando la app temporalmente para escanearla con OWASP ZAP...'
                sh "docker run -d --name ${CONTAINER_NAME}-scan -p 5050:${APP_PORT} ${IMAGE_NAME}:latest"
                sh "sleep 5"
                sh """
                    docker run --rm --network host \
                    -v \$(pwd):/zap/wrk/:rw \
                    zaproxy/zap-stable zap-baseline.py \
                    -t http://localhost:5050 \
                    -r ${ZAP_REPORT} || true
                """
                sh "docker stop ${CONTAINER_NAME}-scan || true"
                sh "docker rm ${CONTAINER_NAME}-scan || true"
            }
        }

        stage('Deploy') {
            steps {
                echo 'Desplegando contenedor final...'
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
                sh "docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} ${IMAGE_NAME}:latest"
            }
        }
    }

    post {
        always {
            echo 'Pipeline finalizado. Archivando reporte de seguridad si existe...'
            archiveArtifacts artifacts: "${ZAP_REPORT}", allowEmptyArchive: true
        }
        success {
            echo 'Pipeline ejecutado con éxito: build, test, escaneo y despliegue completados.'
        }
        failure {
            echo 'El pipeline falló en alguna etapa. Revisar logs de Jenkins.'
        }
    }
}
