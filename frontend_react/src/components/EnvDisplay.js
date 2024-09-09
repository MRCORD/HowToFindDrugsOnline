import React from 'react';

const EnvDisplay = () => {
  return (
    <div style={{ 
      margin: '20px', 
      padding: '20px', 
      border: '1px solid #ccc',
      position: 'fixed',
      bottom: 0,
      right: 0,
      background: 'white',
      zIndex: 9999
    }}>
      <h2>Environment Variables:</h2>
      <pre>
        {JSON.stringify(
          {
            REACT_APP_API_URL: process.env.REACT_APP_API_URL,
            REACT_APP_GOOGLE_ANALYTICS_ID: process.env.REACT_APP_GOOGLE_ANALYTICS_ID,
            NODE_ENV: process.env.NODE_ENV,
          },
          null,
          2
        )}
      </pre>
    </div>
  );
};

export default EnvDisplay;