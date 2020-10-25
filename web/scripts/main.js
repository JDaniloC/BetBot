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

function login(account) {
    localStorage.setItem('account', account);
    document.querySelectorAll('.logout').forEach(item => {
        item.style.display = 'none'
    });
    document.querySelectorAll('.login').forEach(item => {
        item.style.display = 'flex'
    });
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

    eel.handle_login(account)((result) => {
        if (!result) {
            shakeInputs();
        } else {
            login(result);
        }
    })
}
