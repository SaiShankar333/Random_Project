import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, AlertTriangle, CheckCircle, BarChart3 } from 'lucide-react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import GlassCard from '../components/UI/GlassCard';
import CustomTooltip from '../components/Charts/CustomTooltip';
import { getSummary, getCategoryStats } from '../services/api';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState(null);
  const [categoryData, setCategoryData] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [summaryData, catData] = await Promise.all([
        getSummary(),
        getCategoryStats()
      ]);
      console.log('Summary data:', summaryData);
      console.log('Category data:', catData);
      setSummary(summaryData);
      setCategoryData(catData.categories || []);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      alert('Failed to load dashboard data. Check console for details.');
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

  const pieData = [
    { name: 'Genuine', value: summary?.genuine_reviews || 0, color: '#10b981' },
    { name: 'Fake', value: summary?.fake_reviews || 0, color: '#ef4444' }
  ];

  const statsCards = [
    {
      title: 'Total Reviews',
      value: summary?.total_reviews ? summary.total_reviews.toLocaleString() : '0',
      icon: BarChart3,
      color: 'from-blue-500 to-cyan-500'
    },
    {
      title: 'Fake Reviews',
      value: summary?.fake_reviews ? summary.fake_reviews.toLocaleString() : '0',
      subtitle: summary?.fake_percentage ? `${summary.fake_percentage.toFixed(1)}%` : '0%',
      icon: AlertTriangle,
      color: 'from-red-500 to-pink-500'
    },
    {
      title: 'Genuine Reviews',
      value: summary?.genuine_reviews ? summary.genuine_reviews.toLocaleString() : '0',
      subtitle: summary?.genuine_percentage ? `${summary.genuine_percentage.toFixed(1)}%` : '0%',
      icon: CheckCircle,
      color: 'from-green-500 to-emerald-500'
    },
    {
      title: 'Model Accuracy',
      value: summary?.model_accuracy ? `${(summary.model_accuracy * 100).toFixed(1)}%` : '0%',
      icon: TrendingUp,
      color: 'from-purple-500 to-pink-500'
    }
  ];

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold gradient-text mb-2">
            Analytics Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Comprehensive overview of fake review detection results
          </p>
        </motion.div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statsCards.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <GlassCard key={index} delay={index * 0.1}>
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                      {stat.title}
                    </p>
                    <p className="text-3xl font-bold mb-1">
                      {stat.value}
                    </p>
                    {stat.subtitle && (
                      <p className="text-sm text-gray-500 dark:text-gray-500">
                        {stat.subtitle}
                      </p>
                    )}
                  </div>
                  <div className={`p-3 rounded-lg bg-gradient-to-br ${stat.color}`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                </div>
              </GlassCard>
            );
          })}
        </div>

        {/* Pie Chart */}
        <GlassCard className="mb-8">
          <h3 className="text-xl font-semibold mb-4">
            Review Distribution
          </h3>
          <ResponsiveContainer width="100%" height={350}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={120}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </GlassCard>

        {/* Bar Chart */}
        <GlassCard className="mb-8">
          <h3 className="text-xl font-semibold mb-4">
            Top Categories by Fake Rate
          </h3>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={categoryData.slice(0, 5)}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
              <XAxis dataKey="category" tick={{ fontSize: 12 }} />
              <YAxis />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="fake_rate" fill="#00ff88" radius={[8, 8, 0, 0]} name="Fake Rate" unit="%" />
            </BarChart>
          </ResponsiveContainer>
        </GlassCard>

        {/* Category Table */}
        <GlassCard>
          <h3 className="text-xl font-semibold mb-4">
            Reviews by Category
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <th className="text-left py-3 px-4">Category</th>
                  <th className="text-right py-3 px-4">Total</th>
                  <th className="text-right py-3 px-4">Fake</th>
                  <th className="text-right py-3 px-4">Genuine</th>
                  <th className="text-right py-3 px-4">Fake Rate</th>
                </tr>
              </thead>
              <tbody>
                {categoryData.map((cat, index) => (
                  <tr
                    key={index}
                    className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                  >
                    <td className="py-3 px-4 font-medium">{cat.category}</td>
                    <td className="py-3 px-4 text-right">{cat.total.toLocaleString()}</td>
                    <td className="py-3 px-4 text-right text-red-600">{cat.fake.toLocaleString()}</td>
                    <td className="py-3 px-4 text-right text-green-600">{cat.genuine.toLocaleString()}</td>
                    <td className="py-3 px-4 text-right">
                      <span className={`px-2 py-1 rounded-full text-sm ${
                        cat.fake_rate > 60 ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' :
                        cat.fake_rate > 40 ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
                        'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      }`}>
                        {cat.fake_rate.toFixed(1)}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};

export default Dashboard;

