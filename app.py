from flask import Flask, request, render_template, jsonify
import pandas as pd

# Create app
app = Flask(__name__)

# Load dataset
df = pd.read_csv("data.csv")
df = df[['User_ID','Product_ID','User_Rating']]
df.columns = ['user_id','product_id','rating']

# Create user-product matrix
user_matrix = df.pivot_table(index='user_id', columns='product_id', values='rating').fillna(0)

# 🔹 Function to get recommendations
def get_recommendations(user_id):
    if user_id in user_matrix.index:
        # Personalized recommendations
        return (
            user_matrix.loc[user_id]
            .sort_values(ascending=False)
            .head(5)
            .to_dict()
        )
    else:
        # Fallback → popular products
        return (
            df.groupby('product_id')['rating']
            .mean()
            .sort_values(ascending=False)
            .head(5)
            .to_dict()
        )

# 🔹 UI Route
@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = None

    if request.method == 'POST':
        user_id = request.form['user_id']
        recommendations = get_recommendations(user_id)

    return render_template('index.html', recommendations=recommendations)

# 🔹 API Route (IMPORTANT for demo)
@app.route('/recommend/<user_id>')
def recommend(user_id):
    recommendations = get_recommendations(user_id)
    return jsonify(recommendations)

# Run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)