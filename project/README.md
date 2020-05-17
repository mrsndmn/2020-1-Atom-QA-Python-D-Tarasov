

```
podman pod create --name qa-project -p 8000-8080
podman run -d --pod qa-project --name qajenkins -v jenkins_home:/var/jenkins_home localhost/myjenkins

```