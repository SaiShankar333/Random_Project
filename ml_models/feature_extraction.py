"""
Feature Extraction Module for Fake Review Detection
Extracts NLP and metadata features from reviews
"""

import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class ReviewFeatureExtractor:
    """Extract features from review text and metadata"""
    
    def __init__(self, max_tfidf_features=100):
        self.max_tfidf_features = max_tfidf_features
        self.tfidf_vectorizer = None
        self.scaler = None
        self.stop_words = set(stopwords.words('english'))
        
    def preprocess_text(self, text):
        """Clean and preprocess review text"""
        if pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s!?.,]', '', text)
        
        return text.strip()
    
    def extract_text_statistics(self, text):
        """Extract statistical features from text"""
        if pd.isna(text) or text == "":
            return {
                'review_length': 0,
                'word_count': 0,
                'avg_word_length': 0,
                'sentence_count': 0,
                'exclamation_count': 0,
                'question_count': 0,
                'caps_ratio': 0,
                'unique_word_ratio': 0
            }
        
        text_str = str(text)
        
        # Basic statistics
        review_length = len(text_str)
        words = word_tokenize(text_str.lower())
        word_count = len(words)
        
        # Average word length
        avg_word_length = np.mean([len(word) for word in words]) if words else 0
        
        # Sentence count
        sentences = sent_tokenize(text_str)
        sentence_count = len(sentences)
        
        # Punctuation counts
        exclamation_count = text_str.count('!')
        question_count = text_str.count('?')
        
        # Capital letters ratio
        caps_count = sum(1 for c in text_str if c.isupper())
        caps_ratio = caps_count / len(text_str) if len(text_str) > 0 else 0
        
        # Unique word ratio (lexical diversity)
        unique_words = set(words)
        unique_word_ratio = len(unique_words) / word_count if word_count > 0 else 0
        
        return {
            'review_length': review_length,
            'word_count': word_count,
            'avg_word_length': avg_word_length,
            'sentence_count': sentence_count,
            'exclamation_count': exclamation_count,
            'question_count': question_count,
            'caps_ratio': caps_ratio,
            'unique_word_ratio': unique_word_ratio
        }
    
    def extract_metadata_features(self, row):
        """Extract features from metadata columns"""
        features = {}
        
        # Verified purchase (already boolean, convert to int)
        features['verified_purchase'] = int(row.get('verified_purchase', False))
        
        # Missing IDs (derive from data)
        features['order_id_missing'] = int(pd.isna(row.get('order_id', None)))
        features['purchase_id_missing'] = int(pd.isna(row.get('purchase_id', None)))
        
        # Days after purchase
        days = row.get('days_after_purchase', 0)
        features['days_after_purchase'] = days
        features['negative_days'] = int(days < 0)
        features['very_late_review'] = int(days > 365)
        
        # User review count
        review_count = row.get('user_review_count', 0)
        features['user_review_count'] = review_count
        features['high_review_count'] = int(review_count > 50)
        
        # Rating
        features['rating'] = row.get('rating', 3.0)
        features['extreme_rating'] = int(row.get('rating', 3.0) in [1.0, 5.0])
        
        return features
    
    def extract_all_features(self, df):
        """Extract all features from dataframe"""
        print("Extracting text statistics...")
        text_stats_list = []
        for text in df['text_']:
            cleaned_text = self.preprocess_text(text)
            stats = self.extract_text_statistics(cleaned_text)
            text_stats_list.append(stats)
        
        text_stats_df = pd.DataFrame(text_stats_list)
        
        print("Extracting metadata features...")
        metadata_list = []
        for _, row in df.iterrows():
            meta_features = self.extract_metadata_features(row)
            metadata_list.append(meta_features)
        
        metadata_df = pd.DataFrame(metadata_list)
        
        # Combine all features
        combined_features = pd.concat([text_stats_df, metadata_df], axis=1)
        
        return combined_features
    
    def fit_tfidf(self, texts):
        """Fit TF-IDF vectorizer on texts"""
        print("Fitting TF-IDF vectorizer...")
        cleaned_texts = [self.preprocess_text(text) for text in texts]
        
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=self.max_tfidf_features,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=5,
            max_df=0.8
        )
        
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(cleaned_texts)
        return tfidf_matrix
    
    def transform_tfidf(self, texts):
        """Transform texts using fitted TF-IDF vectorizer"""
        if self.tfidf_vectorizer is None:
            raise ValueError("TF-IDF vectorizer not fitted. Call fit_tfidf first.")
        
        cleaned_texts = [self.preprocess_text(text) for text in texts]
        return self.tfidf_vectorizer.transform(cleaned_texts)
    
    def fit_scaler(self, features):
        """Fit scaler on numerical features"""
        print("Fitting feature scaler...")
        self.scaler = StandardScaler()
        scaled_features = self.scaler.fit_transform(features)
        return scaled_features
    
    def transform_scaler(self, features):
        """Transform features using fitted scaler"""
        if self.scaler is None:
            raise ValueError("Scaler not fitted. Call fit_scaler first.")
        
        return self.scaler.transform(features)


def prepare_features(df, extractor, is_training=True):
    """
    Prepare complete feature set for ML model
    
    Args:
        df: DataFrame with reviews
        extractor: ReviewFeatureExtractor instance
        is_training: If True, fit extractors; if False, only transform
    
    Returns:
        Combined feature matrix
    """
    # Extract text and metadata features
    statistical_features = extractor.extract_all_features(df)
    
    # TF-IDF features
    if is_training:
        tfidf_features = extractor.fit_tfidf(df['text_'])
        scaled_features = extractor.fit_scaler(statistical_features)
    else:
        tfidf_features = extractor.transform_tfidf(df['text_'])
        scaled_features = extractor.transform_scaler(statistical_features)
    
    # Convert TF-IDF sparse matrix to dense
    tfidf_dense = tfidf_features.toarray()
    
    # Combine all features
    final_features = np.hstack([scaled_features, tfidf_dense])
    
    print(f"Final feature matrix shape: {final_features.shape}")
    
    return final_features, statistical_features.columns.tolist()


if __name__ == "__main__":
    # Test the feature extractor
    print("Testing Feature Extraction...")
    
    # Load sample data
    df = pd.read_csv('../data/enhanced_reviews_dataset.csv')
    print(f"Loaded {len(df)} reviews")
    
    # Create extractor
    extractor = ReviewFeatureExtractor(max_tfidf_features=100)
    
    # Extract features from first 1000 reviews (for testing)
    sample_df = df.head(1000)
    features, feature_names = prepare_features(sample_df, extractor, is_training=True)
    
    print(f"\nExtracted {features.shape[1]} features from {features.shape[0]} reviews")
    print(f"Statistical features: {len(feature_names)}")
    print(f"TF-IDF features: {extractor.max_tfidf_features}")
    print("\nFeature extraction test completed successfully!")

