Lab 5.1 – CI/CD Pipeline for Flask Application
1. Project Overview

This project is a CI/CD pipeline for a Flask application with a SQLite database. The pipeline uses Jenkins to automate testing, building, deploying, and notifying via Slack. The goal is to demonstrate a complete DevOps workflow, including static code analysis, dynamic testing, data persistence, and multi-environment deployment (DEV/PROD).

2. Jenkins Pipeline Stages
Stage	Description	Purpose / Test
Code Checkout	Pulls source code from GitHub (225-lab5-1b)	Ensures the pipeline always uses the latest code
Lint HTML	Runs HTMLHint on all HTML files	Static test for HTML quality
Static Tests	Python syntax (py_compile) and YAML linter (yaml.safe_load_all)	Checks Python and Kubernetes YAML for errors before build
Build & Push Docker Image	Builds Docker image (Dockerfile.build) and pushes to Docker Hub	Containerization for consistent deployments
Deploy to DEV	Applies deployment-dev.yaml using kubectl	Deploys app to a test environment
Security Checks	Runs DAST scan using public.ecr.aws/portswigger/dastardly	Detects potential security vulnerabilities
Reset DB	Clears SQLite database (DELETE FROM parts)	Ensures a clean state for dynamic tests
Generate Test Data	Runs data-gen.py to populate database	Prepares the application for functional testing
Acceptance Tests	Runs QA container (docker run qa-tests)	Dynamic code testing to verify app functionality
Remove Test Data	Runs data-clear.py	Cleans up the database after testing
Deploy to PROD	Applies deployment-prod.yaml using kubectl	Deploys the application to production environment
Check Kubernetes Cluster	Runs kubectl get all	Verifies pods, services, and deployments
ChatOps / Slack Notification	Sends messages to Slack on success, failure, or unstable build	Provides immediate CI/CD feedback
3. Data Persistence

The Flask application uses a persistent SQLite database stored on an NFS volume:

PersistentVolume (PV):

kind: PersistentVolume
name: flask-pv
nfs:
  path: /srv/nfs/hibbarkm
  server: 10.48.228.25
accessModes: ReadWriteMany
storage: 1Gi


PersistentVolumeClaim (PVC):

kind: PersistentVolumeClaim
name: flask-pvc
accessModes: ReadWriteMany
storage: 1Gi
selector:
  matchLabels:
    type: nfs


The Flask container mounts the PVC at /nfs:

volumeMounts:
  - name: nfs-storage
    mountPath: /nfs




4. Static & Dynamic Testing
Static Tests

Python syntax: python3 -m py_compile $(find . -name "*.py")

YAML linter: Checks all .yaml files using yaml.safe_load_all (supports multiple documents)

HTML lint: HTMLHint verifies HTML quality

Dynamic Tests

Acceptance tests: Run in QA Docker container (docker run qa-tests)

Database reset and test data generation ensure consistent test results

Screenshot Placeholder: Jenkins console showing static and dynamic test success.

5. DEV/PROD Deployments

DEV: deployment-dev.yaml – single replica, test environment

PROD: deployment-prod.yaml – production deployment

Both environments use the same Docker image tag generated during the build.

Screenshot Placeholder: DEV deployment and PROD deployment pods running.

6. ChatOps Integration

Slack notifications configured in Jenkins post section:

Success: Green message with build number

Unstable: Yellow warning

Failure: Red message





8. Summary / Conclusion

Pipeline successfully demonstrates CI/CD with:

Docker build and push

Static code tests (Python, YAML, HTML)

Dynamic tests with QA container

Data persistence with NFS PV/PVC

DEV and PROD deployments

Slack notifications for ChatOps

Optional enhancements: YAML linter added for multiple document support, ensuring pipeline robustness


