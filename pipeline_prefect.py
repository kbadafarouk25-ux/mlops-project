import argparse
import subprocess  # nosec B404
import sys

from prefect import flow, task

PROJECT_DIR = "."
FILES = ["model_pipeline.py", "main.py", "pipeline_prefect.py"]


# ==================================================
# TASKS : PREPARATION, ENTRAINEMENT, SAUVEGARDE,
#         CHARGEMENT ET EVALUATION
# ==================================================


@task
def installer_dependances():
    """Installer les dépendances du projet."""
    subprocess.run(  # nosec B603
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            "requirements.txt",
        ],
        cwd=PROJECT_DIR,
        check=True,
    )


@task
def preparation_donnees():
    """Préparation des données."""
    print("Preparation des donnees...")


@task
def entrainement_modele():
    """Entraînement du modèle."""
    print("Entrainement du modele...")


@task
def sauvegarder_modele():
    """Sauvegarde du modèle."""
    print("Sauvegarde du modele...")


@task
def charger_modele():
    """Chargement du modèle."""
    print("Chargement du modele...")


@task
def evaluation_modele():
    """Évaluation du modèle."""
    print("Evaluation du modele...")


# ==================================================
# TASKS : FORMATAGE, QUALITE, SECURITE ET TESTS
# ==================================================


@task
def format_code():
    """Formater le code avec Black."""
    subprocess.run(  # nosec B603
        [
            sys.executable,
            "-m",
            "black",
            *FILES,
        ],
        cwd=PROJECT_DIR,
        check=True,
    )


@task
def check_code_quality():
    """Vérifier la qualité du code avec Ruff."""
    subprocess.run(  # nosec B603
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            *FILES,
        ],
        cwd=PROJECT_DIR,
        check=True,
    )


@task
def check_code_security():
    """Vérifier la sécurité du code avec Bandit."""
    subprocess.run(  # nosec B603
        [
            sys.executable,
            "-m",
            "bandit",
            "-q",
            *FILES,
        ],
        cwd=PROJECT_DIR,
        check=True,
    )


@task
def run_unit_tests():
    """Exécuter les tests unitaires avec Pytest."""
    subprocess.run(  # nosec B603
        [
            sys.executable,
            "-m",
            "pytest",
            "tests",
        ],
        cwd=PROJECT_DIR,
        check=True,
    )


# ==================================================
# FLOWS
# ==================================================


@flow
def train():
    """Flow d'entraînement du modèle."""
    installer_dependances()
    preparation_donnees()
    entrainement_modele()
    sauvegarder_modele()


@flow
def evaluate():
    """Flow d'évaluation du modèle."""
    installer_dependances()
    charger_modele()
    evaluation_modele()


@flow
def code():
    """Flow de vérification du code (formatage, qualité, sécurité, tests)."""
    format_code()
    check_code_quality()
    check_code_security()
    run_unit_tests()


@flow
def all():
    """Flow complet : entraînement, évaluation et vérifications du code."""
    installer_dependances()
    preparation_donnees()
    entrainement_modele()
    sauvegarder_modele()
    charger_modele()
    evaluation_modele()
    format_code()
    check_code_quality()
    check_code_security()
    run_unit_tests()


# ==================================================
# POINT D'ENTREE
# ==================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline Prefect MLOps")
    parser.add_argument(
        "--flow",
        choices=["train", "evaluate", "code", "all"],
        required=True,
        help="Flow à exécuter",
    )
    args = parser.parse_args()

    flows = {
        "train": train,
        "evaluate": evaluate,
        "code": code,
        "all": all,
    }

    flows[args.flow]()
