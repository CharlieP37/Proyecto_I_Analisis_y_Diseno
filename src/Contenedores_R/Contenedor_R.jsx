import React from 'react'
import '../../src/Contenedores_R/Contenedor_R.css'
import { DragHold } from '../Components/DragHold/DragHold.jsx'

export const Contenedor_R = ({ texto, imagen }) => {
  return (
    <>
      <article className='AreaContenedor_R'>
        <div className='Contenido_R'>
          <img className='img_Selected' src={imagen} alt="Imagen" style={{ width: '30px', height: '30px' }}/>
          <p className='texto'>{texto}</p>
        </div>
        <article className='variable_Area'>
          <DragHold />
        </article>
      </article>
    </>
  );
};
