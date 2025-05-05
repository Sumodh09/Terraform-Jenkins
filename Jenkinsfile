def installTerraform() {
    // Check if terraform is already installed
    def terraformExists = sh(script: 'which terraform', returnStatus: true)
    if (terraformExists != 0) {
        // Install terraform
        sh '''
            echo "Installing Terraform..."
            wget https://releases.hashicorp.com/terraform/1.0.0/terraform_1.0.0_linux_amd64.zip
            unzip terraform_1.0.0_linux_amd64.zip
            sudo mv terraform /usr/local/bin/
            rm -f terraform_1.0.0_linux_amd64.zip
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
       			#terraform output lambda_response | sed 's/\\n/\n/g; s/\\"/"/g; s/\\\\/\\/g' | column -t -s,
			    result=$(terraform output -raw lambda_response)

			    if [[ $result == *"NON_COMPLIANT"* ]]; then
		              echo "Non-Complaint is present will destroy the CFT template and whatever resources asscoiated with CFT except S3 bucket Compliance report"
			      terraform destroy -target=null_resource.zip_python_script -target=null_resource.zip_python_script_name -target=aws_cloudformation_stack.config_rules_stack -auto-approve
		            else
		              echo "Non-compliant resource is not present."
			    fi
                        '''
                    }
                }
            }
        }
    }
}
