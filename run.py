from Homines_Devesseti.app import config_app

if __name__ == "__main__":
    app = config_app("production")
    app.run(debug=True)