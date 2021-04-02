function moneyFormatter(input) {
    var number = input.value.replace(/[^\d]/g, '')
    number = number.replace(/^00/g, '')
    if (number.length <= 2) {
        number = number.replace(/(\d+)/g, "R$$00,$1");
    } else {
        number = number.replace(/(\d+)(\d{2})/g, "R$$$1,$2");
    }
    if (input.maxLength !== -1 && input.maxLength == number.length) {
        number = number.slice(0, input.maxLength - 1)
    }
    input.value = number
}

function floatFormatter(input) {
    var number = input.value.replace(/[^\d]/g, '')
    number = number.replace(/(^0)(\d)/g, '$2')
    if (number.length == 1) {
        number = number.replace(/(\d+)/g, "0.$1");
    } else if (number.length == 2) {
        number = number.replace(/(\d)(\d)/g, "$1.$2");
    } else {
        number = number.replace(/(\d+)(\d{2})/g, "$1.$2");
    }
    if (input.maxLength !== -1 && input.maxLength == number.length) {
        number = number.slice(0, input.maxLength - 1)
    }
    input.value = number
}

function intFormatter(input) {
    var number = input.value.replace(/[^\d]/g, '')
    number = number.replace(/(^0)(\d)/g, '$2')
    if (input.maxLength !== -1 && input.maxLength == number.length) {
        number = number.slice(0, input.maxLength - 1)
    }
    input.value = number
}

function intervalFormatter(input) {
    var number = input.value.replace(/[^\d,.]/g, '')
    if (number.length == 4) {
        number = number.replace(/,/g, '')
        number = number.replace(/(\d.\d)(\d)/g, '$1,$2')
    }
    number = number.replace(/(\d)(\d)/g, '$1.$2')
    if (input.maxLength !== -1 && input.maxLength == number.length) {
        number = number.slice(0, input.maxLength - 1)
    }
    input.value = number
}

function handicapFormatter(input) {
    var number = input.value.replace(/[^\d.,+-]/g, '')
    if (number.length == 4) {
        number = number.replace(/,/g, '')
        number = number.replace(/(\d.\d)(\+?\-?\d?)/g, '$1,$2')
    }
    number = number.replace(/(\d)(\d)/g, '$1.$2')
    if (input.maxLength !== -1 && input.maxLength > number.length) {
        number = number.slice(0, input.maxLength - 1)
    }
    input.value = number
}

function golsFormatter(input) {
    var number = input.value.replace(/[^\d-]/g, '')
    number = number.replace(/(\d)(\d)/g, '$1-$2')
    
    if (input.maxLength !== -1 && input.maxLength == number.length) {
        number = number.slice(0, input.maxLength - 1)
    }
    input.value = number
}

function timeFormatter(input) {
    var number = input.value.replace(/[^\d:]/g, '')
    number = number.replace(/(\d{2})(\d{2})/g, '$1:$2')
    
    if (input.maxLength !== -1 && input.maxLength == number.length) {
        number = number.slice(0, input.maxLength - 1)
    }
    input.value = number
}