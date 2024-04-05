import React, { useState, useRef, useEffect } from 'react';
import '../DropDown_Form/DropDown_Form.css'; 

export const DropDown_Form = ({ mainTest, defaultText, options }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null);
  const dropdownRef = useRef(null);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleOptionClick = (option) => {
    setSelectedOption(option); 
    setIsOpen(false); 
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [dropdownRef]);

  return (
    <div className="new-dropdown-container"> 
      <p className='MainText'>{mainTest}</p>
      <div ref={dropdownRef} className="new-dropdown"> 
        <div className="new-dropdown-header" onClick={toggleDropdown}> 
          <span>{selectedOption ? selectedOption.text : defaultText}</span>
          <i className={`new-arrow ${isOpen ? 'up' : 'down'}`}></i>
          <i className={`arrow-right ${isOpen ? 'open' : 'closed'}`}></i>
        </div>
        {isOpen && (
          <div className="new-dropdown-body"> 
            {options.map((option, index) => (
              <div 
                key={index} 
                className={`new-dropdown-item ${selectedOption === option ? 'selected' : ''}`} 
                onClick={() => handleOptionClick(option)} 
              > 
                <span className='NewText_Option'>{option.text}</span> 
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
