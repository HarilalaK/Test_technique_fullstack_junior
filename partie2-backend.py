# Partie 2 – Backend (Python)

## Classe Task et fonctions associées


class Task:
    def __init__(self, name, project, priority, is_blocked=False, block_reason=None):
        self.name = name
        self.project = project
        self.priority = priority  # 1 = haute, 2 = moyenne, 3 = basse
        self.is_blocked = is_blocked
        self.block_reason = block_reason

    def set_blocked(self, is_blocked: bool, block_reason: str = None):
        """
        Change le statut de blocage d'une tâche.
        
        Règle simple : si on bloque la tâche, il faut obligatoirement une raison.
        La raison ne peut pas être vide ou juste des espaces.
        
        Lève une erreur si la règle n'est pas respectée.
        """
        if is_blocked:
            if not block_reason or not block_reason.strip():
                raise ValueError(
                    "Il faut donner une raison quand on bloque une tâche."
                )

        self.is_blocked = is_blocked
        self.block_reason = block_reason.strip() if block_reason else None

    def __repr__(self):
        return (
            f"Task(name={self.name!r}, project={self.project!r}, "
            f"priority={self.priority}, is_blocked={self.is_blocked}, "
            f"block_reason={self.block_reason!r})"
        )


# --------------------------------------------------------
# 1. Fonction pour trouver et trier les tâches bloquées
# -------------------------------------------------------

def get_blocked_tasks(tasks: list[Task]) -> list[Task]:
    """
    Renvoie seulement les tâches bloquées, bien rangées :
    - d'abord par priorité (1 avant 2 avant 3)
    - ensuite par ordre alphabétique du nom
    """
    blocked = [task for task in tasks if task.is_blocked]
    blocked.sort(key=lambda task: (task.priority, task.name))
    return blocked


# -----------------------------
# Exemples pour tester le code
# -----------------------------

if __name__ == "__main__":

    # --- Création de quelques tâches ---
    tasks = [
        Task("Configurer le serveur",        "Client A", priority=1, is_blocked=True,  block_reason="En attente des accès"),
        Task("Rédiger la documentation",     "Interne",  priority=3, is_blocked=True,  block_reason="Manque d'informations"),
        Task("Mettre à jour le schéma",      "Client B", priority=2, is_blocked=False),
        Task("Déployer en production",       "Client A", priority=1, is_blocked=True,  block_reason="Tests non validés"),
        Task("Analyser les besoins",         "Client C", priority=2, is_blocked=True,  block_reason="Réunion annulée"),
        Task("Corriger le bug d'affichage",  "Interne",  priority=1, is_blocked=False),
    ]

    # --- Test de la fonction get_blocked_tasks ---
    print("=== Tâches bloquées (bien triées) ===")
    for t in get_blocked_tasks(tasks):
        print(f"  [{t.priority}] {t.name!r} — {t.block_reason}")

    print()

    # --- Test : bloquer une tâche correctement ---
    print("=== Test : blocage qui fonctionne ===")
    task = tasks[2]  # "Mettre à jour le schéma", pas encore bloquée
    task.set_blocked(True, "Décision en attente")
    print(f"  {task}")

    print()

    # --- Test : débloquer une tâche ---
    print("=== Test : déblocage ===")
    task.set_blocked(False)
    print(f"  {task}")

    print()

    # --- Test : bloquer sans raison (doit planter) ---
    print("=== Test : blocage sans raison → erreur prévue ===")
    try:
        task.set_blocked(True, "   ")  # juste des espaces → pas bon
    except ValueError as e:
        print(f"  Erreur attrapée : {e}")
