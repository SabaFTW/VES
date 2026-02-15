import React, { useState, useEffect } from 'react';
import api from '../services/api';

function Documents() {
  const [documents, setDocuments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      setIsLoading(true);
      const response = await api.getDocuments();
      setDocuments(response.data.documents);
    } catch (error) {
      console.error('Failed to load documents:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', file.name);
    formData.append('type', 'document');

    try {
      setUploading(true);
      await api.uploadDocument(formData);
      await loadDocuments();
    } catch (error) {
      console.error('Upload failed:', error);
      alert(`Upload failed: ${error.response?.data?.error || error.message}`);
    } finally {
      setUploading(false);
    }
  };

  const deleteDocument = async (id) => {
    if (!window.confirm('Delete this document?')) return;

    try {
      await api.deleteDocument(id);
      await loadDocuments();
    } catch (error) {
      console.error('Delete failed:', error);
      alert(`Delete failed: ${error.response?.data?.error || error.message}`);
    }
  };

  return (
    <div className="documents-container">
      <div className="documents-header">
        <h2>📄 Document Vault</h2>
        <label className="btn-primary" style={{ cursor: 'pointer' }}>
          {uploading ? 'Uploading...' : '+ Upload'}
          <input
            type="file"
            onChange={handleUpload}
            style={{ display: 'none' }}
            disabled={uploading}
            accept=".pdf,.txt,.md,.json,.png,.jpg,.jpeg,.gif"
          />
        </label>
      </div>

      {isLoading ? (
        <div className="loading">Loading documents...</div>
      ) : documents.length === 0 ? (
        <div className="empty-state">
          <p>No documents yet</p>
          <p className="hint">Upload research notes, PDFs, images, or text files</p>
        </div>
      ) : (
        <div className="documents-grid">
          {documents.map(doc => (
            <div key={doc.id} className="document-card">
              <div className="document-icon">
                {doc.type === 'image' ? '🖼️' : '📄'}
              </div>
              <div className="document-info">
                <div className="document-name">{doc.name}</div>
                <div className="document-meta">
                  <span>{doc.type}</span>
                  <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                </div>
              </div>
              <button
                onClick={() => deleteDocument(doc.id)}
                className="btn-danger-small"
              >
                🗑️
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Documents;
