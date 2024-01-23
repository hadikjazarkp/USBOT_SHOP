

  function imageZoom(imgID) {
    let img = document.getElementById(imgID);
    let lens = document.getElementById('lens');

    lens.style.backgroundImage = `url(${img.src})`;

    let ratio = 3;

    lens.style.backgroundSize = (img.width * ratio) + 'px ' + (img.height * ratio) + 'px ';


  img.addEventListener("mousemove", moveLens);
  lens.addEventListener("mousemove", moveLens);
  img.addEventListener("touchmove", moveLens);



    function moveLens(){

      //1  
      let pos = getCursor();
      console.log('pos:', pos);
      

      //2
      let positionleft = pos.x - (lens.offsetWidth / 2);
      let positionTop = pos.y - (lens.offsetHeight / 2);

      //3
      lens.style.left = positionleft + 'px';
      lens.style.top = positionTop + 'px';


      //4
      lens.style.backgroundPosition = "-" +(pos.x * ratio) +'px ' + (pos.y * ratio) +'px ';

    }

    function getCursor(){
      

        let e =window.event
        let bounds = img.getBoundingClientRect()
        
        //console.log('e:', e)
        //console.log('bounds:', bounds)

        let y = e.pageX - bounds.left;
        let x = e.pageY - bounds.left;
        return {'x':x, 'y':y}

    }

}

imageZoom('featured');


function imageZoom(imgID) {
    let img = document.getElementById(imgID);
    let lens = document.getElementById('lens');

    lens.style.backgroundImage = `url(${img.src})`;

    let ratio = 3;

    lens.style.backgroundSize = (img.width * ratio) + 'px ' + (img.height * ratio) + 'px';

    img.addEventListener("mousemove", moveLens);
    lens.addEventListener("mousemove", moveLens);
    img.addEventListener("touchmove", moveLens);

    function moveLens(e) {
      let pos = getCursorPos(e);

      // Adjustments to position calculations
      let positionLeft = pos.x - lens.offsetWidth / 2;
      let positionTop = pos.y - lens.offsetHeight / 2;

      lens.style.left = positionLeft + 'px';
      lens.style.top = positionTop + 'px';

      // Update backgroundPosition calculation
      lens.style.backgroundPosition = -positionLeft * ratio + 'px ' + -positionTop * ratio + 'px';
    }

    function getCursorPos(e) {
      e = e || window.event;
      let bounds = img.getBoundingClientRect();

      // Use clientX and clientY for mouse events
      let x = e.clientX - bounds.left;
      let y = e.clientY - bounds.top;
      
      // Use touches[0] for touch events
      if (e.touches && e.touches.length > 0) {
        x = e.touches[0].clientX - bounds.left;
        y = e.touches[0].clientY - bounds.top;
      }

      return { 'x': x, 'y': y };
    }
  }

  imageZoom('featured');
