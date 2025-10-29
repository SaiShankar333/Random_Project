"""
Model Training Script for Fake Review Detection
Trains Random Forest classifier and evaluates performance
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import joblib
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from feature_extraction import ReviewFeatureExtractor, prepare_features


class FakeReviewDetector:
    """Complete ML pipeline for fake review detection"""
    
    def __init__(self, model_type='random_forest'):
        self.model_type = model_type
        self.model = None
        self.feature_extractor = ReviewFeatureExtractor(max_tfidf_features=30)  # Reduced to 30
        self.feature_names = None
        self.metrics = {}
        
    def create_model(self):
        """Initialize the ML model"""
        if self.model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=25,        # Even fewer trees
                max_depth=8,            # Shallow trees
                min_samples_split=40,   # More samples required
                min_samples_leaf=20,    # More samples in leaves
                max_features=0.5,       # Use only 50% of features
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == 'logistic_regression':
            self.model = LogisticRegression(
                random_state=42,
                max_iter=1000
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        print(f"Initialized {self.model_type} model")
    
    def train(self, X_train, y_train):
        """Train the model"""
        print(f"\nTraining {self.model_type}...")
        print(f"Training samples: {len(X_train)}")
        print(f"Features: {X_train.shape[1]}")
        
        self.model.fit(X_train, y_train)
        print("Training completed!")
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        print("\nEvaluating model...")
        
        # Predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        self.metrics['confusion_matrix'] = cm.tolist()
        self.metrics['true_negatives'] = int(cm[0, 0])
        self.metrics['false_positives'] = int(cm[0, 1])
        self.metrics['false_negatives'] = int(cm[1, 0])
        self.metrics['true_positives'] = int(cm[1, 1])
        
        # Classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        self.metrics['classification_report'] = report
        
        # Feature importance (for tree-based models)
        if hasattr(self.model, 'feature_importances_'):
            self.metrics['feature_importance'] = self.model.feature_importances_.tolist()
        
        return self.metrics
    
    def print_metrics(self):
        """Print evaluation metrics"""
        print("\n" + "="*60)
        print("MODEL PERFORMANCE METRICS")
        print("="*60)
        
        print(f"\nAccuracy:  {self.metrics['accuracy']:.4f}")
        print(f"Precision: {self.metrics['precision']:.4f}")
        print(f"Recall:    {self.metrics['recall']:.4f}")
        print(f"F1-Score:  {self.metrics['f1_score']:.4f}")
        print(f"ROC-AUC:   {self.metrics['roc_auc']:.4f}")
        
        print("\nConfusion Matrix:")
        print(f"  True Negatives:  {self.metrics['true_negatives']}")
        print(f"  False Positives: {self.metrics['false_positives']}")
        print(f"  False Negatives: {self.metrics['false_negatives']}")
        print(f"  True Positives:  {self.metrics['true_positives']}")
        
        print("\nClassification Report:")
        report = self.metrics['classification_report']
        print(f"  Genuine Reviews (0): Precision={report['0']['precision']:.3f}, Recall={report['0']['recall']:.3f}")
        print(f"  Fake Reviews (1):    Precision={report['1']['precision']:.3f}, Recall={report['1']['recall']:.3f}")
        
        print("="*60)
    
    def save_model(self, save_dir='saved_models'):
        """Save trained model and components"""
        import os
        os.makedirs(save_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save model
        model_path = f"{save_dir}/random_forest_model.pkl"
        joblib.dump(self.model, model_path)
        print(f"Model saved: {model_path}")
        
        # Save feature extractor (contains TF-IDF and scaler)
        extractor_path = f"{save_dir}/feature_extractor.pkl"
        joblib.dump(self.feature_extractor, extractor_path)
        print(f"Feature extractor saved: {extractor_path}")
        
        # Save metrics
        metrics_path = f"{save_dir}/model_metrics.json"
        metrics_to_save = {k: v for k, v in self.metrics.items() 
                          if not isinstance(v, (np.ndarray, dict))}
        metrics_to_save['timestamp'] = timestamp
        metrics_to_save['model_type'] = self.model_type
        
        with open(metrics_path, 'w') as f:
            json.dump(metrics_to_save, f, indent=4)
        print(f"Metrics saved: {metrics_path}")
        
        # Save full metrics with report
        full_metrics_path = f"{save_dir}/full_metrics.json"
        with open(full_metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=4, default=str)
        print(f"Full metrics saved: {full_metrics_path}")
    
    @staticmethod
    def load_model(save_dir='saved_models'):
        """Load trained model and components"""
        model = joblib.load(f"{save_dir}/random_forest_model.pkl")
        feature_extractor = joblib.load(f"{save_dir}/feature_extractor.pkl")
        
        with open(f"{save_dir}/model_metrics.json", 'r') as f:
            metrics = json.load(f)
        
        detector = FakeReviewDetector()
        detector.model = model
        detector.feature_extractor = feature_extractor
        detector.metrics = metrics
        
        print("Model loaded successfully!")
        return detector
    
    def predict(self, review_data):
        """
        Predict if a review is fake
        
        Args:
            review_data: dict with keys: text_, order_id, purchase_id, 
                        verified_purchase, user_id, days_after_purchase, 
                        user_review_count, rating
        
        Returns:
            dict with prediction, confidence, and details
        """
        # Convert to DataFrame
        df = pd.DataFrame([review_data])
        
        # Extract features
        features, _ = prepare_features(df, self.feature_extractor, is_training=False)
        
        # Predict
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        return {
            'prediction': 'FAKE' if prediction == 1 else 'GENUINE',
            'confidence': float(max(probabilities)),
            'fake_probability': float(probabilities[1]),
            'genuine_probability': float(probabilities[0])
        }


def main():
    """Main training pipeline"""
    
    print("="*60)
    print("FAKE REVIEW DETECTION - MODEL TRAINING")
    print("="*60)
    
    # Load data
    print("\nLoading dataset...")
    df = pd.read_csv('../data/enhanced_reviews_dataset.csv')
    print(f"Loaded {len(df)} reviews")
    print(f"Fake reviews (CG): {len(df[df['label']=='CG'])}")
    print(f"Genuine reviews (OR): {len(df[df['label']=='OR'])}")
    
    # Prepare labels
    df['label_binary'] = (df['label'] == 'CG').astype(int)
    
    # Split data - using 70/30 split for more realistic results
    print("\nSplitting data (70% train, 30% test)...")
    train_df, test_df = train_test_split(
        df, 
        test_size=0.3,      # Increased from 0.2 for more challenging test
        random_state=42, 
        stratify=df['label_binary']
    )
    
    print(f"Training set: {len(train_df)} reviews")
    print(f"Test set: {len(test_df)} reviews")
    
    # Initialize detector
    detector = FakeReviewDetector(model_type='random_forest')
    detector.create_model()
    
    # Extract features
    print("\nExtracting features from training data...")
    X_train, feature_names = prepare_features(
        train_df, 
        detector.feature_extractor, 
        is_training=True
    )
    y_train = train_df['label_binary'].values
    
    print("\nExtracting features from test data...")
    X_test, _ = prepare_features(
        test_df, 
        detector.feature_extractor, 
        is_training=False
    )
    y_test = test_df['label_binary'].values
    
    # Train model
    detector.train(X_train, y_train)
    
    # Evaluate model
    detector.evaluate(X_test, y_test)
    detector.print_metrics()
    
    # Save model
    print("\nSaving model...")
    detector.save_model()
    
    # Test prediction
    print("\n" + "="*60)
    print("TESTING PREDICTION")
    print("="*60)
    
    sample_review = {
        'text_': "This product is amazing! Best purchase ever!",
        'order_id': None,
        'purchase_id': 'PUR-ABC123',
        'verified_purchase': False,
        'user_id': 'USER-12345',
        'days_after_purchase': -5,
        'user_review_count': 150,
        'rating': 5.0,
        'category': 'Home_and_Kitchen_5'
    }
    
    result = detector.predict(sample_review)
    print(f"\nSample Review: {sample_review['text_']}")
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Fake Probability: {result['fake_probability']:.2%}")
    
    print("\n" + "="*60)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)


if __name__ == "__main__":
    main()

