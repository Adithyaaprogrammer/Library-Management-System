# Deployment of Flask in the backend

## Creation of virtual environment inside Code folder
python -m venv myenv

## Activation of virtual memory
source myenv/Scripts/activate

## Installation of necessary libraries
pip install -r requirements.txt

## deployment of the Backend 
flask run --debug

The backend runs in the http://127.0.0.1:5000

# NPM for local deployment of the frontend

## Installation of npm inside the frontend folder
npm install

### Compilation and hot-relod for the deployment locally
npm run serve

## Production building
npm run build

the  App run in the server  http://10.10.92.36:8080/

## for redis-celery functionality run this code in the ubuntu terminal
celery -A app:celery_app worker -l INFO
~/go/bin/MailHog
celery -A app:celery_app beat -l INFO
