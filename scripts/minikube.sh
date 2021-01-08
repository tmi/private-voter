# turn off VPN :)
minikube start
kubectl create deployment private-voter --image=vojtatuma/private-voter:latest
kubectl expose deployment private-voter --type=LoadBalancer --port=8080
minikube service private-voter # to get the URL to call
curl <ip+port from the output above>/status
# minikube tunnel # to create a tunnel, but does not seem necessary
