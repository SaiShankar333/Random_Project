import { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, Download, FileText, Loader } from 'lucide-react';
import GlassCard from '../components/UI/GlassCard';
import { uploadBulkFile, downloadResults, downloadTemplate } from '../services/api';

const BulkAnalysis = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError(null);
    setUploadProgress(0);

    try {
      const data = await uploadBulkFile(file, (progressEvent) => {
        const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        setUploadProgress(progress);
      });
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleDownload = () => {
    if (result?.download_id) {
      window.open(downloadResults(result.download_id), '_blank');
    }
  };

  const handleDownloadTemplate = () => {
    window.open(downloadTemplate(), '_blank');
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
            Bulk Analysis
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Upload CSV file to analyze multiple reviews at once
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="space-y-6">
            <GlassCard>
              <h2 className="text-2xl font-semibold mb-6">Upload Reviews</h2>

              {/* Template Download */}
              <div className="mb-6 p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
                <div className="flex items-start">
                  <FileText className="w-5 h-5 text-blue-500 mr-3 flex-shrink-0 mt-0.5" />
                  <div className="flex-1">
                    <p className="text-sm text-gray-700 dark:text-gray-300 mb-2">
                      Need a template? Download our sample CSV file with the required format.
                    </p>
                    <button
                      onClick={handleDownloadTemplate}
                      className="text-sm text-primary-600 dark:text-primary-400 hover:underline font-medium"
                    >
                      Download Template
                    </button>
                  </div>
                </div>
              </div>

              {/* File Upload */}
              <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center">
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                
                <input
                  type="file"
                  accept=".csv,.xlsx"
                  onChange={handleFileChange}
                  className="hidden"
                  id="file-upload"
                />
                
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer px-6 py-3 rounded-lg bg-gradient-to-r from-primary-500 to-accent-500 text-white font-semibold hover:shadow-lg transition-all duration-300 inline-block"
                >
                  Choose File
                </label>
                
                {file && (
                  <div className="mt-4 text-sm text-gray-600 dark:text-gray-400">
                    Selected: {file.name}
                  </div>
                )}
                
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-4">
                  Supported formats: CSV, XLSX
                </p>
              </div>

              {/* Upload Button */}
              <button
                onClick={handleUpload}
                disabled={!file || uploading}
                className="w-full px-6 py-3 rounded-lg bg-gradient-to-r from-primary-500 to-accent-500 text-white font-semibold hover:shadow-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {uploading ? 'Processing...' : 'Analyze Reviews'}
              </button>

              {/* Upload Progress */}
              {uploading && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Upload Progress</span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      className="h-2 rounded-full bg-gradient-to-r from-primary-500 to-accent-500 transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    />
                  </div>
                </div>
              )}

              {/* Error Message */}
              {error && (
                <div className="p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
                  <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
                </div>
              )}
            </GlassCard>

            {/* Required Columns */}
            <GlassCard>
              <h3 className="text-lg font-semibold mb-3">Required Columns</h3>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-primary-500 rounded-full mr-2"></span>
                  text_ (review text)
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-primary-500 rounded-full mr-2"></span>
                  rating (1-5)
                </li>
              </ul>
              
              <h3 className="text-lg font-semibold mb-3 mt-4">Optional Columns</h3>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li>order_id, purchase_id, verified_purchase, user_id, days_after_purchase, user_review_count</li>
              </ul>
            </GlassCard>
          </div>

          {/* Results Section */}
          <div>
            {uploading && (
              <GlassCard>
                <div className="flex flex-col items-center justify-center py-12">
                  <Loader className="w-12 h-12 text-primary-500 animate-spin mb-4" />
                  <p className="text-gray-600 dark:text-gray-400">Processing your file...</p>
                </div>
              </GlassCard>
            )}

            {result && (
              <div className="space-y-6">
                {/* Summary */}
                <GlassCard>
                  <h2 className="text-2xl font-semibold mb-6">Analysis Results</h2>
                  
                  <div className="grid grid-cols-2 gap-4 mb-6">
                    <div className="p-4 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500 text-white">
                      <div className="text-3xl font-bold">{result.total}</div>
                      <div className="text-sm opacity-90">Total Reviews</div>
                    </div>
                    
                    <div className="p-4 rounded-lg bg-gradient-to-br from-red-500 to-pink-500 text-white">
                      <div className="text-3xl font-bold">{result.fake_count}</div>
                      <div className="text-sm opacity-90">Fake Reviews</div>
                    </div>
                    
                    <div className="p-4 rounded-lg bg-gradient-to-br from-green-500 to-emerald-500 text-white">
                      <div className="text-3xl font-bold">{result.genuine_count}</div>
                      <div className="text-sm opacity-90">Genuine Reviews</div>
                    </div>
                    
                    <div className="p-4 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 text-white">
                      <div className="text-3xl font-bold">{result.fake_percentage?.toFixed(1)}%</div>
                      <div className="text-sm opacity-90">Fake Rate</div>
                    </div>
                  </div>

                  {/* Download Button */}
                  <button
                    onClick={handleDownload}
                    className="w-full flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-gradient-to-r from-primary-500 to-accent-500 text-white font-semibold hover:shadow-lg transition-all duration-300"
                  >
                    <Download className="w-5 h-5" />
                    Download Results
                  </button>
                </GlassCard>

                {/* Preview */}
                {result.results_preview && result.results_preview.length > 0 && (
                  <GlassCard>
                    <h3 className="text-xl font-semibold mb-4">Preview (First 10 Results)</h3>
                    <div className="space-y-3 max-h-96 overflow-y-auto">
                      {result.results_preview.slice(0, 10).map((review, index) => (
                        <div
                          key={index}
                          className={`p-3 rounded-lg border ${
                            review.prediction === 'FAKE'
                              ? 'border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-900/20'
                              : 'border-green-200 bg-green-50 dark:border-green-800 dark:bg-green-900/20'
                          }`}
                        >
                          <div className="flex justify-between items-start mb-2">
                            <span
                              className={`px-2 py-1 rounded text-xs font-semibold ${
                                review.prediction === 'FAKE'
                                  ? 'bg-red-500 text-white'
                                  : 'bg-green-500 text-white'
                              }`}
                            >
                              {review.prediction}
                            </span>
                            <span className="text-sm text-gray-600 dark:text-gray-400">
                              {(review.confidence * 100).toFixed(1)}% confident
                            </span>
                          </div>
                          <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">
                            {review.text}
                          </p>
                        </div>
                      ))}
                    </div>
                  </GlassCard>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BulkAnalysis;

