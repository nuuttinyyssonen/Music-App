let hiddenContent = document.getElementById('change-name');
let playlistName = document.getElementById('playlist_name');

playlistName.addEventListener('click', displayContent)

function displayContent() {
    if (hiddenContent.style.display == 'none') {
        hiddenContent.style.display = 'flex'
        console.log('working')
    } else {
        hiddenContent.style.display = 'None'
    }
}