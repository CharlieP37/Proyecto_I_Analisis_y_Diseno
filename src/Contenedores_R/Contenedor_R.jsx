import React from 'react'
import '../../src/Contenedores_R/Contenedor_R.css'

export const Contenedor_R = ({ texto, imagen, link_api, Componente  }) => {
  return (
    <>
      <article className='AreaContenedor_R'>
        <div className='Contenido_R'>
          <img className='img_Selected' src={imagen} alt="Imagen" style={{ width: '30px', height: '30px' }} />
          <p className='texto'>{texto}</p>
        </div>
        <article className='SeccionAccion'>
          {Componente}
        </article>
      </article>
    </>
  );
};