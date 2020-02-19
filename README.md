# Memento
NP Portfolio 2 - Project.

## Intro
![Banner](./assets/banner.png)
Memento attempts to address the problem task switching for people with ASD by 
providing a task managment system to help People with ASD switch tasks in 
a timely manner to ensure the punctual completion of tasks.

## Setup
1. Fill `.env` with secrets:
    - Make a copy of `env` file as `.env` and fill it with secrets
2. Deploy Memento
    1. Docker Compose - Single machine setup
        - Pull docker images `docker-compose pull`
        - Run memento stack `docker-compose up`
    2. Kubernetes Cluster setup
        - Prerequisites: K8s Cluster, nginx-ingress controller, cert-manager (optional), helm v3
        - Copy `.env` file to `chart/.env`
        - Deploy memento stack `helm upgrade -n memento --install memento chart`

## Credits
The people that make this project possible:
- Ana @idlefrenchfry - Frontend 
- Adele @Adelollipop - UI/UX Design, Frontend
- Jun Ye @KJY-99 - Backend
- Zhu Zhanyan @mrzzy - Backend, Raspberry Pi
- Guhesh - Raspberry Pi
