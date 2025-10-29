import React, { useState, useEffect } from 'react';
import { Database, Plus, X, CheckCircle, XCircle, Loader2, Trash2, Edit2 } from 'lucide-react';
import { apiManagementAPI } from '../api/client';
import AddAPIModal from './AddAPIModal';

const Sidebar = ({ isOpen, onClose }) => {
  const [apis, setApis] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [editingAPI, setEditingAPI] = useState(null);
  
  useEffect(() => {
    if (isOpen) {
      loadAPIs();
    }
  }, [isOpen]);
  
  const loadAPIs = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiManagementAPI.listAPIs(true);
      setApis(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddAPI = async (apiData) => {
    try {
      if (editingAPI) {
        // Update existing API
        await apiManagementAPI.updateAPI(editingAPI.api_id, apiData);
      } else {
        // Add new API
        await apiManagementAPI.registerAPI(apiData);
      }
      await loadAPIs(); // Reload the list
      setEditingAPI(null); // Clear edit mode
    } catch (err) {
      throw new Error(err.message || 'Failed to save API');
    }
  };

  const handleEditAPI = (api) => {
    setEditingAPI(api);
    setIsAddModalOpen(true);
  };

  const handleDeleteAPI = async (apiId, apiName) => {
    if (!window.confirm(`Are you sure you want to delete "${apiName}"?`)) {
      return;
    }

    try {
      await apiManagementAPI.deleteAPI(apiId);
      await loadAPIs(); // Reload the list
    } catch (err) {
      setError(err.message || 'Failed to delete API');
    }
  };
  
  if (!isOpen) return null;
  
  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
        onClick={onClose}
      />
      
      {/* Sidebar */}
      <div className={`fixed inset-y-0 right-0 w-80 bg-white shadow-xl z-50 transform transition-transform duration-300 ease-in-out ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            <div className="flex items-center gap-2">
              <Database className="w-5 h-5 text-primary-600" />
              <h2 className="text-lg font-semibold text-gray-800">
                Registered APIs
              </h2>
            </div>
            <button
              onClick={onClose}
              className="p-1 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <X className="w-5 h-5 text-gray-600" />
            </button>
          </div>
          
          {/* Content */}
          <div className="flex-1 overflow-y-auto p-4">
            {isLoading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 text-primary-500 animate-spin" />
              </div>
            ) : error ? (
              <div className="text-center py-12">
                <XCircle className="w-12 h-12 text-red-500 mx-auto mb-3" />
                <p className="text-red-600 text-sm">{error}</p>
                <button
                  onClick={loadAPIs}
                  className="btn-secondary mt-4"
                >
                  Retry
                </button>
              </div>
            ) : apis.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                <Database className="w-12 h-12 mx-auto mb-3 opacity-30" />
                <p className="text-sm">No APIs registered yet</p>
              </div>
            ) : (
              <div className="space-y-3">
                {apis.map((api) => (
                  <APICard 
                    key={api.api_id} 
                    api={api} 
                    onDelete={handleDeleteAPI}
                    onEdit={handleEditAPI}
                  />
                ))}
              </div>
            )}
          </div>
          
          {/* Footer */}
          <div className="p-4 border-t border-gray-200">
            <button 
              onClick={() => setIsAddModalOpen(true)}
              className="btn-primary w-full flex items-center justify-center gap-2"
            >
              <Plus className="w-4 h-4" />
              <span>Add New API</span>
            </button>
          </div>
        </div>
      </div>

      {/* Add API Modal */}
      <AddAPIModal
        isOpen={isAddModalOpen}
        onClose={() => {
          setIsAddModalOpen(false);
          setEditingAPI(null);
        }}
        onSubmit={handleAddAPI}
        editMode={!!editingAPI}
        initialData={editingAPI}
      />
    </>
  );
};

const APICard = ({ api, onDelete, onEdit }) => {
  const categoryColors = {
    weather: 'bg-blue-100 text-blue-800',
    crypto: 'bg-yellow-100 text-yellow-800',
    news: 'bg-purple-100 text-purple-800',
    reference: 'bg-green-100 text-green-800',
    finance: 'bg-indigo-100 text-indigo-800',
    sports: 'bg-orange-100 text-orange-800',
    other: 'bg-gray-100 text-gray-800',
  };
  
  const categoryColor = categoryColors[api.category] || categoryColors.other;
  const isActive = api.is_active !== false;
  const isUserAPI = api.is_system === false;
  
  return (
    <div className="bg-gray-50 rounded-lg p-3 border border-gray-200 hover:border-primary-300 transition-colors">
      <div className="flex items-start justify-between mb-2">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <h3 className="font-semibold text-gray-800 text-sm">
              {api.api_name}
            </h3>
            {isUserAPI && (
              <span className="text-xs px-1.5 py-0.5 bg-primary-100 text-primary-700 rounded font-medium">
                Custom
              </span>
            )}
          </div>
          <span className={`text-xs px-2 py-1 rounded-full font-medium ${categoryColor}`}>
            {api.category}
          </span>
        </div>
        <div className="flex items-center gap-2">
          {isActive ? (
            <CheckCircle className="w-4 h-4 text-green-500" title="Active" />
          ) : (
            <XCircle className="w-4 h-4 text-red-500" title="Inactive" />
          )}
          {isUserAPI && (
            <>
              <button
                onClick={() => onEdit(api)}
                className="p-1 hover:bg-blue-100 rounded transition-colors group"
                title="Edit API"
              >
                <Edit2 className="w-4 h-4 text-gray-400 group-hover:text-blue-600" />
              </button>
              <button
                onClick={() => onDelete(api.api_id, api.api_name)}
                className="p-1 hover:bg-red-100 rounded transition-colors group"
                title="Delete API"
              >
                <Trash2 className="w-4 h-4 text-gray-400 group-hover:text-red-600" />
              </button>
            </>
          )}
        </div>
      </div>
      
      <p className="text-xs text-gray-600 mb-2 line-clamp-2">
        {api.description}
      </p>
      
      {api.intent_keywords && api.intent_keywords.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-2">
          {api.intent_keywords.slice(0, 3).map((keyword, idx) => (
            <span
              key={idx}
              className="text-xs px-2 py-0.5 bg-white border border-gray-300 rounded-full text-gray-600"
            >
              {keyword}
            </span>
          ))}
          {api.intent_keywords.length > 3 && (
            <span className="text-xs text-gray-500">
              +{api.intent_keywords.length - 3}
            </span>
          )}
        </div>
      )}
    </div>
  );
};

export default Sidebar;
