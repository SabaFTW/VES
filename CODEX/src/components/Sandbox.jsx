import React, { useState, useEffect } from 'react';

const Sandbox = ({ file }) => {
  const [content, setContent] = useState('');

  useEffect(() => {
    if (file) {
      fetch(`/files?path=${file}`)
        .then((response) => response.text())
        .then((text) => setContent(text));
    }
  }, [file]);

  if (!file) {
    return <div>Select a file to view from the sandbox.</div>;
  }

  return <pre>{content}</pre>;
};

export default Sandbox;
