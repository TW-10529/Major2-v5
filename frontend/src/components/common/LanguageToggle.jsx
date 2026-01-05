import React from 'react';
import { Globe } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

const LanguageToggle = () => {
  const { language, toggleLanguage } = useLanguage();

  return (
    <button
      onClick={toggleLanguage}
      className="flex items-center space-x-2 px-3 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
      title={language === 'en' ? 'Switch to Japanese' : '日本語に切り替え'}
    >
      <Globe className="w-4 h-4 text-gray-600" />
      <span className="text-sm font-medium text-gray-700">
        {language === 'en' ? 'EN' : 'JA'}
      </span>
    </button>
  );
};

export default LanguageToggle;
