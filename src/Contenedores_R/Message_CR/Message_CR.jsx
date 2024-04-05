import React from 'react';
import '../../Contenedores_R/Message_CR/Message_CR.css'
import { Button_Form } from '../../Components/Forms/Button_Form/Button_Form';

export const Message_CR = ({ imgLink, text, bt_color, bt_text, hoverOpacity, link }) => {
  return (
    <div className='Content_CR'>
      <img src={imgLink} alt="Message Image" className='Img_Message' />
      <p>{text}</p>
      <Button_Form backgroundColor={bt_color} text={bt_text} hoverOpacity={hoverOpacity} link={link}/>
    </div>
  );
};
