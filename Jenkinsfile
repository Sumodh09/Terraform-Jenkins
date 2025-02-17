def installTerraform() {
    // Check if Git is installed
    def gitExists = bat(script: 'where git', returnStatus: true)
    if (gitExists != 0) {
        // Install Git
        bat '''
            echo Installing Git...
            powershell -Command "Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.1/Git-2.42.0-64-bit.exe -OutFile git-installer.exe"
            powershell -Command "Start-Process -FilePath git-installer.exe -ArgumentList '/VERYSILENT /NORESTART' -Wait"
            del git-installer.exe
        '''
    } else {
        echo "Git already installed!"
    }

    // Check if Terraform is installed
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
