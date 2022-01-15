from flask import Flask, render_template

app = Flask("Homines Devesseti")

hommes = {
    0: {
        "nom": "Garralis",
        "prenom": "Andrea",
        "localite": "Devesset",
        "fonction": "notaire",
        "date": "20 juin 1322"
    },
    1: {
        "nom": "Verilhati",
        "prenom": "Jean",
        "fonction": "curé",
        "date": "12 septembre 1323",
    }
}


@app.route("/")
def accueil():
    return render_template("pages/accueil.html", nom="Homines Devesseti", hommes=hommes)

@app.route("/name/<int:name_id>")
def nom(name_id):
    return render_template("pages/noms.html", nom="Homines Devesseti", homme=hommes[name_id])

# Petit tips final pour s'assurer que Python s'est pas perdu en chemin et exécute bien ce fichier
if __name__ == "__main__":
    app.run(debug=True)