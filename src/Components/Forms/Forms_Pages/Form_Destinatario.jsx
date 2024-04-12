import React from 'react'
import { DropDown_Form } from '../DropDown_Form/DropDown_Form'
import { InputForm } from '../Input_Form/Input_Form'
import { Button_Form } from '../Button_Form/Button_Form'

const options_country= [
  { text: 'Ecuador'},
  { text: 'Colombia'},
  { text: 'Costa Rica'},
  { text: 'El Salvador'},
  { text: 'Guatemala'},
  { text: 'Honduras'},
  { text: 'Nicaragua'},
  { text: 'Panamá'},
  { text: 'Selecciona un país'}
];

export const Form_Destinatario = () => {
  return (
    <>
      <article>
        <DropDown_Form mainTest='País' defaultText='Selecciona un país.' options={options_country} />
        <InputForm leftText='Compañia' placeholder='Ingrese la compañia' leftPadding="7px"/>
        <InputForm leftText='Vendedor' placeholder='Ingrese el vendedor' leftPadding="13px"/>
        <InputForm leftText='Estado' placeholder='Ingrese el estado' leftPadding="31px"/>
        <Button_Form backgroundColor='#1CCC1D' text='Exportar' hoverColor='#7ccf7c' link=''/>
      </article>
    </>
  )
}