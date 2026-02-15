import React from 'react';

const Portal = ({ file }) => {
  if (!file) {
    return <div>Select a portal to view.</div>;
  }

  return (
    <iframe
      src={`/files?path=${file}`}
      style={{ width: '100%', height: '100%', border: 'none' }}
    />
  );
};

export default Portal;
