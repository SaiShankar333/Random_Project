import { useState } from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, CheckCircle, AlertCircle, Loader } from 'lucide-react';
import GlassCard from '../components/UI/GlassCard';
import { predictReview } from '../services/api';

const Detector = () => {
  const [formData, setFormData] = useState({
    text_: '',
    rating: 5,
    order_id: '',
    purchase_id: '',
    verified_purchase: true,
    user_id: '',
    days_after_purchase: 30,
    user_review_count: 1,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await predictReview(formData);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.error || 'Prediction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const loadExample = (type) => {
    if (type === 'fake') {
      setFormData({
        text_: 'This product is amazing! Best purchase ever!',
        rating: 5,
        order_id: '',
        purchase_id: 'PUR-ABC123',
        verified_purchase: false,
        user_id: 'USER-12345',
        days_after_purchase: -5,
        user_review_count: 150,
      });
    } else {
      setFormData({
        text_: 'I purchased this product last month and have been using it daily. The quality is good and it works as described. Delivery was on time.',
        rating: 4,
        order_id: 'ORD-2024-12345',
        purchase_id: 'PUR-XYZ789',
        verified_purchase: true,
        user_id: 'USER-67890',
        days_after_purchase: 15,
        user_review_count: 3,
      });
    }
    setResult(null);
  };

  const getStatusIcon = () => {
    if (!result) return null;
    
    if (result.status === 'FAKE') {
      return <AlertTriangle className="w-16 h-16 text-red-500" />;
    } else if (result.status === 'SUSPICIOUS') {
      return <AlertCircle className="w-16 h-16 text-yellow-500" />;
    } else {
      return <CheckCircle className="w-16 h-16 text-green-500" />;
    }
  };

  const getStatusColor = () => {
    if (!result) return '';
    if (result.status === 'FAKE') return 'from-red-500 to-pink-500';
    if (result.status === 'SUSPICIOUS') return 'from-yellow-500 to-orange-500';
    return 'from-green-500 to-emerald-500';
  };

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold gradient-text mb-2">
            Review Detector
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Analyze a single review for fake patterns and suspicious indicators
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <GlassCard>
            <h2 className="text-2xl font-semibold mb-6">Review Information</h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Review Text */}
              <div>
                <label className="block text-sm font-medium mb-2">
                  Review Text *
                </label>
                <textarea
                  name="text_"
                  value={formData.text_}
                  onChange={handleChange}
                  required
                  rows={4}
                  className="w-full px-4 py-2 rounded-lg glass border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 outline-none transition-all"
                  placeholder="Enter the review text..."
                />
              </div>

              {/* Rating */}
              <div>
                <label className="block text-sm font-medium mb-2">
                  Rating *
                </label>
                <select
                  name="rating"
                  value={formData.rating}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 rounded-lg glass border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 outline-none transition-all"
                >
                  <option value={1}>1 Star</option>
                  <option value={2}>2 Stars</option>
                  <option value={3}>3 Stars</option>
                  <option value={4}>4 Stars</option>
                  <option value={5}>5 Stars</option>
                </select>
              </div>

              {/* Order ID */}
              <div>
                <label className="block text-sm font-medium mb-2">
                  Order ID
                </label>
                <input
                  type="text"
                  name="order_id"
                  value={formData.order_id}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg glass border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 outline-none transition-all"
                  placeholder="e.g., ORD-2024-12345"
                />
              </div>

              {/* Purchase ID */}
              <div>
                <label className="block text-sm font-medium mb-2">
                  Purchase ID
                </label>
                <input
                  type="text"
                  name="purchase_id"
                  value={formData.purchase_id}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg glass border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 outline-none transition-all"
                  placeholder="e.g., PUR-ABC123"
                />
              </div>

              {/* Verified Purchase */}
              <div className="flex items-center">
                <input
                  type="checkbox"
                  name="verified_purchase"
                  checked={formData.verified_purchase}
                  onChange={handleChange}
                  className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
                />
                <label className="ml-2 text-sm font-medium">
                  Verified Purchase
                </label>
              </div>

              {/* Days After Purchase */}
              <div>
                <label className="block text-sm font-medium mb-2">
                  Days After Purchase
                </label>
                <input
                  type="number"
                  name="days_after_purchase"
                  value={formData.days_after_purchase}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg glass border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 outline-none transition-all"
                />
              </div>

              {/* User Review Count */}
              <div>
                <label className="block text-sm font-medium mb-2">
                  User Review Count
                </label>
                <input
                  type="number"
                  name="user_review_count"
                  value={formData.user_review_count}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg glass border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 outline-none transition-all"
                />
              </div>

              {/* Buttons */}
              <div className="flex gap-2 pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 px-6 py-3 rounded-lg bg-gradient-to-r from-primary-500 to-accent-500 text-white font-semibold hover:shadow-lg transition-all duration-300 disabled:opacity-50"
                >
                  {loading ? 'Analyzing...' : 'Analyze Review'}
                </button>
              </div>

              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => loadExample('fake')}
                  className="flex-1 px-4 py-2 rounded-lg glass border border-gray-300 dark:border-gray-600 text-sm hover:bg-gray-100 dark:hover:bg-gray-800 transition-all"
                >
                  Load Fake Example
                </button>
                <button
                  type="button"
                  onClick={() => loadExample('genuine')}
                  className="flex-1 px-4 py-2 rounded-lg glass border border-gray-300 dark:border-gray-600 text-sm hover:bg-gray-100 dark:hover:bg-gray-800 transition-all"
                >
                  Load Genuine Example
                </button>
              </div>
            </form>
          </GlassCard>

          {/* Results */}
          <div className="space-y-6">
            {loading && (
              <GlassCard>
                <div className="flex flex-col items-center justify-center py-12">
                  <Loader className="w-12 h-12 text-primary-500 animate-spin mb-4" />
                  <p className="text-gray-600 dark:text-gray-400">Analyzing review...</p>
                </div>
              </GlassCard>
            )}

            {error && (
              <GlassCard>
                <div className="text-center py-8">
                  <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-4" />
                  <p className="text-red-600 dark:text-red-400">{error}</p>
                </div>
              </GlassCard>
            )}

            {result && (
              <>
                {/* Main Result */}
                <GlassCard>
                  <div className="text-center py-8">
                    <div className="flex justify-center mb-4">
                      {getStatusIcon()}
                    </div>
                    <h3 className={`text-3xl font-bold mb-2 bg-gradient-to-r ${getStatusColor()} bg-clip-text text-transparent`}>
                      {result.status}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 mb-4">
                      Confidence: {(result.confidence * 100).toFixed(1)}%
                    </p>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                      <div
                        className={`h-3 rounded-full bg-gradient-to-r ${getStatusColor()}`}
                        style={{ width: `${result.confidence * 100}%` }}
                      />
                    </div>
                  </div>
                </GlassCard>

                {/* Probabilities */}
                <GlassCard>
                  <h3 className="text-xl font-semibold mb-4">Prediction Breakdown</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600 dark:text-gray-400">Fake Probability</span>
                      <span className="font-semibold text-red-600">
                        {(result.fake_probability * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600 dark:text-gray-400">Genuine Probability</span>
                      <span className="font-semibold text-green-600">
                        {(result.genuine_probability * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </GlassCard>

                {/* Risk Factors */}
                {result.risk_factors && result.risk_factors.length > 0 && (
                  <GlassCard>
                    <h3 className="text-xl font-semibold mb-4">Risk Factors</h3>
                    <ul className="space-y-2">
                      {result.risk_factors.map((factor, index) => (
                        <li key={index} className="flex items-start">
                          <AlertCircle className="w-5 h-5 text-yellow-500 mr-2 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-700 dark:text-gray-300">{factor}</span>
                        </li>
                      ))}
                    </ul>
                  </GlassCard>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Detector;

