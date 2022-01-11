from flask import Flask, render_template

app = Flask("Homines Devesseti")

@app.route("/")
@app.route("/exemple/<exemple>")
def accueil(exemple=None):
    lieux = ["Devesset", "Saint-Agrève"]
    if exemple:
        lieux = ["Col. Lugdunum", "Augustomagus"]
    return render_template("accueil.html", nom="Gazetteer", lieux=lieux)

if __name__ == "__main__":
    app.run()