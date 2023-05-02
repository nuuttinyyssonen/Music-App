let songSrc = document.getElementsByClassName('songSrc');
let play = document.getElementById('play');
let track = document.getElementById('track');
let prev = document.getElementById('prev');
let volume = document.getElementById('volume');
let next = document.getElementById('forward');
let timer = document.getElementById('duration');
let currentTimer = document.getElementById('current-time');
let trackName = document.getElementById('track-name');
let timeSlider = document.getElementById('seek-slider');
let playBtn = document.getElementById('playBtn');

let songNameList = document.querySelectorAll('.songNames');
let artistNameList = document.querySelectorAll('.artistNames');
let albumList = document.querySelectorAll('.albumCover');
let songList = document.querySelectorAll('.songSrc');
let searchPlayButtons = document.querySelectorAll('.searchPlay');
let songLength = document.querySelectorAll('.songLength');

let playingPic = document.getElementById('playing-pic');

let currentTrackName = document.getElementById('track-name');
let currentArtistName = document.getElementById('artist-name');

let searchAlbum = document.querySelectorAll('.searchAlbum');


play.addEventListener('click', playAudio)
prev.addEventListener('click', playAgain)
next.addEventListener('click', nextTrack)
prev.addEventListener('dblclick', prevTrack)

let songArray = [];
let imgArray = [];
let searchImgArray = [];
let songNameArray = [];
let artistNameArray = [];
let buttonArray = [];
let songIndex = 0;

searchAlbum.forEach(img => {
    searchImgArray.push(img)
})

songLength.forEach(song => {
    song.textContent = track.duration
})

searchPlayButtons.forEach(button => {
    buttonArray.push(button)
    button.addEventListener('click', () => {
        songIndex = buttonArray.indexOf(button)
        track.src = songArray[songIndex]
        playingPic.src = searchImgArray[songIndex].currentSrc
        currentTrackName.textContent = songNameArray[songIndex].defaultValue
        currentArtistName.textContent = artistNameArray[songIndex].defaultValue
        playAudio()
    })
})

albumList.forEach(album => {
    imgArray.push(album)
    album.addEventListener('click', () => {
        songIndex = imgArray.indexOf(album)
        track.src = songArray[songIndex]
        playingPic.src = imgArray[songIndex].currentSrc
        currentTrackName.textContent = songNameArray[songIndex].defaultValue
        currentArtistName.textContent = artistNameArray[songIndex].defaultValue
        console.log(songNameArray)
        playAudio()
    })
})

songNameList.forEach(song => {
    songNameArray.push(song)
})

artistNameList.forEach(artist => {
    artistNameArray.push(artist)
})

songList.forEach(song => {
    songArray.push("data:audio/wav;charset=utf-8;base64," + song.value)
})

let timeSecond = 0

function playAudio() {
    track.play()
    playBtn.className = "fa fa-pause-circle"
    play.removeEventListener('click', playAudio)
    play.addEventListener('click', pauseAudio)
    countdown = setInterval(() => {
        timeSecond++
        seconds = Math.round(track.duration % 60)
        timer.textContent = Math.round(track.duration / 60) + ":" + seconds
        displayTime(track.currentTime)
    }, 1000)
}

function displayTime(seconds) {
    sec = Math.floor(seconds % 60)
    min = Math.floor(seconds / 60)
    currentTimer.innerHTML = `${min}:${sec<10 ? "0" : ""}${sec}`
}


function pauseAudio() {
    track.pause()
    playBtn.className = "fa fa-play-circle"
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
    playingPic.src = imgArray[songIndex].currentSrc
    currentTrackName.textContent = songNameArray[songIndex].defaultValue
    currentArtistName.textContent = artistNameArray[songIndex].defaultValue
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
    playingPic.src = imgArray[songIndex].currentSrc
    currentTrackName.textContent = songNameArray[songIndex].defaultValue
    currentArtistName.textContent = artistNameArray[songIndex].defaultValue
    clearInterval(countdown)
    playAudio()
    timeSecond = 0
    displayTime(timeSecond)
}

volume.addEventListener('input', (e) => {
    track.volume = e.currentTarget.value / 100
})


if(track.play()) {
    setInterval(() => {
        timeSlider.max = track.duration
        timeSlider.value = track.currentTime
    },1000)
}

timeSlider.onchange = (() => {
    track.play();
    track.currentTime = timeSlider.value
})