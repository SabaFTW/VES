import React from 'react';

const Media = ({ file }) => {
  if (!file) {
    return <div>Select a media file to play.</div>;
  }

  const isVideo = file.endsWith('.mp4');
  const isAudio = file.endsWith('.mp3') || file.endsWith('.m4a');

  return (
    <div>
      {isVideo && (
        <video controls style={{ width: '100%' }}>
          <source src={`/files?path=${file}`} type="video/mp4" />
        </video>
      )}
      {isAudio && (
        <audio controls style={{ width: '100%' }}>
          <source src={`/files?path=${file}`} type="audio/mpeg" />
        </audio>
      )}
    </div>
  );
};

export default Media;
