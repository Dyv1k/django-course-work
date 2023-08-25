
window.onload = () => {
    
    const translateRoles = document.querySelectorAll('[data-translate_role]')

    translateRoles.forEach((item)=>{
        const innerValue = item.innerHTML.split('').join('')
        switch (innerValue) {
            case 'ADM':
                item.innerHTML = 'Администратор'
                break;
            case 'MAN':
                item.innerHTML = 'Менеджер'
                break;
            case 'CLI':
                item.innerHTML = 'Клиент'
                break;
            default:
                break;
        }
    })
}