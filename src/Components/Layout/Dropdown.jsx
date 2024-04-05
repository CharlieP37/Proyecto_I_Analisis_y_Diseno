import React, { useState, useRef, useEffect } from 'react';
import './Dropdown.css';
import { Link } from 'react-router-dom';

const Dropdown = ({ defaultText, options, imageUrl }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
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
    <div ref={dropdownRef} className="dropdown">
      <div className="dropdown-header" onClick={toggleDropdown}>
        <img src={imageUrl} alt="Dropdown Icon" />
        <span>{defaultText}</span>
        <i className={`arrow ${isOpen ? 'up' : 'down'}`}></i>
      </div>
      {isOpen && (
        <div className="dropdown-body">
          {options.map((option, index) => (
            <div key={index} className="dropdown-item">
                <Link to={option.link} className='Option_Link'>
                    {option.imageUrl && <img src={option.imageUrl} alt="Option Icon" className='Img_Option_Icon'/>}
                    <span className='Text_Option'>{option.text}</span>
                </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dropdown;
