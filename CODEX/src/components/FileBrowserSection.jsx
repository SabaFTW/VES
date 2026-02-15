import React, { useState, useEffect } from 'react';

const FileBrowserSection = ({ setActiveComponent, setActiveFile }) => {
  const [fileLists, setFileLists] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFileLists = async () => {
      try {
        const response = await fetch('/files');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setFileLists(data);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };
    fetchFileLists();
  }, []);

  const renderFileList = (categoryKey, files) => {
    if (!files || files.length === 0) {
      return null;
    }
    return (
      <ul style={{ listStyleType: 'none', paddingLeft: 10 }}>
        {files.map((file) => (
          <li key={file} style={{ marginBottom: 3, cursor: 'pointer' }} className="hover:text-teal-400">
            <a href="#" onClick={(e) => {
              e.preventDefault();
              setActiveFile(file); // Pass the selected file path
              let componentType = 'UNKNOWN';
              switch (categoryKey) {
                case 'MANUSCRIPTS':
                  componentType = 'MANUSCRIPTS';
                  break;
                case 'PORTALS':
                  componentType = 'PORTALS';
                  break;
                case 'MEDIA':
                  componentType = 'MEDIA';
                  break;
                case 'SEALS':
                  componentType = 'SEALS';
                  break;
                case 'SANDBOX':
                  componentType = 'SANDBOX';
                  break;
                default:
                  componentType = 'UNKNOWN';
              }
              setActiveComponent(componentType); // And set the active component type
            }}>
              {file.split('/').pop()}
            </a>
          </li>
        ))}
      </ul>
    );
  };

  if (loading) return <div className="loader"></div>;
  if (error) return <div className="text-red-500">Error: {error}</div>;

  return (
    <div className="text-sm">
      {Object.entries(fileLists).map(([categoryKey, files]) => (
        <div key={categoryKey} style={{ marginBottom: 15 }}>
          <h3 className="font-bold text-teal-300 mb-2">{categoryKey.replace(/_/g, ' ')}</h3>
          {renderFileList(categoryKey, files)}
        </div>
      ))}
    </div>
  );
};

export default FileBrowserSection;
