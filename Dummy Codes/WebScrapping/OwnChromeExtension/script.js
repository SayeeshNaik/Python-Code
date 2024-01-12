var nextButtonEnable = false

document.addEventListener('DOMContentLoaded',function (){
    if(window.storage_status==true){
        localStorage.clear()
    }
})

document.addEventListener('click',function() {
    window.name = 'sayeesh'
})

async function main(e){
    e = e || window.event;
    var target = e.target;
    var resData = await fetch('http://127.0.0.1:5000/toggle_getting')
    .then(response => response.json())
    .then(data =>{
    
        if(data.toggle_status == 'true' && data.toggle_status!="false"){
        document.addEventListener('click', handle,false);
        document.addEventListener('click', clicked,false);
        document.addEventListener('dblclick',removed,false);
        document.addEventListener('mouseover',hover_func,false);
        document.addEventListener('mouseout',nonHover_func,false); 
        }else
        {
        document.removeEventListener('click',handle);
        document.removeEventListener('click', clicked);
        document.removeEventListener('dblclick',removed);
        document.removeEventListener('mouseover',hover_func);
        }
    }).catch((error)=>{
        document.removeEventListener('click',handle);
        document.removeEventListener('click', clicked);
        document.removeEventListener('dblclick',removed);
        document.removeEventListener('mouseover',hover_func);
    });
}

document.addEventListener('pointerenter',main,false)

function hover_func(e){
    e = e || window.event;
    var target = e.target;
    if(target.offsetParent.className == 'all-my-html'){
        target.style.outline = 'none';
      }else{
        target.style.outline = 'solid green';
        target.style.background = 'orrange'
    }
}

function nonHover_func(e){
    e = e || window.event;
    var target = e.target;
    target.style.outline = 'none';
}

function clicked(e){
    e = e || window.event;
    var target = e.target;
    if(target.offsetParent.className == 'all-my-html'){
        if(target.id == 'switch' || target.className == 'toggle_css'){
            target.style.outline = 'none'
        }else{
            target.style.outline = 'none';
            target.style.background = 'none';
            target.style.color = 'none';
        }
      }else{
        target.style.background = 'yellow';
        target.style.border = '2px solid red';
        target.style.color = 'black';
      }
}
function removed(e){
    e = e || window.event;
    var target = e.target;
    target.style = null
}

