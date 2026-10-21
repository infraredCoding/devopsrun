# devopsrun

A deliberately over-engineered DevOps project: a tiny Flask app wrapped in a semi-production-grade CI/CD pipeline. The app is a throwaway; the point is to see how **Docker, Kubernetes, Terraform, GitHub Actions and ArgoCD** fit together.

## Architecture

```
git push → GitHub Actions (pytest → build image → push to Docker Hub → bump image tag in k8s/deployment.yaml)
                                                                          ↓
                                    ArgoCD watches the repo → syncs manifests → Kubernetes rolling update
```

Terraform provisions the local Minikube cluster (Docker driver) that everything runs on.

## Tech stack

| Layer | Tool |
|---|---|
| App | Flask |
| Tests | pytest |
| Containers | Docker |
| Orchestration | Kubernetes (Minikube) |
| Infrastructure as Code | Terraform |
| CI | GitHub Actions |
| CD (GitOps) | ArgoCD |

## The app

A book-to-author lookup backed by an in-memory `dict`, with no database.

| Endpoint | Response |
|---|---|
| `GET /` | `Welcome to the Book Writer App!` (used for health checks) |
| `GET /<book_name>` | Author name, or `Book not found` |

## Project structure

```
src/                 Flask app, Dockerfile, requirements, tests
k8s/                 deployment.yaml (2 replicas, probes, resource limits) and service.yaml (NodePort)
terraform/           Minikube cluster provisioning
.github/workflows/   CI pipeline
```

## Getting started

**Run tests**
```bash
pip install -r src/requirements.txt
pytest ./tests
```

**Run with Docker**
```bash
docker build -t devopsrun ./src
docker run -p 5000:5000 devopsrun
```

**Provision the cluster**
```bash
cd terraform
terraform init && terraform apply
minikube start
```

**Deploy manually**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

**Deploy with ArgoCD**
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
Then add this repo as an application in the ArgoCD UI. Every change to `k8s/` is synced and rolled out automatically.

## CI/CD pipeline

Triggered on pushes and pull requests to `main`:

1. **test**: runs pytest.
2. **build_and_push**: builds the image tagged with the short commit SHA, pushes it to Docker Hub, replaces the `IMAGE_TAG` placeholder in `k8s/deployment.yaml`, and commits the change with `[skip ci]` to avoid a loop.

Required repository secrets: `DOCKER_USERNAME`, `DOCKERHUB_TOKEN`.

## Known shortcuts

- Flask dev server instead of `gunicorn`
- Minikube instead of a managed cloud cluster
- Terraform used for local provisioning only

## Further reading

Full write-up: [(Shallow) Dive into DevOps](https://www.imraninfrared.com/blogs/shallow-dive-into-devops), linked from my blog.
