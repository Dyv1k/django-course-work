import {MAX_LENGTH_CARDS_DESCRIPTION, MAX_LENGTH_ORDERS_DESCRIPTION} from './config.js';
import {splitValues} from './splitValues.js';

window.onload = () => {
    const textSplit = document.querySelectorAll('[data-text_split]')
    const textSplitLarge = document.querySelectorAll('[data-text_split_large]')
    const numbersSplit = document.querySelectorAll('[data-number_split]')
    if (numbersSplit.length > 0) {
        numbersSplit.forEach((item)=>{
            item.innerText = splitValues.splitNumbers(item.innerText, false)
        })
    }
    if (textSplit.length > 0) {
        textSplit.forEach((item)=>{
            item.innerText = splitValues.splitText(item.innerText, MAX_LENGTH_CARDS_DESCRIPTION)
        })
    }
    if (textSplitLarge.length > 0) {
        textSplitLarge.forEach((item)=>{
            item.innerText = splitValues.splitText(item.innerText, MAX_LENGTH_ORDERS_DESCRIPTION)
        })
    }
}