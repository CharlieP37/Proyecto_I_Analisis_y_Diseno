import './MenuVar.css'
import React from 'react'
import Dropdown from './Dropdown.jsx'
import img_Materia_Prima from '../../assets/img/Img_Materia_Prima.png'
import img_Cliente from '../../assets/img/Img_Clientes.png'
import img_business from '../../assets/img/icons8-business-building-96.png'
import img_place from '../../assets/img/Img_place.png'
import img_Descarga from '../../assets/img/Img_Descarga.png'
import img_Export from '../../assets/img/Img_Export.png'

export function MenuVar () {
  
  
    const options_Materia_Prima = [
        { text: 'Importar', link: '/', imageUrl: img_Descarga },
        { text: 'Exportar', link: '/', imageUrl: img_Export },
    ];
    const options_Clientes = [
        { text: 'Importar', link: '/', imageUrl: img_Descarga },
        { text: 'Exportar', link: '/', imageUrl: img_Export },
    ];
    const options_Compania = [
        { text: 'Importar', link: '/', imageUrl: img_Descarga },
        { text: 'Exportar', link: '/', imageUrl: img_Export },
    ];
    const options_Destinatario = [
        { text: 'Importar', link: '/', imageUrl: img_Descarga },
        { text: 'Exportar', link: '/', imageUrl: img_Export },
    ];

  return(
      <article className="MenuArea">
          <article className='dropdown-container'>
              <Dropdown
                  defaultText="Materia prima"
                  options={options_Materia_Prima}
                  imageUrl= {img_Materia_Prima}
              />
          </article>
          <article className='dropdown-container'>
              <Dropdown
                  defaultText="Clientes"
                  options={options_Clientes}
                  imageUrl={img_Cliente}
              />
          </article>
          <article className='dropdown-container'>
              <Dropdown
                  defaultText="Compania"
                  options={options_Compania}
                  imageUrl={img_business}
              />
          </article>
          <article className='dropdown-container'>
              <Dropdown
                  defaultText="Destinatario"
                  options={options_Destinatario}
                  imageUrl={img_place}
              />
          </article>
      </article>
    )
}