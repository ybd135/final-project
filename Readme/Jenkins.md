## install Jenkins instance on Kubernetes cluster
(based on this page: [Install Jenkins using helm](https://sweetcode.io/how-to-setup-jenkins-ci-cd-pipeline-on-kubernetes-cluster-with-helm/))

### Requirements
- Installed kubectl command-line tool.
- Connected to a Kubernetes cluster - Have a kubeconfig file (default location is ~/.kube/config).
- Install helm.

### Create namespace
```
kubectl create namespace jenkins
```
 
### Install Jenkins
```
sudo apt install helm
```
Add jenkins to your helm repo:
```
helm repo add jenkins https://charts.jenkins.io
```

Update your repo:
```
helm repo update
```
Create a values.yaml file for the needed plugins (remember to update them later):
```
nano values.yaml
```
Paste the following code:
```
controller:
    installPlugins:
      - kubernetes:4029.v5712230ccb_f8
      - workflow-aggregator:596.v8c21c963d92d
      - git:5.2.0
      - configuration-as-code:1700.v6f448841296e
      - gitlab-plugin:1.7.16
      - blueocean:1.27.7
      - workflow-multibranch:756.v891d88f2cd46
      - login-theme:46.v36f624efb_23d
      - prometheus:2.3.3
      - github:1.37.3
      - github-oauth:588.vf696a_350572a_
      - email-ext:2.101
      - docker-plugin:1.5
      - docker-workflow:572.v950f58993843
    installLatestPlugins: true
    installLatestSpecifiedPlugins: true
```
Save and exit.

Install the official jenkins package with the new values file:
```
helm install --namespace jenkins myjenkins jenkins/jenkins -f values.yaml
```
Change the myjenkins service type to LoadBalancer:

```
kubectl patch svc myjenkins -p '{"spec": {"type": "LoadBalancer"}}' -n jenkins
```

Get the password:
```
kubectl get secret --namespace jenkins myjenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode
```
Get the LoadBalancer ip:
```
kubectl get svc --namespace=jenkins 
```
('default' is the default namespace for the installation, in this case we use jenkins ns) 

Go to the website where the IP is the external-service-IP of the 'Jenkins' service with port 8080

Login to jenkins using the username: 'admin' and the above password.

Install the suggested plugins and follow the given instructions.
### Create credentials
Click on "Manage Jenkins" on the left side. \
Click on the "Credentials" section. \
Click on "(global)" under Domain. \
![plot](../images/jenkinscred.png)
click +add credentials in blue in the top right corner and create username
with password kind both for your git repo and dockerhub. \
The description is then crucial for the definition of the pipeline.

### Install plugins

![plot](../images/jenkinsplugin.png)

Click on "Manage Jenkins" on the left side. \
Click on the "Plugins" section. \
Go to "Available plugins". \
Search for: 'Blue Ocean', 'Docker plugin', 'Docker', 'Kubernetes plugin', 'Pipeline', 'Email plugin' \
note that the multibranch workflow plugin is not supported anymore, and we now need to use the 
'Multibranch Pipeline' job type.

### Create pipeline job
In the Dashboard, click "+ New Item" \
Select 'Multibranch Pipeline', give a name, and click 'ok'. \
Give it a display name and description as you like. \
Under 'Branch Sources' select git. \
Enter this project url [repo](https://github.com/Milk18/final_project), and put the credentials we configured earlier.
The pipeline will search for a file called "Jenkinsfile" that exists in the main branch in this repo.
