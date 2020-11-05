function handle_select(event) {
    const account = JSON.parse(localStorage.getItem('account'))

    const input = event.target;
    const [title, option] = input.id.split('|')
    account.search = account.search.filter(
        (x) => (x[0] !== title))

    if (input.checked) {
        account.search.push([title, option, 0])
        addBet(title, option);
    } else {
        removeBet(title, option);
    }
    
    localStorage.setItem('account', JSON.stringify(account));
}

function handle_change(event) {
    const account = JSON.parse(localStorage.getItem('account'))
    
    const input = event.target;
    const [title, option] = input.id.split('|')
    account.search = account.search.filter(
        (x) => (x[0] !== title))
    if (input.value.replaceAll("+", "").replaceAll("-", "") !== "") {
        account.search.push([title, [option, input.value], 0]);
    }
    
    localStorage.setItem('account', JSON.stringify(account));
}

function operate() {
    const account = JSON.parse(localStorage.getItem('account'));
    eel.operate(account);
}