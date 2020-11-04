$(function(){
    $("main").load("components/welcome.html"); 
});

function shakeInputs() {
    const shakeAnimation = [
        [ 
            { transform: 'translateX(0px)' },
            { transform: 'translateX(-10px)' },
            { transform: 'translateX(10px)' },
            { transform: 'translateX(0px)' }
        ], { 
            duration: 150,
            iterations: 2
        }
    ]

    username.parentElement.animate(
        shakeAnimation[0], shakeAnimation[1])
    password.parentElement.animate(
        shakeAnimation[0], shakeAnimation[1])
}

function open_login() {
    const blur = document.querySelector('.blur');
    const login = document.querySelector('.login-panel');
    blur.style.display = 'block';
    login.style.transform = 'translateY(0)'
}

function close_login() {
    const blur = document.querySelector('.blur');
    const login = document.querySelector('.login-panel');
    blur.style.display = 'none';
    login.style.transform = 'translateY(-300px)'
}

function cleanup_username() {
    const username = document.querySelector('#username');
    username.value = '';
}

function fill_field(css_selector, value) {
    document.querySelector(css_selector
        ).textContent = value
}

function load_license(account) {
    const original_value = account.license.original_value.toFixed(2)
    const actual_value = account.license.actual_value.toFixed(2)
    fill_field("#original_value", `R$${original_value}`)
    fill_field("#actual_value", `R$${actual_value}`)
    fill_field("#today_gain", "R$0,00")
    fill_field("#from_date", account.license.from_date)
    fill_field("#to_date", account.license.to_date)
}

function login(account) {
    localStorage.setItem('account', JSON.stringify(account));
    document.querySelectorAll('.logout').forEach(item => {
        item.style.display = 'none'
    });
    document.querySelectorAll('.login').forEach(item => {
        item.style.display = 'flex'
    });

    load_license(account);
    close_login()
}

function handle_login() {
    const username = document.querySelector('#username');
    const password = document.querySelector('#password');
 
    if (username.value === '' || password.value === '') {
        shakeInputs()
        return
    }

    const account = {
        username: username.value, password: password.value
    }
    username.value = '';
    password.value = '';

    login({
        "email": "gabrieltradermm007@gmail.com",
        "username": "trojan43",
        "password": "021820g",
        "digits": "0218",
        "license": {
            "from_date": '19/09/2000',
            "to_date": '30/10/2000',
            "original_value": 0.0, 
            "actual_value": 0.5, 
        },
        "settings": {
            "stopWin": 10,
            "stopLoss": 10,
            "maxGales": 2
        },
        "filters": {
            "golsFilter": [true, [0, 0]],
            "maxTime": 45,
            "maxBet": 6,
            "minOdd": 0
        },
        "search": [
            ["Resultado Final", "casa", 10],
            ["Partida - Gols", ["Mais de", "1.5"], 10]
        ]
    });

    return

    eel.handle_login(account)((result) => {
        if (!result) {
            shakeInputs();
        } else {
            login(result);
        }
    })
}

function logout() {
    localStorage.removeItem('account')
    toggle_user_container();

    document.querySelectorAll('.logout').forEach(item => {
        item.style.display = 'flex'
    });
    document.querySelectorAll('.login').forEach(item => {
        item.style.display = 'none'
    });
    welcome();
}
