import React from 'react'
import { NavBar } from '../Components/Layout/NavBar'
import { MenuVar } from '../Components/Layout/MenuVar'
import { Contenedor_R } from '../Contenedores_R/Contenedor_R'
import img_home from '../assets/img/icons8-home-48.png'
import { Default_CR } from '../Contenedores_R/Default/Default_CR.jsx'

export const Layout = () => {

  return (
    <>
        <NavBar />
        <article style={{display: 'flex', gap: '4px'}}>
            <MenuVar />
            <Contenedor_R texto={''} imagen={img_home} link_api="" Componente={<Default_CR/>}/>
        </article>
    </>
  )
}