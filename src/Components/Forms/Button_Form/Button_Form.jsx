import React from 'react';
import '../../Forms/Button_Form/Button_Form.css';

export const Button_Form = ({ backgroundColor, text, hoverOpacity, link }) => {
  const buttonStyle = {
    backgroundColor: backgroundColor,
  };

  const hoverStyle = {
    backgroundColor: backgroundColor, 
    opacity: hoverOpacity
  };

  return (
    <button className='Button_Main' style={buttonStyle}>
      <p>{text || 'Aceptar'}</p>
      <style>
        {`.Button_Main:hover {
          background-color: ${hoverStyle.backgroundColor};
          opacity: ${hoverStyle.opacity};
        }`}
      </style>
    </button>
  );
};
