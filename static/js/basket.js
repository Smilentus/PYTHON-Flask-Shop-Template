let chooseAllBtn = document.getElementById('chooseAllBtn');
let unChooseAllBtn = document.getElementById('unChooseAllBtn');

chooseAllBtn.addEventListener('click', chooseAll, false);
unChooseAllBtn.addEventListener('click', unChooseAll, false);

function chooseAll(e)
{
    e.preventDefault();

    checkBoxes = document.getElementsByClassName('custom-checkbox');
    
    for (let item of checkBoxes)
    {
        item.checked = true;
    }
}

function unChooseAll(e)
{
    e.preventDefault();

    checkBoxes = document.getElementsByClassName('custom-checkbox');
    
    for (let item of checkBoxes)
    {
        item.checked = false;
    }
}