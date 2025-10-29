import { motion } from 'framer-motion';

const BlobBackground = ({ color = 'primary', size = 'large', opacity = 0.5 }) => {
  const sizeClasses = {
    small: 'w-64 h-64',
    medium: 'w-96 h-96',
    large: 'w-[600px] h-[600px]',
  };

  const colorClasses = {
    primary: 'from-primary-400 to-primary-600',
    accent: 'from-accent-400 to-accent-600',
    success: 'from-green-400 to-green-600',
    danger: 'from-red-400 to-red-600',
  };

  return (
    <motion.div
      className={`absolute blob ${sizeClasses[size]} bg-gradient-to-br ${colorClasses[color]} blur-3xl`}
      style={{ opacity }}
      animate={{
        x: [0, 30, -30, 0],
        y: [0, -30, 30, 0],
        scale: [1, 1.1, 0.9, 1],
        rotate: [0, 5, -5, 0],
      }}
      transition={{
        duration: 15,
        repeat: Infinity,
        ease: "easeInOut"
      }}
    />
  );
};

export default BlobBackground;

