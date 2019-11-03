# Contributing
Guidelines to follow when contributing to NP-Portfolio-2.

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
    - `backend/` - backend server
        - `notification/` - notification service
        - `object/` - object service
    - `pi/` - Raspberry PI
- `containers/` - docker containers. 

