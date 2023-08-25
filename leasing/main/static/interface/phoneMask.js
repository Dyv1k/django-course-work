const element = document.getElementsByName('phone')[0];
    const maskOptions = {
        mask: '+{7}(000)000-00-00',
    }
    const mask = new IMask(element, maskOptions);

    const element2 = document.getElementsByName('email')[0];
    const maskOptions2 = {
        mask: function (value) {
            if (/^[a-z0-9_\.-]+$/.test(value))
                return true;
            if (/^[a-z0-9_\.-]+@$/.test(value))
                return true;
            if (/^[a-z0-9_\.-]+@[a-z0-9-]+$/.test(value))
                return true;
            if (/^[a-z0-9_\.-]+@[a-z0-9-]+\.$/.test(value))
                return true;
            if (/^[a-z0-9_\.-]+@[a-z0-9-]+\.[a-z]{1,4}$/.test(value))
                return true;
            if (/^[a-z0-9_\.-]+@[a-z0-9-]+\.[a-z]{1,4}\.$/.test(value))
                return true;
            if (/^[a-z0-9_\.-]+@[a-z0-9-]+\.[a-z]{1,4}\.[a-z]{1,4}$/.test(value))
                return true;
            return false;
        },
        lazy: false
    }
    const mask2 = new IMask(element2, maskOptions2);