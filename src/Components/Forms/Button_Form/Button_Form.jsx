import React from 'react';
import '../../Forms/Button_Form/Button_Form.css';

export const Button_Form = ({ backgroundColor, hoverColor, text, link }) => {
  const buttonStyle = {
    backgroundColor: backgroundColor,
  };

  const hoverStyle = {
    backgroundColor: hoverColor
  };

  return (
    <article className='Container'>
      <button className='Button_Main' style={buttonStyle}>
        <p>{text || 'Aceptar'}</p>
        <style>
          {`.Button_Main:hover {
            background-color: ${hoverStyle.backgroundColor};
          }`}
        </style>
      </button>
    </article>
  );
};
