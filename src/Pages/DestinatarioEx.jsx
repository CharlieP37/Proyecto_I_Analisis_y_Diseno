import React from 'react'
import { NavBar } from '../Components/Layout/NavBar'
import { MenuVar } from '../Components/Layout/MenuVar'
import { Contenedor_R } from '../Contenedores_R/Contenedor_R'
import img_home from '../assets/img/Img_place.png'
import { Form_Destinatario } from '../Components/Forms/Forms_Pages/Form_Destinatario'

export const DestinatarioEx = () => {

  return (
    <>
        <NavBar />
        <article style={{display: 'flex', gap: '4px'}}>
            <MenuVar />
            <Contenedor_R texto={'Exportar'} imagen={img_home} link_api="" Componente={<Form_Destinatario />}/>
        </article>
    </>
  )
}
