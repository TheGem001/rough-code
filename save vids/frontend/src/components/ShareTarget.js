import React, { useEffect, useState } from 'react';

const ShareTarget = () => {
  const [status, setStatus] = useState('Initializing...');

  useEffect(() => {
    // Parse the shared URL from the GET request parameters
    const parsedUrl = new URL(window.location.href);
    const sharedUrl = parsedUrl.searchParams.get('url') || parsedUrl.searchParams.get('text');

    if (sharedUrl) {
      setStatus('Processing Video...');
      triggerDownload(sharedUrl);
    }
  }, []);

  const triggerDownload = async (videoUrl) => {
    try {
      // Send the link to the backend endpoint
      const response = await fetch(`/api/download?url=${encodeURIComponent(videoUrl)}`);
      if (response.ok) {
        const blob = await response.blob();
        const downloadLink = document.createElement('a');
        downloadLink.href = URL.createObjectURL(blob);
        downloadLink.download = 'video.mp4';
        downloadLink.click();
        setStatus('Download Started! Returning to feed...');
        // Close app or redirect after a delay to allow user to return to social media
        setTimeout(() => window.close(), 2000); 
      }
    } catch (error) {
      setStatus('Error processing video.');
    }
  };

  return (
    <div style={{ padding: '20px', textAlign: 'center', fontFamily: 'sans-serif' }}>
      <h2>{status}</h2>
      <p>Save Vids is handling your request in the background.</p>
    </div>
  );
};

export default ShareTarget;