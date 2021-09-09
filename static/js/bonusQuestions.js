// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log("SORTING THE SHIT OUT OF YOU")
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        items.sort((a,b)=> {
            a = a["Description"];
            b = b["Description"];
            if(a<b){
                return -1;
            }
            if(a>b){
                return 1;
            } else {
                return 0;
            }
        })
    } else {
        items.sort((a,b)=> {
            a = a["Description"];
            b = b["Description"];
            if(a<b){
                return 1;
            }
            if(a>b){
                return -1;
            } else {
                return 0;
            }
        })
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {

    if (filterValue.length === 0) {
        return items;
    }

    const filterArr = filterValue.split(" ");
    let filteredData = [];
    const xlm = filterValue[0] === "!";

    if (filterArr.length < 2 && filterArr[0] !== "Description:") {
        filterByWord(xlm, items, filteredData, filterValue, "Title")
    } else {
        filterByWord(xlm, items, filteredData, filterArr[1], "Description")
    }

    return filteredData
}

function filterByWord(c, initArr, arr, value, key){
    const l = initArr.length;
    for (let i=0; i<l; i++) {
        if(!c) {
            if(initArr[i][key].split(" ").includes(value)){
                arr.push(initArr[i])
            }
        }else {
            if(!(initArr[i][key].split(" ").includes(value.replace('!', '')))){
                arr.push(initArr[i])
            }
        }
    }
}

function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
    fontEval(1);
}

function decreaseFont() {
    fontEval(-1);
}

function fontEval(c){
    const body = document.querySelector("table")
    let number = window.getComputedStyle(body, null).getPropertyValue("font-size")
    let fontSize = Number(number.replace("px", ""))
    const limit = c > 0 ? 25 : 3;
    if (c > 0) {
        fontSize = fontSize < limit ? fontSize + 1 * c : fontSize;
    } else {
        fontSize = fontSize > limit ? fontSize + 1 * c : fontSize;
    }
    body.setAttribute("style", `font-size: ${fontSize}px`)
}