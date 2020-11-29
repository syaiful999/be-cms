SERVER_ENV=$1 # ex : dev / uat / prod
IMAGE_TAG=$2 # ex : 1.0.0-dev / 1.0.0-dev / 1.0.0

if [ -z "$SERVER_ENV" ]; then
  echo "Please provide server environment!"
  exit 1
fi

if [ -z "$IMAGE_TAG" ]; then
  echo "Please provide docker image tag!"
  exit 1
fi

set -e
cd $WORKSPACE/src/fms-python-service-$SERVER_ENV

cat /tmp/regpass | sudo docker login --username admin --password-stdin docker-registry.indikaenergy.co.id
sudo docker build --build-arg SERVER_ENV=$SERVER_ENV --build-arg VERSION=$IMAGE_TAG -t docker-registry.indikaenergy.co.id/ext/fms/python-service:$IMAGE_TAG .
sudo docker push docker-registry.indikaenergy.co.id/ext/fms/python-service:$IMAGE_TAG