export class splitValues{
    
    static splitNumbers(field, itemObj){
        //field - поле  объекта или число
        const defaultSplitArray = itemObj? String(itemObj[field]).split('').reverse() : String(field).split('').reverse()
        let splitIteration = 0
        let splitArray = defaultSplitArray.map((item, index)=>{
            if (((index+1) % 3) === 0) {
                splitIteration += 1
                return `${defaultSplitArray[index]}${defaultSplitArray[index-1]}${defaultSplitArray[index-2]}`
            }
        })
        if(splitIteration*3 !== defaultSplitArray.length){
            splitArray.push(defaultSplitArray.slice(splitIteration*3, defaultSplitArray.length).reverse().join(''))
        }
        return splitArray.reverse().join(' ')
    }

    static splitText(field, parametr){
        if (field.length > parametr) {
            const splitString = field.split('')
            return `${splitString.splice(0, parametr).join('')} ...`
        }
        else return field
    }
}