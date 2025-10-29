import React, { useState, useEffect } from 'react';
import { X, Plus, Trash2 } from 'lucide-react';

const AddAPIModal = ({ isOpen, onClose, onSubmit, editMode = false, initialData = null }) => {
  const getInitialFormData = () => ({
    api_name: '',
    description: '',
    category: 'other',
    endpoint: '',
    method: 'GET',
    intent_keywords: [],
    parameters: { required: [], optional: [] },
    response_mapping: {},
    response_template: '',
    auth_config: { type: 'none' },
    rate_limit: { requests_per_minute: 60 },
  });

  const [formData, setFormData] = useState(getInitialFormData());
  const [currentKeyword, setCurrentKeyword] = useState('');
  const [currentParam, setCurrentParam] = useState({ name: '', type: 'string', description: '' });
  const [currentMapping, setCurrentMapping] = useState({ key: '', path: '' });
  const [customCategory, setCustomCategory] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  // Populate form when editing
  useEffect(() => {
    if (isOpen && editMode && initialData) {
      const predefinedCategories = ['weather', 'crypto', 'news', 'reference', 'finance', 'sports', 'other'];
      const isCustomCategory = !predefinedCategories.includes(initialData.category);
      
      const populatedData = {
        api_name: initialData.api_name || '',
        description: initialData.description || '',
        category: isCustomCategory ? 'other' : (initialData.category || 'other'),
        endpoint: initialData.endpoint || '',
        method: initialData.method || 'GET',
        intent_keywords: Array.isArray(initialData.intent_keywords) ? initialData.intent_keywords : [],
        parameters: initialData.parameters || { required: [], optional: [] },
        response_mapping: initialData.response_mapping || {},
        response_template: initialData.response_template || '',
        auth_config: initialData.auth_config || { type: 'none' },
        rate_limit: initialData.rate_limit || { requests_per_minute: 60 },
      };
      
      setFormData(populatedData);
      
      if (isCustomCategory) {
        setCustomCategory(initialData.category);
      }
    } else if (isOpen && !editMode) {
      // Reset form for new API
      setFormData(getInitialFormData());
      setCustomCategory('');
    }
  }, [isOpen, editMode, initialData]);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    try {
      // Use custom category if "other" is selected
      const submitData = {
        ...formData,
        category: formData.category === 'other' && customCategory.trim() 
          ? customCategory.trim().toLowerCase() 
          : formData.category
      };
      
      await onSubmit(submitData);
      // Reset form only if not in edit mode (edit mode closes via onClose)
      if (!editMode) {
        setFormData(getInitialFormData());
        setCustomCategory('');
      }
      onClose();
    } catch (err) {
      setError(err.message || `Failed to ${editMode ? 'update' : 'add'} API`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const addKeyword = () => {
    if (currentKeyword.trim()) {
      setFormData({
        ...formData,
        intent_keywords: [...formData.intent_keywords, currentKeyword.trim()],
      });
      setCurrentKeyword('');
    }
  };

  const removeKeyword = (index) => {
    setFormData({
      ...formData,
      intent_keywords: formData.intent_keywords.filter((_, i) => i !== index),
    });
  };

  const addParameter = (type) => {
    if (currentParam.name.trim()) {
      const newParams = { ...formData.parameters };
      newParams[type] = [...newParams[type], { ...currentParam }];
      setFormData({ ...formData, parameters: newParams });
      setCurrentParam({ name: '', type: 'string', description: '' });
    }
  };

  const removeParameter = (type, index) => {
    const newParams = { ...formData.parameters };
    newParams[type] = newParams[type].filter((_, i) => i !== index);
    setFormData({ ...formData, parameters: newParams });
  };

  const addMapping = () => {
    if (currentMapping.key.trim() && currentMapping.path.trim()) {
      setFormData({
        ...formData,
        response_mapping: {
          ...formData.response_mapping,
          [currentMapping.key]: currentMapping.path,
        },
      });
      setCurrentMapping({ key: '', path: '' });
    }
  };

  const removeMapping = (key) => {
    const newMapping = { ...formData.response_mapping };
    delete newMapping[key];
    setFormData({ ...formData, response_mapping: newMapping });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-800">
            {editMode ? 'Edit API' : 'Add New API'}
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto p-6 space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {/* Basic Information */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">Basic Information</h3>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                API Name *
              </label>
              <input
                type="text"
                required
                value={formData.api_name}
                onChange={(e) => setFormData({ ...formData, api_name: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="e.g., CoinGecko Crypto API"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description *
              </label>
              <textarea
                required
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                rows="3"
                placeholder="Describe what this API does"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Category *
                </label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="weather">Weather</option>
                  <option value="crypto">Crypto</option>
                  <option value="news">News</option>
                  <option value="dictionary">Dictionary</option>
                  <option value="finance">Finance</option>
                  <option value="reference">Reference</option>
                  <option value="sports">Sports</option>
                  <option value="other">Other</option>
                </select>
              </div>

              {formData.category === 'other' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Custom Category *
                  </label>
                  <input
                    type="text"
                    required
                    value={customCategory}
                    onChange={(e) => setCustomCategory(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="e.g., entertainment, gaming"
                  />
                </div>
              )}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Method *
                </label>
                <select
                  value={formData.method}
                  onChange={(e) => setFormData({ ...formData, method: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="GET">GET</option>
                  <option value="POST">POST</option>
                  <option value="PUT">PUT</option>
                  <option value="DELETE">DELETE</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Endpoint URL *
              </label>
              <input
                type="url"
                required
                value={formData.endpoint}
                onChange={(e) => setFormData({ ...formData, endpoint: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="https://api.example.com/v1/endpoint"
              />
              <p className="text-xs text-gray-500 mt-1">
                Use {'{paramName}'} for path parameters, e.g., /users/{'{userId}'}
              </p>
            </div>
          </div>

          {/* Authentication */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">Authentication</h3>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Authentication Type *
              </label>
              <select
                value={formData.auth_config.type}
                onChange={(e) => setFormData({ 
                  ...formData, 
                  auth_config: { type: e.target.value }
                })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="none">None (No Authentication)</option>
                <option value="header">Header (API Key in Header)</option>
                <option value="query">Query Parameter (API Key in URL)</option>
                <option value="bearer">Bearer Token</option>
              </select>
            </div>

            {formData.auth_config.type === 'header' && (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Header Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.auth_config.header_name || ''}
                    onChange={(e) => setFormData({ 
                      ...formData, 
                      auth_config: { 
                        ...formData.auth_config, 
                        header_name: e.target.value 
                      }
                    })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="e.g., X-API-Key, X-Auth-Token, Authorization"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    API Key *
                  </label>
                  <input
                    type="password"
                    required
                    value={formData.auth_config.key || ''}
                    onChange={(e) => setFormData({ 
                      ...formData, 
                      auth_config: { 
                        ...formData.auth_config, 
                        key: e.target.value 
                      }
                    })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="Your API key"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    🔒 Your API key will be encrypted and stored securely
                  </p>
                </div>
              </>
            )}

            {formData.auth_config.type === 'query' && (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Parameter Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.auth_config.param_name || ''}
                    onChange={(e) => setFormData({ 
                      ...formData, 
                      auth_config: { 
                        ...formData.auth_config, 
                        param_name: e.target.value 
                      }
                    })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="e.g., apikey, api_key, token"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    API Key *
                  </label>
                  <input
                    type="password"
                    required
                    value={formData.auth_config.key || ''}
                    onChange={(e) => setFormData({ 
                      ...formData, 
                      auth_config: { 
                        ...formData.auth_config, 
                        key: e.target.value 
                      }
                    })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="Your API key"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    🔒 Your API key will be encrypted and stored securely
                  </p>
                </div>
              </>
            )}

            {formData.auth_config.type === 'bearer' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Bearer Token *
                </label>
                <input
                  type="password"
                  required
                  value={formData.auth_config.key || ''}
                  onChange={(e) => setFormData({ 
                    ...formData, 
                    auth_config: { 
                      ...formData.auth_config, 
                      key: e.target.value 
                    }
                  })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Your bearer token"
                />
                <p className="text-xs text-gray-500 mt-1">
                  🔒 Will be sent as "Authorization: Bearer {'{token}'}"
                </p>
              </div>
            )}
          </div>

          {/* Parameters */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">Parameters</h3>
            <p className="text-sm text-gray-600">
              Add parameters that this API accepts
            </p>

            <div className="space-y-3">
              <div className="space-y-2">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={currentParam.name}
                    onChange={(e) => setCurrentParam({ ...currentParam, name: e.target.value })}
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="Parameter name (e.g., t, city, q, apikey)"
                  />
                  <select
                    value={currentParam.type}
                    onChange={(e) => setCurrentParam({ ...currentParam, type: e.target.value })}
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="string">String</option>
                    <option value="number">Number</option>
                    <option value="boolean">Boolean</option>
                  </select>
                </div>
                <input
                  type="text"
                  value={currentParam.description}
                  onChange={(e) => setCurrentParam({ ...currentParam, description: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Description (e.g., API key for authentication, Team name to search)"
                />
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => addParameter('required')}
                    className="btn-primary whitespace-nowrap flex-1"
                    title="Add as required parameter"
                  >
                    Add Required
                  </button>
                  <button
                    type="button"
                    onClick={() => addParameter('optional')}
                    className="btn-secondary whitespace-nowrap flex-1"
                    title="Add as optional parameter"
                  >
                    Add Optional
                  </button>
                </div>
              </div>

              {formData.parameters.required.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Required Parameters:</h4>
                  <div className="space-y-2">
                    {formData.parameters.required.map((param, index) => (
                      <div key={index} className="flex items-start justify-between p-3 bg-red-50 rounded-lg">
                        <div className="flex-1">
                          <div className="font-mono text-sm font-medium text-gray-800">
                            {param.name} <span className="text-gray-500">({param.type})</span>
                          </div>
                          {param.description && (
                            <div className="text-xs text-gray-600 mt-1">{param.description}</div>
                          )}
                        </div>
                        <button
                          type="button"
                          onClick={() => removeParameter('required', index)}
                          className="p-1 hover:bg-red-100 rounded ml-2"
                        >
                          <Trash2 className="w-4 h-4 text-red-500" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {formData.parameters.optional.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Optional Parameters:</h4>
                  <div className="space-y-2">
                    {formData.parameters.optional.map((param, index) => (
                      <div key={index} className="flex items-start justify-between p-3 bg-blue-50 rounded-lg">
                        <div className="flex-1">
                          <div className="font-mono text-sm font-medium text-gray-800">
                            {param.name} <span className="text-gray-500">({param.type})</span>
                          </div>
                          {param.description && (
                            <div className="text-xs text-gray-600 mt-1">{param.description}</div>
                          )}
                        </div>
                        <button
                          type="button"
                          onClick={() => removeParameter('optional', index)}
                          className="p-1 hover:bg-blue-100 rounded ml-2"
                        >
                          <Trash2 className="w-4 h-4 text-blue-500" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Intent Keywords */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">Intent Keywords</h3>
            <p className="text-sm text-gray-600">
              Add keywords that will trigger this API (e.g., "weather", "temperature", "forecast")
            </p>
            
            <div className="flex gap-2">
              <input
                type="text"
                value={currentKeyword}
                onChange={(e) => setCurrentKeyword(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addKeyword())}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="Add a keyword"
              />
              <button
                type="button"
                onClick={addKeyword}
                className="btn-primary"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>

            <div className="flex flex-wrap gap-2">
              {formData.intent_keywords.map((keyword, index) => (
                <span
                  key={index}
                  className="inline-flex items-center gap-2 px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm"
                >
                  {keyword}
                  <button
                    type="button"
                    onClick={() => removeKeyword(index)}
                    className="hover:text-primary-900"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </span>
              ))}
            </div>
          </div>

          {/* Response Mapping */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">Response Mapping</h3>
            <p className="text-sm text-gray-600">
              Map fields from the API response to template variables
            </p>

            <div className="flex gap-2">
              <input
                type="text"
                value={currentMapping.key}
                onChange={(e) => setCurrentMapping({ ...currentMapping, key: e.target.value })}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="Variable name (e.g., temperature)"
              />
              <input
                type="text"
                value={currentMapping.path}
                onChange={(e) => setCurrentMapping({ ...currentMapping, path: e.target.value })}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="JSON path (e.g., main.temp)"
              />
              <button
                type="button"
                onClick={addMapping}
                className="btn-primary"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-2">
              {Object.entries(formData.response_mapping).map(([key, path]) => (
                <div
                  key={key}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex-1">
                    <span className="font-mono text-sm text-gray-800">{key}</span>
                    <span className="text-gray-500 mx-2">→</span>
                    <span className="font-mono text-sm text-gray-600">{path}</span>
                  </div>
                  <button
                    type="button"
                    onClick={() => removeMapping(key)}
                    className="p-1 hover:bg-gray-200 rounded"
                  >
                    <Trash2 className="w-4 h-4 text-red-500" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Response Template */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">Response Template</h3>
            <p className="text-sm text-gray-600">
              Use {'{variable}'} to insert mapped values
            </p>
            
            <textarea
              value={formData.response_template}
              onChange={(e) => setFormData({ ...formData, response_template: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent font-mono text-sm"
              rows="3"
              placeholder="The temperature is {temperature}°C"
            />
          </div>
        </form>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 p-6 border-t border-gray-200">
          <button
            type="button"
            onClick={onClose}
            className="btn-secondary"
            disabled={isSubmitting}
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            className="btn-primary"
            disabled={isSubmitting}
          >
            {isSubmitting 
              ? (editMode ? 'Updating...' : 'Adding...') 
              : (editMode ? 'Update API' : 'Add API')
            }
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddAPIModal;
