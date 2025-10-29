import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Target, Activity, Award } from 'lucide-react';
import GlassCard from '../components/UI/GlassCard';
import { getModelPerformance } from '../services/api';

const Performance = () => {
  const [loading, setLoading] = useState(true);
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    loadPerformance();
  }, []);

  const loadPerformance = async () => {
    try {
      const data = await getModelPerformance();
      setMetrics(data);
    } catch (error) {
      console.error('Error loading performance data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  const metricsCards = [
    {
      title: 'Accuracy',
      value: `${(metrics?.accuracy * 100)?.toFixed(2)}%`,
      icon: Target,
      color: 'from-blue-500 to-cyan-500',
      description: 'Overall correct predictions'
    },
    {
      title: 'Precision',
      value: `${(metrics?.precision * 100)?.toFixed(2)}%`,
      icon: TrendingUp,
      color: 'from-green-500 to-emerald-500',
      description: 'Accuracy of fake predictions'
    },
    {
      title: 'Recall',
      value: `${(metrics?.recall * 100)?.toFixed(2)}%`,
      icon: Activity,
      color: 'from-purple-500 to-pink-500',
      description: 'Fake reviews caught'
    },
    {
      title: 'F1-Score',
      value: `${(metrics?.f1_score * 100)?.toFixed(2)}%`,
      icon: Award,
      color: 'from-orange-500 to-red-500',
      description: 'Harmonic mean of precision and recall'
    }
  ];

  const cm = metrics?.confusion_matrix;

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold gradient-text mb-2">
            Model Performance
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Detailed evaluation metrics for the fake review detection model
          </p>
        </motion.div>

        {/* Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {metricsCards.map((metric, index) => {
            const Icon = metric.icon;
            return (
              <GlassCard key={index} delay={index * 0.1}>
                <div className="flex items-start justify-between mb-4">
                  <div className={`p-3 rounded-lg bg-gradient-to-br ${metric.color}`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                </div>
                <h3 className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                  {metric.title}
                </h3>
                <p className="text-3xl font-bold mb-2">
                  {metric.value}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-500">
                  {metric.description}
                </p>
              </GlassCard>
            );
          })}
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Confusion Matrix */}
          <GlassCard>
            <h2 className="text-2xl font-semibold mb-6">Confusion Matrix</h2>
            
            <div className="grid grid-cols-2 gap-4">
              {/* True Negatives */}
              <div className="p-6 rounded-lg bg-gradient-to-br from-green-500 to-emerald-500 text-white text-center">
                <div className="text-4xl font-bold mb-2">{cm?.true_negatives}</div>
                <div className="text-sm opacity-90">True Negatives</div>
                <div className="text-xs opacity-75 mt-1">Genuine correctly identified</div>
              </div>

              {/* False Positives */}
              <div className="p-6 rounded-lg bg-gradient-to-br from-yellow-500 to-orange-500 text-white text-center">
                <div className="text-4xl font-bold mb-2">{cm?.false_positives}</div>
                <div className="text-sm opacity-90">False Positives</div>
                <div className="text-xs opacity-75 mt-1">Genuine flagged as fake</div>
              </div>

              {/* False Negatives */}
              <div className="p-6 rounded-lg bg-gradient-to-br from-orange-500 to-red-500 text-white text-center">
                <div className="text-4xl font-bold mb-2">{cm?.false_negatives}</div>
                <div className="text-sm opacity-90">False Negatives</div>
                <div className="text-xs opacity-75 mt-1">Fake missed</div>
              </div>

              {/* True Positives */}
              <div className="p-6 rounded-lg bg-gradient-to-br from-green-500 to-emerald-500 text-white text-center">
                <div className="text-4xl font-bold mb-2">{cm?.true_positives}</div>
                <div className="text-sm opacity-90">True Positives</div>
                <div className="text-xs opacity-75 mt-1">Fake correctly identified</div>
              </div>
            </div>

            <div className="mt-6 p-4 rounded-lg bg-gray-50 dark:bg-gray-800/50">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                The confusion matrix shows how well the model distinguishes between genuine and fake reviews.
                Perfect classification would show values only in the green boxes (diagonal).
              </p>
            </div>
          </GlassCard>

          {/* Classification Report */}
          <GlassCard>
            <h2 className="text-2xl font-semibold mb-6">Classification Report</h2>
            
            <div className="space-y-4">
              {/* Genuine Reviews (Class 0) */}
              <div className="p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                <h3 className="font-semibold text-lg mb-3 text-green-600 dark:text-green-400">
                  Genuine Reviews (Class 0)
                </h3>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <div className="text-gray-500 dark:text-gray-400">Precision</div>
                    <div className="text-xl font-semibold">
                      {(metrics?.classification_report?.['0']?.precision * 100)?.toFixed(1)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-gray-500 dark:text-gray-400">Recall</div>
                    <div className="text-xl font-semibold">
                      {(metrics?.classification_report?.['0']?.recall * 100)?.toFixed(1)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-gray-500 dark:text-gray-400">F1-Score</div>
                    <div className="text-xl font-semibold">
                      {(metrics?.classification_report?.['0']?.['f1-score'] * 100)?.toFixed(1)}%
                    </div>
                  </div>
                </div>
              </div>

              {/* Fake Reviews (Class 1) */}
              <div className="p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                <h3 className="font-semibold text-lg mb-3 text-red-600 dark:text-red-400">
                  Fake Reviews (Class 1)
                </h3>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <div className="text-gray-500 dark:text-gray-400">Precision</div>
                    <div className="text-xl font-semibold">
                      {(metrics?.classification_report?.['1']?.precision * 100)?.toFixed(1)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-gray-500 dark:text-gray-400">Recall</div>
                    <div className="text-xl font-semibold">
                      {(metrics?.classification_report?.['1']?.recall * 100)?.toFixed(1)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-gray-500 dark:text-gray-400">F1-Score</div>
                    <div className="text-xl font-semibold">
                      {(metrics?.classification_report?.['1']?.['f1-score'] * 100)?.toFixed(1)}%
                    </div>
                  </div>
                </div>
              </div>

              {/* ROC-AUC */}
              <div className="p-4 rounded-lg bg-gradient-to-r from-primary-500 to-accent-500 text-white">
                <div className="text-sm opacity-90 mb-1">ROC-AUC Score</div>
                <div className="text-3xl font-bold">
                  {metrics?.roc_auc?.toFixed(4)}
                </div>
                <div className="text-xs opacity-75 mt-2">
                  Area under the ROC curve - measures model's ability to distinguish classes
                </div>
              </div>
            </div>
          </GlassCard>
        </div>

        {/* Model Information */}
        <GlassCard className="mt-8">
          <h2 className="text-2xl font-semibold mb-6">Model Information</h2>
          
          <div className="grid md:grid-cols-3 gap-6">
            <div>
              <h3 className="text-sm text-gray-500 dark:text-gray-400 mb-2">Model Type</h3>
              <p className="text-lg font-semibold">Random Forest Classifier</p>
            </div>
            <div>
              <h3 className="text-sm text-gray-500 dark:text-gray-400 mb-2">Training Dataset</h3>
              <p className="text-lg font-semibold">40,432 reviews</p>
            </div>
            <div>
              <h3 className="text-sm text-gray-500 dark:text-gray-400 mb-2">Features Used</h3>
              <p className="text-lg font-semibold">48 features</p>
            </div>
          </div>

          <div className="mt-6 p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
            <h3 className="font-semibold mb-2 text-blue-900 dark:text-blue-100">Feature Categories</h3>
            <ul className="space-y-1 text-sm text-blue-800 dark:text-blue-200">
              <li>• Metadata verification (10 features: order ID, purchase ID, verified purchase, timing, user behavior)</li>
              <li>• Text statistics (8 features: length, word count, sentence count, punctuation, caps ratio)</li>
              <li>• TF-IDF vectors (30 most important terms from review text)</li>
            </ul>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};

export default Performance;

