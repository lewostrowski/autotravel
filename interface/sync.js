class PrintData {
    constructor(data, filter) {
        this.data = data
        this.filter = filter
        this.heads = Object.keys(this.data[0])
    }

    rollTable() {
        // Add heads to data table.
        this.heads.forEach((k) => {
            var head = document.createElement('th')
            head.innerText = k
            document.getElementById('table_head').appendChild(head)
        })

        
        // Add rows to data table.
        this.data.forEach((d) => {
            var row = document.createElement('tr')
            this.heads.forEach((h) => {
                var cell = document.createElement('td')
                cell.innerText = d[h]
                row.appendChild(cell)
            })
            document.getElementById('table_body').appendChild(row)
        })
    }
}


const fetchData = () => {
    fetch('http://127.0.0.1:5000', {
        method: 'GET',
        headers: {'Content-Type': 'application/json'}
    })
    .then(res => res.json())
    .then(data => {
        var pd = new PrintData(data, false)
        pd.rollTable()
    })
}
fetchData()