let songSrc = document.getElementsByClassName('songSrc');
let play = document.getElementById('play');
let songList = document.querySelectorAll('.songSrc');
let track = document.getElementById('track');
let prev = document.getElementById('prev');
let volume = document.getElementById('volume');
let next = document.getElementById('forward');


play.addEventListener('click', playAudio)
prev.addEventListener('click', playAgain)
next.addEventListener('click', nextTrack)
prev.addEventListener('dblclick', prevTrack)

let songArray = [];
let songIndex = 0

songList.forEach(song => {
    songArray.push("data:audio/wav;charset=utf-8;base64," + song.value)
})

function setSong() {
    track.src = songArray[0]
}
setSong()

function playAudio() {
    track.play()
    console.log(songArray.indexOf('track.src'))
    play.removeEventListener('click', playAudio)
    play.addEventListener('click', pauseAudio)
}

function pauseAudio() {
    track.pause()
    play.removeEventListener('click', pauseAudio)
    play.addEventListener('click', playAudio)
}

function playAgain() {
    track.currentTime = 0
    track.play()
}

function prevTrack() {
    track.currentTime = 0
    songIndex -= 1
    track.src = songArray[songIndex]
    track.play()
}

function nextTrack() {
    track.currentTime = 0
    songIndex += 1
    track.src = songArray[songIndex]
    track.play()
}

volume.addEventListener('input', (e) => {
    track.volume = e.currentTarget.value / 100
})