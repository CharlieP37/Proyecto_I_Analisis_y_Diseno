import React from 'react'
import { NavBar } from '../Components/Layout/NavBar'
import { MenuVar } from '../Components/Layout/MenuVar'
import { Contenedor_R } from '../Contenedores_R/Contenedor_R'
import img_home from '../assets/img/Img_Clientes.png'
import { Form_Clientes } from '../Components/Forms/Forms_Pages/Form_Clientes'


export const ClientesEx = () => {

  return (
    <>
        <NavBar />
        <article style={{display: 'flex', gap: '4px'}}>
            <MenuVar />
            <Contenedor_R texto={'Exportar'} imagen={img_home} link_api="" Componente={<Form_Clientes />}/>
        </article>
    </>
  )
}
