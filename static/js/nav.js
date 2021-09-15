let authBtn = document.getElementById('authBtn');
let closeBtn = document.getElementById('closeAuthWindowBtn');
let authWindow = document.getElementById('authWindow');

let isAuthWindowShowed = false;

authBtn.addEventListener('click', showHideAuthWindow, false);
closeBtn.addEventListener('click', showHideAuthWindow, false);

function showHideAuthWindow(e)
{
    e.preventDefault();

    isAuthWindowShowed = !isAuthWindowShowed;
    
    if (isAuthWindowShowed)
    {
        authWindow.classList.add('modalShowed'); 
        document.body.classList.add('modalShowedBody');
    }
    else
    {
        authWindow.classList.remove('modalShowed');
        document.body.classList.remove('modalShowedBody');
    }
}