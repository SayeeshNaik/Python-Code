

function my(){

    axios.get('http://127.0.0.1:5000/demo')
    .then(response=>{
        console.log(response.data.gender)
        var gen=response.data.gender;
        var y='';
        for(var i=0; i<gen.length; i++)
         {
            y += '<input type=radio name=gg>' + gen[i] + '<br>';
            document.getElementById("a").innerHTML= y;
         }
    })
}