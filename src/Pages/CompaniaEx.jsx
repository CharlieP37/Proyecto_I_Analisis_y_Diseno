import React from 'react'
import { NavBar } from '../Components/Layout/NavBar'
import { MenuVar } from '../Components/Layout/MenuVar'
import { Contenedor_R } from '../Contenedores_R/Contenedor_R'
import img_home from '../assets/img/icons8-business-building-96.png'
import { Form_Compania } from '../Components/Forms/Forms_Pages/Form_Compania'

export const CompaniaEx = () => {

  return (
    <>
        <NavBar />
        <article style={{display: 'flex', gap: '4px'}}>
            <MenuVar />
            <Contenedor_R texto={'Exportar'} imagen={img_home} link_api="" Componente={<Form_Compania />}/>
        </article>
    </>
  )
}
