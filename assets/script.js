alert('Hi hello, Thank you to use me.')

var inputElt = document.getElementById('pile-no');
var btn = document.getElementById('button-1'); 
console.log(inputElt)

if(inputElt){
    inputElt.addEventListener("input", function(){
        btn.disabled = (this.value === '');
        })  
    }



    




