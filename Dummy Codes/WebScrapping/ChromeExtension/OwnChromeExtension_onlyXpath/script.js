document.addEventListener('click', handle,false);
document.addEventListener('click', clicked,false);
document.addEventListener('dblclick',removed,false)

function clicked(e){
    e = e || window.event;
    var target = e.target;
    if(target.className == 'txt' || target.className == 'outer txt'){
        target.style.background = 'transparent';
        target.style.border = 'none';
      }else{
        target.style.background = 'yellow';
        target.style.border = '2px solid red';
        target.style.color = 'black'
      }
}
function removed(e){
    e = e || window.event;
    var target = e.target;
    target.style.background = 'transparent';
    target.style.border = 'none';
}

var count = 0;

async function handle(e) {
    var dict = {}
    console.log('e = ',e)
    e = e || window.event;
    var target = e.target
    text = target.textContent || target.innerText;
    lis = ['tagName','title','id','className','type','name','value','alt','src','textContent']
    data = []
    var myPath = ''
        dict['baseUrl'] = window.location.href
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

    var xpath = '//'+target.tagName+myPath
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
    
    console.log(xpath)
    dict['XPath'] = xpath

    count += 1;
    console.log('Total clicked = ',count)

    //  if(dict['className']!='***'){
    //     var totalClasses = document.querySelectorAll("." + e.target.className).length
    //     console.log('new = ',document.querySelectorAll("." + e.target.className))
    //     console.log('Class Count = ',totalClasses)
    //     dict['CountOfClasses'] = totalClasses;
    //  }else{
    //     dict['CountOfClasses'] = totalClasses
    //  }

    fetch('http://127.0.0.1:5000/test',{method: "POST",body:JSON.stringify(
        { data : dict }
        )});
    
    var path = document.evaluate(`(${dict['XPath']})`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

    if( JSON.parse(localStorage.getItem('data')) != null ){
        var stored = JSON.parse(localStorage.getItem('data'));
        stored.push(dict)
        localStorage.setItem('data',JSON.stringify(stored))
        console.log('stored = ',stored)
    }
    else{
        dataLis = [];
        dataLis.push(dict);
        localStorage.setItem('data',JSON.stringify(dataLis))
        console.log('datalis = ',dataLis)
    }     
}

var btn = document.querySelector(".btnId");
btn.addEventListener("click",function (){
    document.querySelector(".view").style.background = "rgb(183, 255, 183)";
    chrome.storage.sync.get('data',(r)=>{
        console.log("ex = ",r )
        fetch('http://127.0.0.1:5000/test',{method: "POST",body:JSON.stringify(
            { data : 'sayeesh' }
            )});
        
        // window.open('https://docs.google.com/spreadsheets/d/1sIdi8q3G5NqL0YtRjlMabM5LNsizEEJdb8QxV5pJEiA/edit?usp=sharing')

    })   
    
})