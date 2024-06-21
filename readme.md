`docker build -f ./Dockerfile -t tarrakki/fdsdk .`
`docker run --name tarrakki_fd_sdk -d -p 8000:8000 --memory="500m" --memory-reservation="250m" --memory-swap="1.5g" --cpus="0.5" --cpu-shares=750 tarrakki/fdsdk uvicorn app.main:app`


1. Build docker image<br>
   `docker build --platform linux/arm64 -f ./Dockerfile -t 584934319897.dkr.ecr.ap-south-1.amazonaws.com/tarrakki/deposits/sfb:develop.latest-arm64 .`
   `docker build -f ./Dockerfile -t 584934319897.dkr.ecr.ap-south-1.amazonaws.com/tarrakki/deposits/sfb:develop.latest-arm64 .`
2. Login
   `aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 584934319897.dkr.ecr.ap-south-1.amazonaws.com`
3. Push image to ECR
   `docker push 584934319897.dkr.ecr.ap-south-1.amazonaws.com/tarrakki/deposits/sfb:develop.latest-arm64`
4. Update service
   `aws ecs update-service --cluster SandboxCluster-Arm64 --service TarrakkiDepositService-Sandbox --force-new-deployment --region ap-south-1`
5. Run migrations
   `aws ecs run-task  --cluster SandboxCluster-Arm64 --task-definition TarrakkiDepositServiceTaskDefinition-Sandbox-Arm64 --network-configuration '{ "awsvpcConfiguration": { "securityGroups": ["sg-68626102"], "subnets": ["subnet-04a4ffd21ee395459"]}}' --overrides '{ "containerOverrides": [ { "name": "TarrakkiDepositContainer-Sandbox-Arm64", "command": ["/bin/sh", "-c", "alembic upgrade head"] } ] }'`


   `aws ecs run-task  --cluster SandboxCluster-Arm64 --task-definition TarrakkiDepositServiceTaskDefinition-Sandbox-Arm64 --network-configuration '{ "awsvpcConfiguration": { "securityGroups": ["sg-68626102"], "subnets": ["subnet-04a4ffd21ee395459"]}}' --overrides '{ "containerOverrides": [ { "name": "TarrakkiDepositContainer-Sandbox-Arm64", "command": ["/bin/sh", "-c", "python -m src.tasks add_tenant ClC52XwuN2xWzt3CfgmN6OXoDZ6TqATOVCL06cqW myfi"] } ] }'`
