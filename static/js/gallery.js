let container = document.getElementById('galleryContainer');

let modalBackground = document.getElementById('modalBackground');
let modalWindow = document.getElementById('modalWindow');

let closeFullBtn = document.getElementById('fullCloseBtn');
let fullScreenImage = document.getElementById('fullScreenImage');
let fullLeftArrow = document.getElementById('fullLeftArrow');
let fullRightArrow = document.getElementById('fullRightArrow');

let lastOpenedImage = 0;

modalBackground.addEventListener('click', closeImages);
closeFullBtn.addEventListener('click', closeImages);
fullLeftArrow.addEventListener('click', openPrevImage);
fullRightArrow.addEventListener('click', openNextImage);

function createGallery() {
    let eng = 'ABCDEFGHIKLMNOPRSTU';
    for (let counter = 0; counter <= 18; counter++) {
        let block = document.createElement('img');
        block.setAttribute('class', `block${eng[counter]}`);
        block.setAttribute('src', `./static/gallery/gallery_${counter}.jpg`);
        block.setAttribute('onclick', `openImage(${counter})`);
        container.appendChild(block);
    }
}

function closeImages() {
    modalBackground.classList.add('hidden');
    modalWindow.classList.add('hidden');
    document.body.style = '';
}

function openImage(imageNumber) {
    if (imageNumber > 18) imageNumber = 0;
    if (imageNumber < 0) imageNumber = 18;

    modalWindow.classList.remove('hidden');
    modalBackground.classList.remove('hidden');
    fullScreenImage.setAttribute('src', `./static/gallery/gallery_${imageNumber}.jpg`);
    lastOpenedImage = imageNumber;

    document.body.style = 'overflow: hidden';
}

function openNextImage() {
    openImage(++lastOpenedImage);
}

function openPrevImage() {
    openImage(--lastOpenedImage);
}

createGallery();