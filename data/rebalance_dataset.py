"""
Rebalance the dataset to create more realistic, non-perfect distributions
"""

import pandas as pd
import numpy as np

# Load the enhanced dataset
df = pd.read_csv('enhanced_reviews_dataset.csv')

print(f"Original dataset size: {len(df)}")
print(f"Original fake reviews: {len(df[df['label']=='CG'])}")
print(f"Original genuine reviews: {len(df[df['label']=='OR'])}")

# Set random seed for reproducibility
np.random.seed(42)

# Define realistic fake rates per category with HIGH VARIATION
# Some categories are heavily targeted, others are trusted
category_fake_rates = {
    'Home_and_Kitchen_5': 0.28,      # Low - trusted, established sellers
    'Electronics_5': 0.67,            # Very High - competitive, high-value items
    'Books_5': 0.18,                 # Very Low - Amazon reviews, established publishers
    'Clothing_Shoes_and_Jewelry_5': 0.58,  # High - fashion/trendy items, new sellers
    'Toys_and_Games_5': 0.72,        # Highest - seasonal, gift items heavily targeted
    'Sports_and_Outdoors_5': 0.35,   # Medium-Low - niche community
    'Pet_Supplies_5': 0.23,          # Low - pet owners are loyal, careful buyers
    'Kindle_Store_5': 0.15,          # Very Low - verified purchases, digital goods
    'Tools_and_Home_Improvement_5': 0.42,  # Medium - professional buyers check specs
    'Movies_and_TV_5': 0.52,         # Medium-High - entertainment, subjective
}

# Get unique categories
categories = df['category'].unique()

# Define category sizes (some categories have more reviews than others - more natural)
category_sizes = {
    'Electronics_5': 1.2,        # Popular category - more reviews
    'Books_5': 1.3,              # Very popular - most reviews
    'Clothing_Shoes_and_Jewelry_5': 1.15,  # Popular
    'Home_and_Kitchen_5': 1.1,   # Popular
    'Toys_and_Games_5': 0.85,    # Seasonal - fewer reviews
    'Movies_and_TV_5': 0.95,     # Medium
    'Sports_and_Outdoors_5': 0.75, # Niche - fewer reviews
    'Pet_Supplies_5': 0.70,      # Smaller market
    'Kindle_Store_5': 1.05,      # Digital - decent size
    'Tools_and_Home_Improvement_5': 0.80,  # Smaller niche
}

# Create new balanced dataset
new_rows = []

for category in categories:
    cat_df = df[df['category'] == category].copy()
    
    # Get target fake rate for this category
    # If category not in our mapping, use a random rate between 25-60%
    if category in category_fake_rates:
        target_fake_rate = category_fake_rates[category]
    else:
        target_fake_rate = np.random.uniform(0.25, 0.60)
    
    # Apply size multiplier to create varied category sizes
    size_multiplier = category_sizes.get(category, 1.0)
    
    print(f"\n{category}:")
    print(f"  Target fake rate = {target_fake_rate:.1%}")
    print(f"  Size multiplier = {size_multiplier:.2f}x")
    
    # Separate fake and genuine
    fake_reviews = cat_df[cat_df['label'] == 'CG'].copy()
    genuine_reviews = cat_df[cat_df['label'] == 'OR'].copy()
    
    # Apply size multiplier to total
    total_reviews = int(len(cat_df) * size_multiplier)
    target_fake_count = int(total_reviews * target_fake_rate)
    target_genuine_count = total_reviews - target_fake_count
    
    # Sample to get desired distribution (with replacement if needed)
    if len(fake_reviews) >= target_fake_count:
        fake_sample = fake_reviews.sample(n=target_fake_count, random_state=42)
    else:
        # Need more samples - sample with replacement
        fake_sample = fake_reviews.sample(n=target_fake_count, replace=True, random_state=42)
    
    if len(genuine_reviews) >= target_genuine_count:
        genuine_sample = genuine_reviews.sample(n=target_genuine_count, random_state=42)
    else:
        # Need more samples - sample with replacement
        genuine_sample = genuine_reviews.sample(n=target_genuine_count, replace=True, random_state=42)
    
    # Combine
    category_sample = pd.concat([fake_sample, genuine_sample])
    
    print(f"  Fake: {len(fake_sample)} ({len(fake_sample)/len(category_sample)*100:.1f}%)")
    print(f"  Genuine: {len(genuine_sample)} ({len(genuine_sample)/len(category_sample)*100:.1f}%)")
    
    new_rows.append(category_sample)

# Combine all categories
new_df = pd.concat(new_rows, ignore_index=True)

# Shuffle the dataset
new_df = new_df.sample(frac=1, random_state=42).reset_index(drop=True)

print("\n" + "="*60)
print("NEW DATASET STATISTICS")
print("="*60)
print(f"Total reviews: {len(new_df)}")
print(f"Fake reviews (CG): {len(new_df[new_df['label']=='CG'])} ({len(new_df[new_df['label']=='CG'])/len(new_df)*100:.1f}%)")
print(f"Genuine reviews (OR): {len(new_df[new_df['label']=='OR'])} ({len(new_df[new_df['label']=='OR'])/len(new_df)*100:.1f}%)")

# Save the rebalanced dataset
new_df.to_csv('enhanced_reviews_dataset.csv', index=False)
print("\n✅ Rebalanced dataset saved to 'enhanced_reviews_dataset.csv'")

# Show per-category breakdown
print("\n" + "="*60)
print("PER-CATEGORY BREAKDOWN")
print("="*60)
for category in new_df['category'].unique():
    cat_data = new_df[new_df['category'] == category]
    fake_count = len(cat_data[cat_data['label'] == 'CG'])
    total = len(cat_data)
    fake_rate = fake_count / total * 100 if total > 0 else 0
    print(f"{category:30} Total: {total:5} Fake: {fake_count:5} ({fake_rate:5.1f}%)")

