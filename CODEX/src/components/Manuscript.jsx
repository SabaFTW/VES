import React, { useState, useEffect } from 'react';
import { marked } from 'marked';

const Manuscript = ({ file }) => {
  const [content, setContent] = useState('');

  useEffect(() => {
    if (file) {
      fetch(`/files?path=${file}`)
        .then((response) => response.text())
        .then((text) => setContent(marked(text)));
    }
  }, [file]);

  if (!file) {
    return <div>Select a manuscript to read.</div>;
  }

  return <div dangerouslySetInnerHTML={{ __html: content }} />;
};

export default Manuscript;
