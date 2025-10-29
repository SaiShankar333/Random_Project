# Fake Review Detection System

An AI-powered full-stack application for detecting fake product reviews using machine learning and natural language processing.

## Project Overview

This system combines metadata verification with advanced NLP techniques to identify fraudulent product reviews with high accuracy. Built with a modern tech stack featuring React, Flask, and scikit-learn.

### Key Features

- **AI-Powered Detection**: Random Forest classifier trained on 40,000+ reviews
- **Real-time Analysis**: Instant predictions with confidence scores
- **Bulk Processing**: Upload CSV files to analyze multiple reviews
- **Comprehensive Analytics**: Interactive dashboards with visualizations
- **6 Core Verification Metrics**: Order ID, Purchase ID, Verified Purchase, User ID, Timing, and User Behavior
- **NLP Analysis**: 48 features including TF-IDF, text statistics, and linguistic patterns
- **Fluid UI Design**: Modern, organic interface with smooth animations

### Performance Metrics

- Accuracy: 93.50%
- Precision: 94.20%
- Recall: 91.80%
- F1-Score: 92.99%
- ROC-AUC: 0.9812

## Tech Stack

### Backend
- Python 3.8+
- Flask (REST API)
- scikit-learn (Machine Learning)
- NLTK (NLP preprocessing)
- pandas & numpy (Data processing)

### Frontend
- React 18
- Vite (Build tool)
- Tailwind CSS (Styling)
- Framer Motion (Animations)
- Recharts (Data visualization)
- Lucide React (Icons)

### ML Pipeline
- Random Forest Classifier
- TF-IDF Vectorization
- Feature Engineering
- Text Preprocessing

## Project Structure

```
Shivani's Project/
├── data/
│   ├── fake reviews dataset.csv (original)
│   └── enhanced_reviews_dataset.csv (with 6 metrics)
│
├── ml_models/
│   ├── feature_extraction.py
│   ├── train_model.py
│   ├── model_utils.py
│   └── saved_models/
│       ├── random_forest_model.pkl
│       ├── feature_extractor.pkl
│       └── model_metrics.json
│
├── backend/
│   ├── app.py (Flask application)
│   ├── config.py
│   ├── routes/
│   │   ├── predict.py (Single/batch predictions)
│   │   ├── analytics.py (Dashboard data)
│   │   └── bulk.py (File upload processing)
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Dashboard.jsx (Landing Page)
    │   │   ├── Detector.jsx
    │   │   ├── BulkAnalysis.jsx
    │   │   └── Performance.jsx
    │   ├── components/
    │   │   ├── Layout/ (Navbar, Footer)
    │   │   └── UI/ (GlassCard, BlobBackground, WaveDivider)
    │   ├── services/api.js
    │   └── App.jsx
    ├── package.json
    └── vite.config.js
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Step 1: Clone the Project

```bash
cd "/Users/saishankars/Desktop/SIP II/Shivani's Project"
```

### Step 2: Setup Backend

```bash
# Install Python dependencies
pip3 install Flask flask-cors pandas numpy scikit-learn nltk joblib

# Train the ML model (if not already trained)
cd ml_models
python3 train_model.py
cd ..
```

### Step 3: Setup Frontend

```bash
cd frontend

# Install Node.js dependencies
npm install

# This will install:
# - react & react-dom
# - react-router-dom
# - axios
# - framer-motion
# - recharts
# - lucide-react
# - tailwindcss
# - vite
```

## Running the Application

### Terminal 1: Start Backend Server

```bash
cd backend
python3 app.py
```

The Flask API will start on: `http://localhost:5000`

### Terminal 2: Start Frontend Development Server

```bash
cd frontend
npm run dev
```

The React app will start on: `http://localhost:5173`

### Access the Application

Open your browser and navigate to: **http://localhost:5173**

## Usage Guide

### 1. Dashboard (Landing Page)
- View analytics and statistics
- Review distribution charts
- Category analysis
- Model performance overview
- Interactive data tables

### 2. Review Detector
- Analyze single reviews
- Input review text and metadata
- Get instant predictions with confidence scores
- View detailed risk factors
- Load example reviews (fake or genuine)

### 3. Bulk Analysis
- Upload CSV/XLSX files
- Process multiple reviews at once
- Download template for proper format
- View summary statistics
- Download results with predictions

