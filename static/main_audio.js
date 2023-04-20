let songSrc = document.getElementsByClassName('songSrc');
let play = document.getElementById('play');
let songList = document.querySelectorAll('.songSrc');
let track = document.getElementById('track');
let prev = document.getElementById('prev');
let volume = document.getElementById('volume');
let next = document.getElementById('forward');
let timer = document.getElementById('duration');
let currentTimer = document.getElementById('current-time');
let trackName = document.getElementById('track-name');
let timeSlider = document.getElementById('seek-slider');

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

let timeSecond = 0

function playAudio() {
    track.play()
    play.removeEventListener('click', playAudio)
    play.addEventListener('click', pauseAudio)
    countdown = setInterval(() => {
        timeSecond++
        seconds = Math.round(track.duration % 60)
        timer.textContent = Math.round(track.duration / 60) + ":" + seconds
        displayTime(timeSecond)
    }, 1000)
}

function displayTime(seconds) {
    sec = Math.floor(seconds % 60)
    min = Math.floor(seconds / 60)
    currentTimer.innerHTML = `${min<10 ? "0" : ""}${min}:${sec<10 ? "0" : ""}${sec}`
}


function pauseAudio() {
    track.pause()
    play.removeEventListener('click', pauseAudio)
    play.addEventListener('click', playAudio)
    clearInterval(countdown)
}

function playAgain() {
    track.currentTime = 0
    clearInterval(countdown)
    playAudio()
    timeSecond = 0
    displayTime(timeSecond)
}

function prevTrack() {
    timeRemainder = Math.round(track.duration % 60)
    timer.textContent = Math.round(track.duration / 60) + ":" + timeRemainder
    track.currentTime = 0
    songIndex -= 1
    track.src = songArray[songIndex]
    clearInterval(countdown)
    playAudio()
    timeSecond = 0
    displayTime(timeSecond)
}

function nextTrack() {
    timeRemainder = Math.round(track.duration % 60)
    timer.textContent = Math.round(track.duration / 60) + ":" + timeRemainder
    track.currentTime = 0
    songIndex += 1
    track.src = songArray[songIndex]
    clearInterval(countdown)
    playAudio()
    timeSecond = 0
    displayTime(timeSecond)
}

volume.addEventListener('input', (e) => {
    track.volume = e.currentTarget.value / 100
})

timeSlider.addEventListener('input', (e) => {
    track.duration = e.currentTarget.value
})