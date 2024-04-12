import React, { useState, useRef } from 'react';
import axios from 'axios';
import './DragHold.css';
import img_Upload_File from '../../assets/img/Img_Import_Data.png';

export const DragHold = ({ link_api }) => {
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const dropAreaRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    handleFileSelect(file);
  };

  const handleFileSelect = (file) => {
    if (file && file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
      setFile(file);
    }
  };

  const handleButtonClick = () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.xlsx';
    fileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      handleFileSelect(file);
    });
    fileInput.click();
  };

  const handleDropAreaClick = () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.xlsx';
    fileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      handleFileSelect(file);
    });
    fileInput.click();
  };

  const handleSubmit = async () => {
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      try {
        const response = await axios.post(link_api, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        window.alert('Data correctamente guardada');
      } catch (error) {
        window.alert('Error al enviar el archivo');
      }
    }
  };

  return (
    <>
      <div
        ref={dropAreaRef}
        className={`drag-drop-container ${dragOver ? 'drag-over' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={(e) => {
          if (e.target === dropAreaRef.current) {
            handleDropAreaClick();
          }
        }}
      >
        <img src={img_Upload_File} alt="Imagen de Carga de archivo" className="Img_Import_Data" />
        {file ? (
          <div className="file-preview">
            <p>Archivo seleccionado: {file.name}</p>
            <button className="submit-button" onClick={handleSubmit}>
              Enviar archivo
            </button>
          </div>
        ) : (
          <p className="Text-DragHold">Selecciona el archivo de Excel que deseas importar para comenzar.</p>
        )}
      </div>
    </>
  );
};