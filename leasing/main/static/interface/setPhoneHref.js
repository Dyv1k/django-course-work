window.onload = () => {
    
    const phoneLinks = document.querySelectorAll('[data-link_phone]')

    phoneLinks.forEach((item)=>{
        let currentPhoneHref = '';
        item.innerHTML.split('').forEach((target)=>{
            if (!isNaN(target)) {
                currentPhoneHref += `${target}`
            }
        })
        item.href = `tel:${currentPhoneHref}`
    })
}