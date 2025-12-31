import subprocess
import sys


def run(cmd: str):
    print(f"\n>>> Executando: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"\n❌ ERRO ao executar: {cmd}")
        sys.exit(result.returncode)
    print("✔ Concluído com sucesso.")


def main():
    dockerfile = "./src/deploy/docker/Dockerfile"
    kubeconfig = "./src/deploy/k8s/k8s.yaml"
    deployment = "./src/deploy/k8s/deployment.yaml"
    deployment_name = "convo-api"
    service = "./src/deploy/k8s/service.yaml"
    image = "raf4lb/convo-api:latest"

    # 1) Build + multi-platform push
    run(
        f"docker buildx build "
        f"-f {dockerfile} "
        f"--platform linux/arm/v8 "
        f"-t {image} "
        f"--push ."
    )

    # 2) kubectl apply deployment
    run(f"kubectl --kubeconfig={kubeconfig} apply -f {deployment}")
    run(
        f"kubectl --kubeconfig={kubeconfig} rollout restart deployment {deployment_name}"
    )

    # 3) kubectl apply service
    run(f"kubectl --kubeconfig={kubeconfig} apply -f {service}")

    print("\n🚀 Deploy finalizado com sucesso!")


if __name__ == "__main__":
    main()
