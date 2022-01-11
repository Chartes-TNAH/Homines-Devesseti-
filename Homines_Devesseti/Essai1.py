from flask import Flask, render_template

app = Flask("Homines Devesseti")

@app.route("/")
def accueil():
    return render_template("accueil.html", nom="Homines Devesseti")

@app.route("/places/<int:place_id>")
def chemin_place(place_id):
    return "On est sur " + str(place_id)

if __name__ == "__main__":
    app.run()