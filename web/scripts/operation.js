function handle_select(event) {
    const account = JSON.parse(localStorage.getItem('account'))

    const input = event.target;
    const [title, option] = input.id.split('|')
    account.search = account.search.filter(
        (x) => (x[0] !== title))

    if (input.checked) {
        account.search.push([title, option, account.value])
    } 
    
    localStorage.setItem('account', JSON.stringify(account));
}

function handle_change(event) {
    const account = JSON.parse(localStorage.getItem('account'))
    
    const input = event.target;
    const [title, option] = input.id.split('|')
    account.search = account.search.filter(
        (x) => (x[0] !== title))
    if (input.value !== "") {
        account.search.push(
            [title, [option, input.value], account.value]);
    }
    
    localStorage.setItem('account', JSON.stringify(account));

    console.log(account)
}

function operate() {
    const account = JSON.parse(localStorage.getItem('account'));
    console.log(account);
}