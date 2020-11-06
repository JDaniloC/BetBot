function handleSelect(event) {
    const input = event.target;
    const [title, option] = input.id.split('|')
    const account = removeFromSearch(title);

    if (input.checked) {
        account.search.push([title, option, 0])
        addBet(title, option);
    } else {
        removeBet(title, option);
    }
    
    localStorage.setItem('account', JSON.stringify(account));
}

function handleChange(event) {
    const input = event.target;
    const [title, option] = input.id.split('|')
    const account = removeFromSearch(title);

    if (input.value.replaceAll("+", "").replaceAll("-", "") !== "") {
        account.search.push([title, [option, input.value], 0]);
    }
    
    localStorage.setItem('account', JSON.stringify(account));
}

function removeFromSearch(title) {
    const account = JSON.parse(localStorage.getItem('account'))
    account.search = account.search.filter(
        (x) => (x[0] !== title))
    localStorage.setItem('account', JSON.stringify(account));
    return account;
}

function operate() {
    const account = JSON.parse(localStorage.getItem('account'));
    eel.operate(account);
}