# Contributing
Guidelines to follow when contributing to NP-Portfolio-2.

## Setup
Development Setup with Docker-Compose:
1. Build docker images
```
docker-compose build
```
2. Bring up development stack
```
docker-compose up
```

### Backend
Dependencies & Prerequisites:
- python version 3.7

Development setup without docker:
1. Install module dependencies:
```
cd src/backend
pip install -r requirements.txt
```
2. Perform database migrations
```
flask db upgrade
```
3. Run the backend server
```
python run.py
```
## Branches
Branches used in the project:
- develop - main develop branch
    - strive to be stable and not break
- release/X - release branch for release X
    - should be mostly stable and not break
- master - current release version
    - should be almost completely stable and not break
> Use feature branches on to work on high risk 'something would break' features.

## Project Structure
- `src/` - source code
    - `frontend/` - website fontend
    - `backend/` - backend service
        - `models/` - backend models
            - `iam/` - identity and user managment 
            - `notification/` - notification 
            - `asssignment/` - assignment 
        - `api/` - backend api routes
            - `iam/` - identity and user managment 
            - `notification/` - notification 
            - `asssignment/` - assignment 
        - `mapping/` - mappings between models and json representation
    - `pi/` - Raspberry PI
- `containers/` - docker containers 
