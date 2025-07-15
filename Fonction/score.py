FILENAME = "scores.txt" # nom du fichier ou y'a le score
MAX_SCORES = 5 # nombre de score max save dans le fichier

def read_scores(filename=FILENAME):
    try:
        with open(filename, "r") as f:
            scores = [int(line.strip()) for line in f.readlines()]
        return scores
    except FileNotFoundError:
        return []

def save_scores(scores, filename=FILENAME):
    with open(filename, "w") as f:
        for score in scores:
            f.write(f"{score}\n")

def add_score(new_score, filename=FILENAME, max_scores=MAX_SCORES):
    scores = read_scores(filename)
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:max_scores]
    save_scores(scores)
    return scores

# --- Exemple d'utilisation ---
"""
score = int(input("Entre ton score : "))
top_scores = add_score(score)

print("\n🏆 Top 10 meilleurs scores :")
for i, s in enumerate(top_scores, 1):
    print(f"{i}. {s}")
"""