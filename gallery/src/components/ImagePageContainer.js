import React, {useState, useEffect} from 'react'
import axios from 'axios'

/*
Author: Anthony D'Alesandro

ImageViewer is a component that conditionally renders the children component.
If element != null then it will bring up a screen to view that element. Gives selection arrows and navigation.

expects element to be of format from a github api request.

TODO: 
- pass a render burger menu function. allows user to explain how to render the burger menu which is now very specific to the element passed.
- pass a function that tells the component how to access the image link from the element passed.
*/
function ImageViewer(props) {
  const { children, ...restProps } = props;

  const imageElement = props.element ? <SelectedImageContainer {...restProps} /> : props.children;
  return (
    <div>
      {imageElement}
    </div>
  );
}
 /*
  author: Anthony D'Alesandro
  
  BurgerMenu is exclusively used in SelectedImageContainer with the sole purposes of rendering meta data from the image element passed to it.
 */
function BurgerMenu(props) {
  const { imageElement } = props;

  const [file,setFile] = useState();
  useEffect(() => {
    const config = { responseType: 'blob' };
    axios.get(imageElement.download_url, config).then(res => {
      const file = new File([res.data], imageElement.name, {type: res.data.type});
      setFile(file);
    })
  }, [imageElement])

  return (
    <div className='burger-menu'>
      <a href={imageElement.html_url} target="_blank" rel="noreferrer">
        <h3> Image </h3>
      </a>
      <p>name: {imageElement.name}</p>
      <p>size: {imageElement.size}</p>
      { file && 
        <a href={URL.createObjectURL(file)} download>
          <p> Download </p>
        </a>
      }
    </div>
  )
}

/*
 author: Anthony D'Alesandro

 SelectedImageContainer renders an image on the full view port.

 TODO:
 - refactor burger menu to be its own self contained element. No need to have a useState for that element in this component.
*/
function SelectedImageContainer(props) {
  const { element, onUpdate, onExit} = props;
  const [burgerOpen, setBurgerOpen] = useState(false);
  return(
    <div className='selected-image-container'>
      <img src={element.download_url} alt=''/>
      <button className='exit-button button-hover ' onClick={onExit}/>
      <button className='next-button button-hover ' onClick={() => onUpdate(1)}/>
      <button className='previous-button button-hover ' onClick={() => onUpdate(-1)}/>
      <button className='open-burger-menu-button button-hover' onClick={() => setBurgerOpen(prev => !prev)}/>
      {burgerOpen && <BurgerMenu imageElement={element} /> }
    </div>
  )
}

export default ImageViewer