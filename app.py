from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_csv("data.csv")
df = df[['User_ID', 'Product_ID', 'User_Rating']]
df.columns = ['user_id', 'product_id', 'rating']

# Create matrix
user_matrix = df.pivot_table(index='user_id', columns='product_id', values='rating').fillna(0)

# ✅ AUTO-GENERATE customer names
import random

# Real-looking names list
name_list = [
    "Rahul", "Priya", "Ananya", "Rohit", "Kiran",
    "Sneha", "Arjun", "Meena", "Vikram", "Pooja"
]

# Assign random names to users
user_names = {
    uid: random.choice(name_list) for uid in user_matrix.index
}

# Product names mapping
product_names = {
    "P0004": "Laptop",
    "P0018": "Mobile Phone",
    "P0039": "Headphones",
    "P0049": "Smart Watch",
    "P0086": "Bluetooth Speaker"
}

# Recommendation logic
def get_recommendations(user_id):
    if user_id in user_matrix.index:
        rec_dict = (
            user_matrix.loc[user_id]
            .sort_values(ascending=False)
            .head(5)
            .to_dict()
        )
    else:
        rec_dict = (
            df.groupby('product_id')['rating']
            .mean()
            .sort_values(ascending=False)
            .head(5)
            .to_dict()
        )

    rec_named = {
        product_names.get(k, k): v for k, v in rec_dict.items()
    }

    return rec_named

# UI route
@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = None
    customer_name = None

    if request.method == 'POST':
        user_id = request.form['user_id']

        recommendations = get_recommendations(user_id)
        customer_name = user_names.get(user_id, f"Customer {user_id}")

    return render_template(
        'index.html',
        recommendations=recommendations,
        customer_name=customer_name
    )

# API route
@app.route('/recommend/<user_id>')
def recommend(user_id):
    recommendations = get_recommendations(user_id)
    return jsonify(recommendations)

# Run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)