import React, { useState, useEffect } from 'react';
import api from '../services/api';

function Anchors() {
  const [anchors, setAnchors] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [newAnchor, setNewAnchor] = useState({
    type: 'sigil',
    name: '',
    data: ''
  });

  useEffect(() => {
    loadAnchors();
  }, []);

  const loadAnchors = async () => {
    try {
      setIsLoading(true);
      const response = await api.getAnchors();
      setAnchors(response.data.anchors);
    } catch (error) {
      console.error('Failed to load anchors:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const createAnchor = async (e) => {
    e.preventDefault();

    try {
      await api.createAnchor(newAnchor);
      setNewAnchor({ type: 'sigil', name: '', data: '' });
      setShowForm(false);
      await loadAnchors();
    } catch (error) {
      console.error('Failed to create anchor:', error);
      alert(`Failed to create anchor: ${error.response?.data?.error || error.message}`);
    }
  };

  const deleteAnchor = async (id) => {
    if (!window.confirm('Delete this anchor?')) return;

    try {
      await api.deleteAnchor(id);
      await loadAnchors();
    } catch (error) {
      console.error('Delete failed:', error);
      alert(`Delete failed: ${error.response?.data?.error || error.message}`);
    }
  };

  const getAnchorIcon = (type) => {
    switch (type) {
      case 'sigil': return '🜂';
      case 'qr': return '📱';
      case 'project': return '🗂️';
      default: return '⚓';
    }
  };

  return (
    <div className="anchors-container">
      <div className="anchors-header">
        <h2>⚓ Anchors & Sigils</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn-primary"
        >
          {showForm ? 'Cancel' : '+ New Anchor'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={createAnchor} className="anchor-form">
          <div className="form-group">
            <label>Type:</label>
            <select
              value={newAnchor.type}
              onChange={(e) => setNewAnchor({ ...newAnchor, type: e.target.value })}
              className="form-select"
            >
              <option value="sigil">🜂 Sigil</option>
              <option value="qr">📱 QR Code</option>
              <option value="project">🗂️ Project</option>
            </select>
          </div>

          <div className="form-group">
            <label>Name:</label>
            <input
              type="text"
              value={newAnchor.name}
              onChange={(e) => setNewAnchor({ ...newAnchor, name: e.target.value })}
              className="form-input"
              placeholder="Anchor name..."
              required
            />
          </div>

          <div className="form-group">
            <label>Data / Description:</label>
            <textarea
              value={newAnchor.data}
              onChange={(e) => setNewAnchor({ ...newAnchor, data: e.target.value })}
              className="form-textarea"
              placeholder="Anchor data, description, or metadata..."
              rows={4}
            />
          </div>

          <button type="submit" className="btn-primary">
            Create Anchor
          </button>
        </form>
      )}

      {isLoading ? (
        <div className="loading">Loading anchors...</div>
      ) : anchors.length === 0 ? (
        <div className="empty-state">
          <p>No anchors yet</p>
          <p className="hint">Create sigils, QR codes, or project anchors</p>
        </div>
      ) : (
        <div className="anchors-grid">
          {anchors.map(anchor => (
            <div key={anchor.id} className="anchor-card">
              <div className="anchor-icon">
                {getAnchorIcon(anchor.type)}
              </div>
              <div className="anchor-info">
                <div className="anchor-name">{anchor.name}</div>
                <div className="anchor-type">{anchor.type}</div>
                {anchor.data && (
                  <div className="anchor-data">{anchor.data.substring(0, 100)}</div>
                )}
                <div className="anchor-meta">
                  {new Date(anchor.created_at).toLocaleDateString()}
                </div>
              </div>
              <button
                onClick={() => deleteAnchor(anchor.id)}
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

export default Anchors;
