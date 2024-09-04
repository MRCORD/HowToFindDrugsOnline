import React from 'react';
import { TypeAnimation } from 'react-type-animation';
import config from '../config';

const TypewriterText = ({ text, onComplete }) => {
  return (
    <TypeAnimation
      sequence={[
        text,
        1000,
        () => {
          if (onComplete) onComplete();
        },
      ]}
      wrapper="span"
      cursor={true}
      repeat={0}
      speed={config.typingSpeed}
      style={{ display: 'inline-block' }}
    />
  );
};

export default TypewriterText;