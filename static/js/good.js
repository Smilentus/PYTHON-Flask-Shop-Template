let minusBtn = document.getElementById('inputMinus');
let plusBtn = document.getElementById('inputPlus');

let inputAmount = document.getElementById('inputAmount');

let amount = 1;

minusBtn.addEventListener('click', minusAmount, false);
plusBtn.addEventListener('click', plusAmount, false);

function plusAmount(e)
{
    e.preventDefault();
    amount++;
    inputAmount.value = amount;
}

function minusAmount(e)
{
    e.preventDefault();
    amount--;
    if (amount <= 0)
        amount = 1;
    inputAmount.value = amount;
}