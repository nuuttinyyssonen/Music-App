let hiddenContent = document.getElementById('change-name');
let playlistName = document.getElementById('playlist_name');
let dropDownPlaylistActions = document.getElementById('dropdown-playlist-actions');
let threeDotsBtn = document.getElementById('threeDots');

playlistName.addEventListener('click', displayContent)
threeDotsBtn.addEventListener('click', displayDropDown)

function displayContent() {
    if (hiddenContent.style.display == 'none') {
        hiddenContent.style.display = 'flex'
        console.log('working')
    } else {
        hiddenContent.style.display = 'none'
    }
}

function displayDropDown() {
    if (dropDownPlaylistActions.style.display == 'none') {
        dropDownPlaylistActions.style.display = 'flex'
    } else {
        dropDownPlaylistActions.style.display = 'none'
    }
}