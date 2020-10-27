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

function fill_fields(account) {
    document.querySelector("#original_value"
        ).textContent = `R$${account.original_value.toFixed(2)}`
    document.querySelector("#actual_value"
        ).textContent = `R$${account.actual_value.toFixed(2)}`
    document.querySelector("#today_gain"
        ).textContent = "R$0,00"
    document.querySelector("#from_date"
        ).textContent = account.from_date
    document.querySelector("#to_date"
        ).textContent = account.to_date
}

function login(account) {
    localStorage.setItem('account', account);
    document.querySelectorAll('.logout').forEach(item => {
        item.style.display = 'none'
    });
    document.querySelectorAll('.login').forEach(item => {
        item.style.display = 'flex'
    });

    fill_fields(account);
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
        "from_date": '19/09/2000',
        "to_date": '30/10/2000',
        "original_value": 0.0, 
        "actual_value": 0.5, 
        "settings": {
            "stopwin": 10,
            "stoploss": 10,
            "gales": 2
        },
        "filters": {
            "filtro_gols": [0, 0],
            "tempo": 45,
            "maximo": 6 
        },
        "search": [
            ["Partida - Gols", ["mais de", "1.5"], 10],
            ["Gols +/-", ["mais de", "2.5"], 5],
            ["Próximos 10 Minutos", ["mais de", "Escanteios"], 3]
        ]
    });
    close_login()

    return

    eel.handle_login(account)((result) => {
        if (!result) {
            shakeInputs();
        } else {
            login(result);
            close_login()
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
}
