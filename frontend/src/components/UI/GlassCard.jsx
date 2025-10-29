import { motion } from 'framer-motion';

const GlassCard = ({ children, className = '', hover = true, delay = 0 }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      whileHover={hover ? { y: -5, scale: 1.02 } : {}}
      className={`glass rounded-2xl shadow-xl p-6 transition-smooth ${className}`}
    >
      {children}
    </motion.div>
  );
};

export default GlassCard;

