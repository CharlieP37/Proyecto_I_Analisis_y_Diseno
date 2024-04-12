import React from 'react'
import { NavBar } from '../Components/Layout/NavBar'
import { MenuVar } from '../Components/Layout/MenuVar'
import { Contenedor_R } from '../Contenedores_R/Contenedor_R'
import img_home from '../assets/img/icons8-business-building-96.png'
import { DragHold } from '../Components/DragHold/DragHold.jsx'

export const CompaniaImp = () => {

  return (
    <>
        <NavBar />
        <article style={{display: 'flex', gap: '4px'}}>
            <MenuVar />
            <Contenedor_R texto={'Importar'} imagen={img_home} link_api="" Componente={<DragHold />} />
        </article>
    </>
  )
}
