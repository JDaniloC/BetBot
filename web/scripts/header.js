$(function(){
    $("header").load("components/header.html"); 
});

function toggle_user_container() {
    const login = document.querySelector('.user-container');
    if (login.style.display == '') {
        login.style.display = 'inline-flex'
    } else {
        login.style.display = ''
    }
}

function welcome() {
    $(function(){
        $("main").load("components/welcome.html"); 
    });
}

function operation() {
    if (localStorage.getItem('account') === null) {
        return open_login()
    }
    $(function(){
        $("main").load("components/operation.html"); 
    });
}

function configuration() {
    if (localStorage.getItem('account') === null) {
        return open_login()
    }

    $(function(){
        $("main").load("components/config.html"); 
    });
}