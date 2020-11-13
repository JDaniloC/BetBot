function openBets() {
    const wallet = document.querySelectorAll('.wallet > *');
    if (wallet[1].style.display == 'flex') {
        return closeBets();
    }
    wallet.forEach(element => {
        if (element.tagName !== "HEADER") {
            element.style.display = "flex";
        }
    })
}

function closeBets() {
    const wallet = document.querySelectorAll('.wallet > *');
    wallet.forEach(element => {
        if (element.tagName !== "HEADER") {
            element.style.display = "none";
        }
    })
}

function addBet(betTitle, betInfo) {
    function createCloseButton() {
        const closeBet = document.createElement("button");
        const closeImg = document.createElement("img");
        closeBet.className = "close-bet";
        closeImg.src = "images/x.svg";
        closeBet.addEventListener('click', function() {
            removeBet(betTitle); 
            removeFromSearch(betTitle);
        });
        closeBet.appendChild(closeImg)
        return closeBet;    
    }
    function createInfos() {
        const infos = document.createElement("div");
        infos.className = "bet-information";
        infos.appendChild(createText(betTitle));
        infos.appendChild(createText(betInfo));
        return infos;
    }
    function createText(text) {
        const p = document.createElement("p");
        p.textContent = text
        return p
    }
    function createInput() {
        const input = document.createElement("input");
        input.type = "text";
        input.className = "bet-value";
        input.placeholder = "Valor de Aposta";
        input.addEventListener('input', function() {
            moneyFormatter(input); 
            calculateAmount();
        });
        input.addEventListener('focusout', function(event) {
            const account = JSON.parse(localStorage.getItem('account'))
            const valor = event.target.value;
            account.search.forEach(bet => {
                if (bet[0] === betTitle) {
                    bet[2] = parseFloat(
                        valor.replace("R$", "").replace(",", "."));
                }
            });
            localStorage.setItem('account', JSON.stringify(account));
        });
        input.oninput = "moneyFormatter(this)";
        return input;
    }
    removeBet(betTitle);
    const bets = document.querySelector('.wallet ul');
    const newBet = document.createElement("li");
    newBet.appendChild(createCloseButton());
    newBet.appendChild(createInfos());
    const input = createInput()
    newBet.appendChild(input);
    bets.appendChild(newBet);

    const counter = document.querySelector(
        '.wallet .wallet-counter');
    counter.textContent = parseInt(counter.textContent) + 1;
    return input;
}

function removeBet(betTitle) {
    const bets = document.querySelectorAll('.wallet li');
    bets.forEach(bet => {
        const [title, option] = bet.querySelectorAll("p");
        if (title.textContent === betTitle) {
            document.querySelector(
                '.wallet ul'
            ).removeChild(bet)
            const counter = document.querySelector(
                '.wallet .wallet-counter');
            counter.textContent = parseInt(counter.textContent) - 1;
            calculateAmount()
        }
    })
}

function clearBets() {
    const bets = document.querySelectorAll('.wallet li');
    bets.forEach(element => {
        document.querySelector(
            '.wallet ul'
        ).removeChild(element)
    })
    document.querySelector(
        '.wallet .wallet-balance p + p'
    ).textContent = "R$0,00"
    document.querySelector(
        '.wallet .wallet-counter'
    ).textContent = 0;

    const account = JSON.parse(
        localStorage.getItem('account'));
    account.search = [];
    localStorage.setItem('account', JSON.stringify(account));

    document.querySelectorAll('.operation input').forEach(
        element => {
            element.checked = false;
            element.value = '';
    })
}

function calculateAmount() {
    const inputs = document.querySelectorAll('.wallet input');
    let amount = 0;
    inputs.forEach(input => {
        if (input.value !== "") {
            amount += parseFloat(input.value.replace(
                "R$", ""
            ).replace(",", "."));
        }
    })
    document.querySelector(
        '.wallet .wallet-balance p + p'
    ).textContent = `R$${amount.toFixed(2)}`
}