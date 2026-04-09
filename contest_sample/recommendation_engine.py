"""
AI Recommendation Engine - Machine Learning based recommendations
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple

class RecommendationEngine:
    """AI-powered recommendation system using collaborative filtering"""

    def __init__(self, products_df: pd.DataFrame):
        self.products_df = products_df.copy()
        self.scaler = StandardScaler()

    def get_product_features(self) -> np.ndarray:
        """Extract and normalize numeric features from products"""
        numeric_cols = self.products_df.select_dtypes(include=[np.number]).columns
        features = self.products_df[numeric_cols].fillna(0)
        return self.scaler.fit_transform(features)

    def content_based_recommendation(self, product_id: int, top_n: int = 5) -> List[Dict]:
        """
        Recommend similar products based on content similarity
        """
        features = self.get_product_features()

        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(features)

        if product_id < 0 or product_id >= len(similarity_matrix):
            return []

        # Get similarities for the given product
        similarities = similarity_matrix[product_id]

        # Get indices of most similar products (excluding the product itself)
        similar_indices = np.argsort(similarities)[::-1][1:top_n + 1]

        recommendations = []
        for idx in similar_indices:
            product = self.products_df.iloc[idx]
            recommendations.append({
                'id': idx,
                'name': product.get('name', f'Product {idx}'),
                'similarity_score': float(similarities[idx]),
                'info': product.to_dict()
            })

        return recommendations

    def price_based_recommendation(self, budget: float, category: str = None, top_n: int = 5) -> List[Dict]:
        """
        Recommend products within budget and optionally by category
        """
        filtered_df = self.products_df.copy()

        # Filter by price
        if 'price' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['price'] <= budget]

        # Filter by category if provided
        if category and 'category' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['category'].str.lower() == category.lower()]

        # Sort by rating if available, else by price
        if 'rating' in filtered_df.columns:
            filtered_df = filtered_df.sort_values('rating', ascending=False)
        elif 'price' in filtered_df.columns:
            filtered_df = filtered_df.sort_values('price', ascending=True)

        recommendations = []
        for idx, (_, product) in enumerate(filtered_df.head(top_n).iterrows()):
            recommendations.append({
                'id': idx,
                'name': product.get('name', f'Product {idx}'),
                'price': product.get('price', 'N/A'),
                'category': product.get('category', 'N/A'),
                'rating': product.get('rating', 'N/A'),
                'info': product.to_dict()
            })

        return recommendations

    def rating_based_recommendation(self, min_rating: float = 4.0, top_n: int = 5) -> List[Dict]:
        """
        Recommend top-rated products
        """
        if 'rating' not in self.products_df.columns:
            return []

        filtered_df = self.products_df[self.products_df['rating'] >= min_rating]
        filtered_df = filtered_df.sort_values('rating', ascending=False)

        recommendations = []
        for idx, (_, product) in enumerate(filtered_df.head(top_n).iterrows()):
            recommendations.append({
                'id': idx,
                'name': product.get('name', f'Product {idx}'),
                'rating': product.get('rating', 'N/A'),
                'info': product.to_dict()
            })

        return recommendations

    def smart_recommendation(self, budget: float, preferred_rating: float = 3.0,
                           category: str = None, top_n: int = 5) -> Dict:
        """
        Combined smart recommendation using multiple strategies
        """
        recommendations = {
            'smart_picks': [],
            'budget_friendly': [],
            'highly_rated': [],
            'reason': []
        }

        # Budget friendly recommendations
        budget_recs = self.price_based_recommendation(budget, category, top_n)
        recommendations['budget_friendly'] = budget_recs

        # Highly rated recommendations
        rated_recs = self.rating_based_recommendation(preferred_rating, top_n)
        recommendations['highly_rated'] = rated_recs

        # Smart picks (intersection + scoring)
        smart_picks = []
        budget_names = {rec['name'] for rec in budget_recs}
        rated_names = {rec['name'] for rec in rated_recs}

        for rec in budget_recs:
            if rec['name'] in rated_names:
                smart_picks.append(rec)

        recommendations['smart_picks'] = smart_picks[:top_n]

        # Generate recommendations
        if smart_picks:
            recommendations['reason'] = f"Found {len(smart_picks)} products that are within your budget (₹{budget}) and highly rated!"
        elif budget_recs:
            recommendations['reason'] = f"Found {len(budget_recs)} affordable options. Consider increasing rating preference for more highly-rated items."
        else:
            recommendations['reason'] = "No products found matching your criteria. Try increasing your budget."

        return recommendations

    def get_product_stats(self) -> Dict:
        """Get statistics about products"""
        stats = {}
        numeric_cols = self.products_df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            stats[col] = {
                'mean': float(self.products_df[col].mean()),
                'median': float(self.products_df[col].median()),
                'std': float(self.products_df[col].std()),
                'min': float(self.products_df[col].min()),
                'max': float(self.products_df[col].max())
            }

        return stats
