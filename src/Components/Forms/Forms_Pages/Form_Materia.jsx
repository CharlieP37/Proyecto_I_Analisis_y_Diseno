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

const options_state = [
  { text: 'Activo'},
  { text: 'Desactivo'}
];

export const Form_Materia = () => {
  return (
    <>
      <article>
        <DropDown_Form mainTest='País' defaultText='Selecciona un país.' options={options_country} />
        <InputForm leftText='Bodega' placeholder='Ingrese la bodega' leftPadding="25px"/>
        <InputForm leftText='Categoria' placeholder='Ingrese la categoria' leftPadding="13px"/>
        <DropDown_Form mainTest='Estado' defaultText='Seleccionar un estado' options={options_state} />
        <InputForm leftText='Sector' placeholder='Ingrese el sector' leftPadding="38px"/>
        <Button_Form backgroundColor='#1CCC1D' text='Exportar' hoverColor='#7ccf7c' link=''/>
      </article>
    </>
  )
}
