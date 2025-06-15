from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

# load the model once at start-up
model = pickle.load(open("corolla_price_model.pkl", "rb"))

# (optional) hard-coded choices for the HTML drop-downs
COMPANIES   = ["Select Company", "Toyota"]          # expand if needed
DOOR_COUNTS = [3, 4, 5]
GEARS       = [4, 5, 6]

# ------------------------------------------------------
# 2 – Routes
# ------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    """
    HTML form for quick manual testing in a browser.
    """
    return render_template(
        "index.html",
        companies=COMPANIES,
        doors=DOOR_COUNTS,
        gears=GEARS
    )

@app.route("/predict", methods=["POST"])
def predict():
    """
    Accepts either:
      • a browser form submission (Content-Type: application/x-www-form-urlencoded)
      • or raw JSON { "Age_08_04": …, "KM": …, "HP": …, "Doors": …, "Gears": …, "Weight": … }
    Returns the estimated price in euro.
    """
    if request.is_json:                       # API call
        data = request.get_json(force=True)
    else:                                     # form submission
        data = request.form.to_dict()

    # coerce fields to numeric – raise KeyError if any are missing
    features = pd.DataFrame([[
        float(data["Age_08_04"]),
        float(data["KM"]),
        float(data["HP"]),
        float(data["Doors"]),
        float(data["Gears"]),
        float(data["Weight"])
    ]],
        columns=["Age_08_04", "KM", "HP", "Doors", "Gears", "Weight"]
    )

    # model expects the exact same column order used during training
    pred = model.predict(features)[0]

    # round to two decimals for readability
    return jsonify({"predicted_price": round(pred, 2)})

# ------------------------------------------------------
# 3 – Launch
# ------------------------------------------------------
if __name__ == "__main__":
    # debug=False for production; host='0.0.0.0' lets Docker expose the port
    app.run(host="0.0.0.0", port=5000, debug=True)
