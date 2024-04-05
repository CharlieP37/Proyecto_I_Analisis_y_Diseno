import './NavBar.css'
import React from 'react';
import Img_Cambiagro_Negative_Green from '../../assets/img/Cambiagro_Negative_Green.png'

export function NavBar () {
    return(
        <article className='navbar'>
           <img src={Img_Cambiagro_Negative_Green} alt="Cambiagro Logo" className='img_logo' />
        </article>
    )
}