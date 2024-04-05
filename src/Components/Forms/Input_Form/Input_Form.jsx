import React from 'react';
import './Input_Form'
import './Input_Form.css'

export const InputForm = ({leftText, placeholder}) => {
  return (
    <div className="input-container">
      <span className="left-text">{leftText}</span>
      <input
        type="text"
        className="input-field"
        placeholder={placeholder}
      />
    </div>
  );
};