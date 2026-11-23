from datetime import timedelta
from pipeline_prefect import all, code, evaluate, train

def deployer():
    # Déploiement du flow ALL avec une planification (toutes les 24h)
    # L'argument 'interval' accepte un objet timedelta ou une chaîne comme "24h"
    all.deploy(
        name="ml-pipeline-all",
        work_pool_name="default-process-pool", # Pool par défaut, souvent utilisé en local
        interval=timedelta(days=1),
        tags=["full-pipeline", "mlops"]
    )

    # Déploiement du flow TRAIN
    train.deploy(
        name="ml-pipeline-train",
        work_pool_name="default-process-pool",
        tags=["mlops", "training"]
    )

    # Déploiement du flow EVALUATE
    evaluate.deploy(
        name="ml-pipeline-evaluate",
        work_pool_name="default-process-pool",
        tags=["evaluation", "mlops"]
    )

    # Déploiement du flow CODE
    code.deploy(
        name="ml-pipeline-code",
        work_pool_name="default-process-pool",
        tags=["quality", "mlops"]
    )

if __name__ == "__main__":
    deployer()
