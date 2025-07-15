FILENAME = "scores.txt" # nom du fichier ou y'a le score
MAX_SCORES = 5 # nombre de score max save dans le fichier

def read_scores(filename=FILENAME):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            scores = []
            for line in f.readlines():
                line = line.strip()
                if line:
                    # Format: "pseudo:score" ou juste "score" pour la compatibilité
                    if ":" in line:
                        pseudo, score = line.split(":", 1)
                        scores.append((pseudo, int(score)))
                    else:
                        scores.append(("Anonyme", int(line)))
            return scores
    except FileNotFoundError:
        return []

def save_scores(scores, filename=FILENAME):
    with open(filename, "w", encoding="utf-8") as f:
        for pseudo, score in scores:
            f.write(f"{pseudo}:{score}\n")

def add_score(new_score, pseudo="Anonyme", filename=FILENAME, max_scores=MAX_SCORES):
    scores = read_scores(filename)
    scores.append((pseudo, new_score))
    # Trier par score décroissant
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:max_scores]
    save_scores(scores, filename)
    return scores

# --- Exemple d'utilisation ---
"""
pseudo = input("Entre ton pseudo : ")
score = int(input("Entre ton score : "))
top_scores = add_score(score, pseudo)

print("\n🏆 Top 5 meilleurs scores :")
for i, (pseudo, s) in enumerate(top_scores, 1):
    print(f"{i}. {pseudo}: {s}")
"""