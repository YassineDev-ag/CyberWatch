from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Page d'accueil
@app.route("/")
def home():
    return render_template("index.html")

# Vérification du lien
@app.route("/check", methods=["POST"])
def check():
    url = request.form["url"]
    
    # Signes de danger simples
    signes_dangereux = [
        "free-money",
        "login-verify",
        "account-suspended",
        "click-here-now",
        "urgent-action",
        ".xyz",
        ".tk",
        ".ml",
        "bit.ly",
        "tinyurl"
    ]
    
    # Calcul du score de danger
    score = 0
    raisons = []
    
    for signe in signes_dangereux:
        if signe in url.lower():
            score += 1
            raisons.append(signe)
    
    # HTTPS ou non ?
    if not url.startswith("https"):
        score += 1
        raisons.append("Pas de HTTPS")
    
    # URL trop longue ?
    if len(url) > 100:
        score += 1
        raisons.append("URL très longue")
    
    # Résultat
    if score == 0:
        resultat = "✅ SÛR"
        couleur = "green"
        message = "Ce lien semble sûr"
    elif score <= 2:
        resultat = "⚠️ SUSPECT"
        couleur = "orange"
        message = "Ce lien est suspect, soyez prudent"
    else:
        resultat = "❌ DANGEREUX"
        couleur = "red"
        message = "Ce lien est probablement dangereux!"
    
    return render_template("index.html", 
                           result=resultat,
                           color=couleur,
                           message=message,
                           reasons=raisons,
                           url=url)

if __name__ == "__main__":
    app.run(debug=True)
