AutoPrice – AI-Powered Toyota Corolla Resale Valuation Engine
A lightweight machine-learning service that delivers instant, objective price quotes for used Toyota Corolla cars.
AutoPrice ingests six easily measurable vehicle attributes, feeds them through a transparent regression model, and returns a fair-market estimate via a REST endpoint hosted on Vercel.

Table of Contents
Overview

Problem & Goals

How it Works

Tech Stack

Dataset

Training & Tuning

API Reference

Quick Start

Project Structure

Contributing

License

Overview
Manual pricing of second-hand cars is slow and subjective. AutoPrice replaces gut-feel with data-driven valuation, helping dealers and private sellers negotiate faster and more confidently.

Problem & Goals
Inconsistent valuations create mistrust and lost sales.

Need a fast, explainable model that runs on commodity hardware and integrates with any frontend.

AutoPrice delivers:

≤ 1 s latency per prediction

~€1 350 RMSE (≈ 14 % of median price)

Fully open-source code, data and model so results can be audited and improved.

How it Works
A client sends a JSON payload with six numeric features (Age_08_04, KM, HP, Doors, Gears, Weight) to the /api/predict route.

The Flask server loads a pickled Multiple Linear Regression model and returns {"predicted_price": <float>}.

Vercel’s serverless runtime auto-scales the endpoint worldwide; cold-starts are < 1 s.

Tech Stack
Python 3.11

scikit-learn 1.5 for model fitting

Optuna for hyper-parameter sweeps

Docker (local) → Vercel Serverless Functions (prod)

Flask 3.0 REST micro-framework

GitHub Actions CI/CD

Dataset
Open “Toyota Corolla” CSV (1 436 rows, 10 columns).
Pre-processing: drop Cylinders (100 % NaN) and keep six numeric predictors that show the strongest correlation with price.

Training & Tuning
Baseline: Multiple Linear Regression

Alternative: Random-Forest benchmark (RMSE ≈ €1 100)

Cross-validation: 5-fold, mean R² ≈ 0.84

Optuna grid explored polynomial features & elastic-net penalties; no improvement on hold-out, so kept plain OLS for transparency.

The final estimator is stored as corolla_price_model.pkl.

API Reference
Endpoint	Method	Body fields	Response
/api/predict	POST	JSON with the six numeric features	{"predicted_price": 12345.67}
Example call:

bash
curl -X POST https://<your-vercel-domain>/api/predict \
     -H "Content-Type: application/json" \
     -d '{"Age_08_04":36,"KM":42000,"HP":90,"Doors":5,"Gears":5,"Weight":1100}'
Quick Start
bash
# clone & install
git clone https://github.com/your-handle/AutoPrice.git
cd AutoPrice
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# run locally
python app.py         # listens on http://127.0.0.1:5000
Deploy to Vercel:

bash
npm i -g vercel
vercel deploy          # picks up vercel.json and builds the Flask function
Project Structure
text
AutoPrice/
│
├─ data/                     # raw ToyotaCorolla.csv
├─ notebooks/                # EDA & model development
├─ app.py                    # Flask entry-point
├─ corolla_price_model.pkl   # trained model
├─ api/                      # Vercel serverless function
├─ Dockerfile                # optional local container
├─ requirements.txt
└─ tests/
Contributing
Pull requests are welcome! Please open an issue first to discuss major changes.