var count = 0;
async function handle(e) {
    var dict = {}
    console.log('e = ',e)
    e = e || window.event;
    var target = e.target;
    text = target.textContent || target.innerText;
    lis = ['tagName','title','id','className','type','name','value','alt','src','textContent']
    data = []
    var myPath = ''
        dict['baseUrl'] = window.location.href;
    
    for(let i=0;i<lis.length;i++){
        try{
            dict[lis[i]] = target[lis[i]]
            if(target[lis[i]]===''||target[lis[i]]===null||target[lis[i]]===undefined){
                dict[lis[i]] = "***"
            }
        } catch{}
    }

    var arr = Object.keys(dict)
    var remove_lis = ['baseUrl','tagName','textContent','alt',]
    arr = arr.filter(function(item) {
        return !remove_lis.includes(item)
        
    })
    for(let i in arr){
        if(dict[arr[i]]!='***'){
            if(arr[i]=='className'){
                myPath += '[(@class' + "=" + "'" + dict[arr[i]] + "'" + ')]'
            }
            // else if(dict['id']!='***'){
            //     myPath += '[(@id' + "=" + "'" + dict['id'] + "'" + ')]'
            // }
            // else {
            //     myPath += '[(@'+arr[i] + "=" +"'" +dict[arr[i]]+"'"+')]'
            // }    

        }
    }

    var parentTagName = target.offsetParent.tagName
    var parentClassName = target.offsetParent.className
    var parentXpath = "//" + parentTagName + "[(@class='" + parentClassName + "')]";

    if(target.className!=''){
        var xpath = '//'+target.tagName + myPath
    }else{
        var parentTagName = target.parentElement.tagName
        var parentClassName = target.parentElement.className
        var xpath = "//" + parentTagName + "[(@class='" + parentClassName + "')]"
    }
    
    // if(target.tagName=='IMG'){
    //     xpath = '//IMG[(@src' + "=" +"'" + target.src + "'" + ')]'
    // }

    // if(target.id!=''){
    //     xpath = '//' + target.tagName + '[(@id=' + "'" + target.id + "'" + ')]'
    // }
    if(target.tagName=='A'){
        if(target.title!=''){
            xpath = '//A[(@title=' + "'" + target.title + "'" + ')]'
        }else{
            xpath = ''
        }            
    }
    if(xpath==parentXpath){
        var newClassName = target.offsetParent.children[0].className
        var xpath = '//' + target.offsetParent.children[0].tagName + '[(@class=' + "'" + newClassName + "'" + ')]'
    }
    console.log('NewClassName = ',newClassName)
    console.log('Parent = ',parentXpath)
    console.log('Xpath = ',xpath)

    dict['parentXpath'] = parentXpath;
    dict['XPath'] = xpath;

    count += 1;
    console.log('Total clicked = ',count)
    
    localStorage.setItem('data',JSON.stringify(dict))

    if(target.className != "txt" && target.id !='myId' && target.id != 'switch' && target.className != 'btnId' && target.className != 'view txt' && target.id != 'tg' && target.id != 'myId' && target.className != 'outer txt' && target.className != 'toggleDiv' && target.className != 'nextbtn' && target.id != 'next-pencil'){
        fetch('http://127.0.0.1:5000/test',{ method: "POST",body: JSON.stringify(
        { data : dict }
        )}).then(res=>res.json().then(resData=>{
            console.log("Test Api = ",resData.data)
            if(resData.data == true){
                fetch('http://127.0.0.1:5000/test?next_button_input=true')
            }
        }));
    }
    
    var path = document.evaluate(`(${dict['XPath']})`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;



    if( JSON.parse(localStorage.getItem('data')) != null ){
        var stored = JSON.parse(localStorage.getItem('data'));
        stored.push(dict)
        localStorage.setItem('data',JSON.stringify(stored))
    }
    else{
        dataLis = [];
        dataLis.push(dict);
        localStorage.setItem('data',JSON.stringify(dataLis))
        console.log('datalis = ',dataLis)
    }     

    var parentTagName = target.offsetParent.tagName
    var parentClassName = target.offsetParent.className
    var p = "//" + parentTagName + "[(@class='" + parentClassName + "')]" + xpath 
    console.log('new path = ',p)
   
}


var btn = document.querySelector(".btnId");
btn.addEventListener("click",function (){
    window.storage_status = true
    document.querySelector(".view").style.background = "rgb(183, 255, 183)";
    chrome.storage.sync.get('data',(r)=>{
        console.log("ex = ",r )

    fetch('http://127.0.0.1:5000/google_sheet').then(
        (res)=>res.json().then(
          (resData)=>window.open(resData.sheet_url)
        ))
    fetch('http://127.0.0.1:5000/next_button?next_button_status=false')

    })   

    document.querySelector(".btnId").disabled = true;
    document.querySelector(".btnDownload").disabled = false;
    
//    var data = ({name:'sayeesh'})
//    const blob = new Blob([s2ab(atob(data))],{type:''});
//    const href = URL.createObjectURL(blob);
//    const a = Object.assign(document.createElement("a"),{
//     href,
//     download: 'data.xlsx',
//    });
//    document.body.append(a);
//    a.click();
//    URL.revokeObjectURL(href);
//    a.remove();

filename='reports.xlsx'; 
       
        var ws = XLSX.utils.json_to_sheet({'name':'sayeesh'}); 
        var wb = XLSX.utils.book_new(); 
        XLSX.utils.book_append_sheet(wb, ws, "People"); 
        XLSX.writeFile(wb,filename); 

})

var bx = document.getElementById('switch');

bx.addEventListener('click',async function(){
    var c = document.getElementById('switch');
    var txt = document.getElementById('tg');
    if(c.checked){
        localStorage.setItem('toggleChecked','true')
        toggleStatus = true;
        txt.innerHTML = "ON"
    }else{
        localStorage.setItem('toggleChecked','false')
        toggleStatus = false;
        txt.innerHTML = "OFF"
    }
    await fetch('http://127.0.0.1:5000/toggle?toggle_status='+toggleStatus).then(
        (res)=>res.json().then(
            (resData)=>{
                c.disabled = false
                console.log('res togle = ',resData.toggle_status)
            }
          )
       ).catch((error)=>{
            localStorage.setItem('toggleChecked','false')
            toggleStatus = false;
            txt.innerHTML = "OFF"
            c.disabled = true
       })

    if(localStorage.getItem('toggleChecked')=='true'){
       c.checked = true  
    }else{
       c.checked = false
    }

    main()
});

if(localStorage.getItem('toggleChecked')=='true'){
    document.getElementById('switch').checked = true;
    document.getElementById('tg').innerHTML = "ON"
}else{
    document.getElementById('switch').checked = false;
    document.getElementById('tg').innerHTML = "OFF"
}

var next_button_xpath_text = document.getElementById('nextBtnXpath');
try{
    fetch('http://127.0.0.1:5000/getxpath').then(res=>res.json().then(
        resData=>{
            var next_xpath = resData.out.XPath;
            next_button_xpath_text.value = next_xpath;
        }
    ))
    fetch('http://127.0.0.1:5000/next_button?default=false')
}catch{ }

localStorage.setItem('next_button',false)
var nextButton = document.getElementById('next-pencil');
nextButton.addEventListener('click',function(){        
        fetch('http://127.0.0.1:5000/next_button').then(res=>res.json().then(
        resData=>{
            if(resData.next_button_status==true){
                nextButton.style.color = 'blue';
                next_button_input.disabled = true
                localStorage.setItem('next_button',true)
            }else{
                nextButton.style.color = 'black';
                next_button_input.disabled = true
                localStorage.setItem('next_button',false)
            }
        }
    ))

})

