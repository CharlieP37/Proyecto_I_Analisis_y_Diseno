import React, { useState } from 'react';
import './DragHold.css';
import img_Upload_File from '../../assets/img/Img_Import_Data.png'

export const DragHold = () => {
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);

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
    if (file && file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
      setFile(file);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
      setFile(file);
    }
  };

  const handleSubmit = async () => {
    if (file) {
      // Cambiar después para que jale la API
      console.log('Enviando archivo:', file);
    }
  };

  return (
    <>
      <div
        className={`drag-drop-container ${dragOver ? 'drag-over' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <img src={img_Upload_File} alt="Imagen de Carga de archivo" className='Img_Import_Data' />
        <input type="file" accept=".xlsx" onChange={handleFileSelect} style={{ display: 'none' }} />
        {file ? (
          <div className="file-preview">
            <p>Archivo seleccionado: {file.name}</p>
            <button className="submit-button" onClick={handleSubmit}>Enviar archivo</button>
          </div>
        ) : (
          <p className='Text-DragHold'>Selecciona el archivo de Excel que deseas importar para comenzar.</p>
        )}
      </div>
    </>
  );
};
