// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    if (filterValue.length === 0) {
        return items;
    }

    const l = items.length;
    const filterArr = filterValue.split(" ");
    let filteredData = [];
    const xlm = filterValue[0] === "!";
    console.log(xlm);

    if (filterArr.length < 2) {

    } else {

    }
    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    for (let i=0; i<l; i++) {
        if(!xlm) {
            if(items[i]["Title"].split(" ").includes(filterValue)){
                filteredData.push(items[i])
                console.log(filteredData)
            }
            }else {
             if(!(items[i]["Title"].split(" ").includes(filterValue.replace('!', '')))){
                 filteredData.push(items[i])
            }
        }
    }

    return filteredData
}

function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
    console.log("increaseFont")
}

function decreaseFont() {
    console.log("decreaseFont")
}