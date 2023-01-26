const socket = io(window.origin  + '/room')
           
socket.emit('room_request')



socket.on('room_response', res =>{
    console.log(sessionStorage.length)
    for(let data in res){
        if (res[data]['clientId'] === socket.id){
            if(res[data]['clientName'].split(' ')[1] === '(host)'){
                $('.item-container').fadeIn()
                sessionStorage.setItem('host',res[data]['clientName'])
                $('.srt-btn').css('pointer-events', 'visible')
                $('.srt-btn').css('cursor', 'not-allowed')
                console.log(sessionStorage.length)
                break
        }
        }

    }
})

let setItems = []
document.addEventListener('keydown', (e)=>{
    if(e.keyCode === 13){
        const itemValue = document.getElementById('input-item')
        const itemContainer = document.getElementById('items')

        $(itemContainer).append(`<div class="item">${itemValue.value}</div>`)
        setItems.push(itemValue.value)

        itemValue.value = ''
    }
})

let roomName = document.getElementById('roomName').innerText.toLowerCase()
const set_btn = () =>{
    console.log(setItems.length)
    if(setItems.length % 2 == 0 && setItems.length !== 0) {
        socket.emit('set_items', setItems, roomName)
    }else{
        alert("The items must be 'EVEN' is size.")
    }
    
}   

socket.on('load_items', res =>{
    $('.main-header').fadeOut()
    $('.item-container').fadeOut('fast', ()=>{
        $('.sorter').slideDown(()=>{
            for(data of res){
                load_item(data)
            }
        })
    })

})


const load_item = (item) =>{
    $("ul").append(`<li class="item-sort" draggable="true"><span><i class="fa fa-trash"></i></span>${item}</li>`);
}


let playerSet = []
const send_btn = () =>{
    const items = document.querySelectorAll('.item-sort')
    items.forEach((elem,index) => {
        playerSet.push([elem.innerText,(items.length-index)])
    });
    socket.emit('prepare_set', playerSet, roomName)
    $('.sorter').fadeOut()
    $('.loading-wrapper').css('display', 'flex')
}

socket.on('btn_activator', data =>{
    if (sessionStorage.length == 0){
        $('.srt-btn').css('pointer-events', 'visible')
        $('.srt-btn').css('cursor', 'not-allowed')
    }
})

socket.on('pre_sets', res =>{
    let playerData = {player1: playerSet}
    if(res['id'] !== socket.id){
        playerData['player2'] = res['data']
    }
    if(Object.keys(playerData).length == 2){
        al_request(playerData)
    }
    
})

socket.on('backup', data =>{
    if (sessionStorage.length == 0){
        $('.loading-wrapper').fadeOut()
        $('.result-container').css('display','flex')
        resultLoader(data, 1)
    }
    
})

const al_request = (data) =>{
    axios.post('http://127.0.0.1:3000/alProcedure',data)
    .then(res => {
         $('.loading-wrapper').fadeOut()
         $('.result-container').css('display','flex')
         resultLoader(res.data, 0)
         console.log(res.data)
         socket.emit('backup_loader', res.data, roomName)
    }).catch(err => console.log(err))
}


const resultLoader = (data, index) =>{
    for(let list of data[index]){
        $('.rsub-container').append(`<div class="result-item">${list[0]}</div>`)
    }
}


const returnHome = () =>{
    window.location.href = `${window.origin}/`
}