class PrintData {
    constructor(data, filter) {
        this.data = data
        this.filter = filter
        this.heads = Object.keys(this.data[0])
    }

    clearState(idEl) {
        var el = document.getElementById(idEl)

        while (el.hasChildNodes()) {
            el.removeChild(el.firstChild)
        }
    }

    rollFilter() {
        this.clearState('select_filter')

        let routesArr = ['all']
        this.data.forEach((d) => {
            if (!routesArr.includes(d['route'])) {
                routesArr.push(d['route'])
            }
        })

        routesArr.forEach((s) => {
            var selectOption = document.createElement('option')
            selectOption.setAttribute('value', s)
            selectOption.innerText = s
            if (s === this.filter) {
                selectOption.selected = true
            }
            document.getElementById('select_filter').appendChild(selectOption)
        })

    }

    rollTable() {
        // Add heads to data table.
        this.clearState('table_head')
        this.heads.forEach((k) => {
            var head = document.createElement('th')
            head.innerText = k.toUpperCase().replace('_', ' ')
            document.getElementById('table_head').appendChild(head)
        })

        
        // Add rows to data table.
        this.clearState('table_body')
        this.data.forEach((d) => {
            if (this.filter === d['route'] || this.filter === 'all') {
                var row = document.createElement('tr')
                this.heads.forEach((h) => {
                    var cell = document.createElement('td')
                    cell.innerText = d[h]
                    row.appendChild(cell)
                })
                document.getElementById('table_body').appendChild(row)
            }
        })
    }
}

const externalOperator = (jsonData, selectEl) => {
    if (jsonData.length > 0) {
        var roller = new PrintData(jsonData, selectEl)
        roller.rollTable()
        roller.rollFilter()
    }
}

