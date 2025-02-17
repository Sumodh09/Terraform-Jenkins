def installTerraform() {
    // Check if Terraform is already installed
    def terraformExists = bat(script: 'where terraform', returnStatus: true)
    if (terraformExists != 0) {
        // Install Terraform
        bat '''
            echo Installing Terraform...
            powershell -Command "Invoke-WebRequest -Uri https://releases.hashicorp.com/terraform/1.0.0/terraform_1.0.0_windows_amd64.zip -OutFile terraform.zip"
            powershell -Command "Expand-Archive -Path terraform.zip -DestinationPath C:\\terraform -Force"
            powershell -Command "Move-Item -Path C:\\terraform\\terraform.exe -Destination C:\\Windows\\System32\\terraform.exe"
            del terraform.zip
        '''
    } else {
        echo "Terraform already installed!"
    }
}


pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                // Pull the git repo
                cleanWs()
                checkout scm
            }
        }

        stage('Install Terraform') {
            steps {
                script {
                  installTerraform()
            }

          }
	}
        stage('Terraform Deployment') {
            steps {
                script {
                    // CD into deployment folder and run terraform commands
                    dir('deployment') {
                        sh '''
                            terraform init
                            terraform plan
                            terraform apply -auto-approve
                        '''
                    }
                }
            }
        }
    }
}
