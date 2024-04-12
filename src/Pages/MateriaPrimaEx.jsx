import React from 'react'
import { NavBar } from '../Components/Layout/NavBar'
import { MenuVar } from '../Components/Layout/MenuVar'
import { Contenedor_R } from '../Contenedores_R/Contenedor_R'
import img_top from '../assets/img/Img_Materia_Prima.png'
import { Form_Materia } from '../Components/Forms/Forms_Pages/Form_Materia'

export const MateriaPrimaEx = () => {

  return (
    <>
        <NavBar />
        <article style={{display: 'flex', gap: '4px'}}>
            <MenuVar />
            <Contenedor_R texto={'Exportar'} imagen={img_top} link_api="" Componente={<Form_Materia />}/>
        </article>
    </>
  )
}
