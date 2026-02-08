#!/bin/bash
set -e

IMAGE="raf4lb/convo-ui:latest"
PLATFORM="linux/arm/v8"

npm i
npm run build

docker buildx build --platform $PLATFORM -t $IMAGE --push .

kubectl --kubeconfig=k8s/k8s.yaml apply -f k8s/deployment.yaml
kubectl --kubeconfig=k8s/k8s.yaml rollout restart deploy convo-ui
kubectl --kubeconfig=k8s/k8s.yaml apply -f k8s/service.yaml

echo "Deployment complete!"
