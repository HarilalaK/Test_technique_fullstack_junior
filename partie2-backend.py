# Partie 2 – Backend (Python)

## Classe Task et fonctions associées


class Tache:
    def __init__(self, nom_tache, nom_projet, niveau_priorite, est_bloquee=False, raison_blocage=None):
        self.nom_tache = nom_tache
        self.nom_projet = nom_projet
        self.niveau_priorite = niveau_priorite  # 1 = haute, 2 = moyenne, 3 = basse
        self.est_bloquee = est_bloquee
        self.raison_blocage = raison_blocage

    def definir_blocage(self, est_bloquee: bool, raison_blocage: str = None):
        """
        Change le statut de blocage d'une tâche.
        
        Règle simple : si on bloque la tâche, il faut obligatoirement une raison.
        La raison ne peut pas être vide ou juste des espaces.
        
        Lève une erreur si la règle n'est pas respectée.
        """
        if est_bloquee:
            if not raison_blocage or not raison_blocage.strip():
                raise ValueError(
                    "Il faut donner une raison quand on bloque une tâche."
                )

        self.est_bloquee = est_bloquee
        self.raison_blocage = raison_blocage.strip() if raison_blocage else None

    def __repr__(self):
        return (
            f"Tache(nom_tache={self.nom_tache!r}, nom_projet={self.nom_projet!r}, "
            f"niveau_priorite={self.niveau_priorite}, est_bloquee={self.est_bloquee}, "
            f"raison_blocage={self.raison_blocage!r})"
        )


# --------------------------------------------------------
# 1. Fonction pour trouver et trier les tâches bloquées
# -------------------------------------------------------

def obtenir_taches_bloquees(liste_taches: list[Tache]) -> list[Tache]:
    """
    Renvoie uniquement les tâches bloquées, triées par :
    - Priorité croissante (1 avant 2 avant 3)
    - Ordre alphabétique du nom de tâche
    """
    taches_bloquees = [tache for tache in liste_taches if tache.est_bloquee]
    taches_bloquees.sort(key=lambda tache: (tache.niveau_priorite, tache.nom_tache))
    return taches_bloquees


# -----------------------------
# Exemples pour tester le code
# -----------------------------

if __name__ == "__main__":

    # --- Création de quelques tâches ---
    liste_taches = [
        Tache("Configurer le serveur",        "Client A", niveau_priorite=1, est_bloquee=True,  raison_blocage="En attente des accès"),
        Tache("Rédiger la documentation",     "Interne",  niveau_priorite=3, est_bloquee=True,  raison_blocage="Manque d'informations"),
        Tache("Mettre à jour le schéma",      "Client B", niveau_priorite=2, est_bloquee=False),
        Tache("Déployer en production",       "Client A", niveau_priorite=1, est_bloquee=True,  raison_blocage="Tests non validés"),
        Tache("Analyser les besoins",         "Client C", niveau_priorite=2, est_bloquee=True,  raison_blocage="Réunion annulée"),
        Tache("Corriger le bug d'affichage",  "Interne",  niveau_priorite=1, est_bloquee=False),
    ]

    # --- Test de la fonction obtenir_taches_bloquees ---
    print("=== Tâches bloquées (bien triées) ===")
    for tache_actuelle in obtenir_taches_bloquees(liste_taches):
        print(f"  [{tache_actuelle.niveau_priorite}] {tache_actuelle.nom_tache!r} — {tache_actuelle.raison_blocage}")

    print()

    # --- Test : bloquer une tâche correctement ---
    print("=== Test : blocage qui fonctionne ===")
    tache_test = liste_taches[2]  # "Mettre à jour le schéma", pas encore bloquée
    tache_test.definir_blocage(True, "Décision en attente")
    print(f"  {tache_test}")

    print()

    # --- Test : débloquer une tâche ---
    print("=== Test : déblocage ===")
    tache_test.definir_blocage(False)
    print(f"  {tache_test}")

    print()

    # --- Test : bloquer sans raison (doit planter) ---
    print("=== Test : blocage sans raison → erreur prévue ===")
    try:
        tache_test.definir_blocage(True, "   ")  # juste des espaces → pas bon
    except ValueError as erreur:
        print(f"  Erreur attrapée : {erreur}")
