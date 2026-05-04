from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_csv("data.csv")

# Select required columns
df = df[['User_ID', 'Product_ID', 'User_Rating']]
df.columns = ['user_id', 'product_id', 'rating']

# Create matrix
user_matrix = df.pivot_table(index='user_id', columns='product_id', values='rating').fillna(0)

# API route
@app.route('/recommend/<user_id>')
def recommend(user_id):
    if user_id not in user_matrix.index:
        return jsonify({"error": "User not found"})

    user_data = user_matrix.loc[user_id]
    recs = user_data.sort_values(ascending=False).head(5)

    return jsonify(recs.to_dict())

# Run app
if __name__ == '__main__':
    app.run(debug=True)