### 4. Performance
- Detailed model metrics
- Confusion matrix
- Classification report
- ROC-AUC score

## API Endpoints

### Prediction
- `POST /api/predict` - Analyze single review
- `POST /api/predict/batch` - Analyze multiple reviews

### Analytics
- `GET /api/analytics/summary` - Overall statistics
- `GET /api/analytics/category` - Category breakdown
- `GET /api/analytics/timing` - Timing analysis
- `GET /api/analytics/reviews` - Paginated review list
- `GET /api/analytics/model-performance` - Model metrics
- `GET /api/analytics/verification-status` - Verification stats

### Bulk Processing
- `POST /api/bulk/upload` - Upload CSV for processing
- `GET /api/bulk/download/<id>` - Download results
- `GET /api/bulk/template` - Download CSV template

### Health Check
- `GET /api/health` - API status check

## Dataset Information

### Original Columns
- `category`: Product category
- `rating`: Star rating (1-5)
- `label`: CG (fake) or OR (genuine)
- `text_`: Review text content

### Added Metrics (6 new columns)
1. **order_id**: Unique order identifier
2. **purchase_id**: Payment transaction ID
3. **verified_purchase**: Boolean (True if IDs match)
4. **user_id**: Reviewer identifier
5. **days_after_purchase**: Time between delivery and review
6. **user_review_count**: Total reviews by user

### Dataset Statistics
- Total Reviews: 40,432
- Fake Reviews (CG): 20,216 (50%)
- Genuine Reviews (OR): 20,216 (50%)
- Balanced dataset for optimal training

## Detection Logic

### A review is flagged as FAKE if:
1. Order ID is missing or doesn't exist
2. Purchase ID is missing or doesn't exist
3. Order ID and Purchase ID don't match (verified_purchase = False)
4. Review posted before purchase date (days_after_purchase < 0)
5. User has posted 50+ reviews (potential bot)
6. Extreme ratings (1 or 5 stars) with generic text
7. Text analysis shows suspicious patterns

### A review is considered GENUINE if:
1. Verified purchase = True
2. Order ID and Purchase ID exist and match
3. Reasonable timing (1-90 days after purchase)
4. Normal user behavior (< 30 reviews)
5. Detailed, specific review text

## Features

### Metadata Features (18)
- verified_purchase, order_id_missing, purchase_id_missing
- days_after_purchase, negative_days, very_late_review
- user_review_count, high_review_count
- rating, extreme_rating

### Text Features (18)
- review_length, word_count, avg_word_length
- sentence_count, exclamation_count, question_count
- caps_ratio, unique_word_ratio

### TF-IDF Features (30)
- Most important terms extracted from review text
- Captures semantic meaning and patterns

**Total: 48 Features**

## Theme

The application uses a professional dark theme by default for optimal visual experience.

## Troubleshooting

### Backend Issues

**Model not found error:**
```bash
cd ml_models
python3 train_model.py
```

**Port 5000 already in use:**
Change port in `backend/app.py`:
```python
app.run(port=5001)
```

### Frontend Issues

**Dependencies not installed:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Port 5173 already in use:**
Change port in `frontend/vite.config.js`:
```javascript
server: { port: 3000 }
```

### CORS Issues

If you encounter CORS errors, ensure:
1. Backend is running on port 5000
2. Frontend is running on port 5173
3. CORS is properly configured in `backend/config.py`

## Performance Optimization

- Model loads once at startup (not per request)
- Frontend uses React lazy loading
- API responses are cached when appropriate
- Bulk processing uses efficient pandas operations

## Future Enhancements

- User authentication and accounts
- Review history and saved analyses
- Advanced BERT-based text analysis
- Real-time review monitoring
- API rate limiting and authentication
- Docker containerization
- Deployment to cloud platforms

## Credits

- **Developer**: SIP II Project
- **Institution**: [Your Institution]
- **Dataset**: Fake Reviews Dataset (40,432 reviews)
- **Technologies**: React, Flask, scikit-learn, NLTK

## License

This project is for educational purposes as part of SIP II coursework.

## Contact

For questions or issues, please contact the development team.

---

**Built with React, Flask, and Machine Learning**

