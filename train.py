import pandas as pd

# Load dataset
df = pd.read_csv("data.csv")

print("✅ Dataset Loaded Successfully!\n")
print(df.head())

# Select required columns
df = df[['User_ID', 'Product_ID', 'User_Rating']]

# Rename columns
df.columns = ['user_id', 'product_id', 'rating']

# Create matrix
user_matrix = df.pivot_table(index='user_id', columns='product_id', values='rating').fillna(0)

print("\n🔢 User-Product Matrix:")
print(user_matrix.head())

# Recommendation function
def recommend(user_id):
    if user_id not in user_matrix.index:
        return "❌ User not found"

    user_data = user_matrix.loc[user_id]
    return user_data.sort_values(ascending=False).head(5)

# Test
print("\n🎯 Recommendations for U0103:")
print(recommend('U0103'))