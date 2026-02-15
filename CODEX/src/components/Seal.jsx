import React from 'react';

const Seal = ({ file }) => {
  if (!file) {
    return <div>Select a seal to view.</div>;
  }

  return (
    <iframe
      src={`/files?path=${file}`}
      style={{ width: '100%', height: '100%', border: 'none' }}
    />
  );
};

export default Seal;
