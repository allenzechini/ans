// Component to pull and display customer equipment data

/*
    XHR defaults to async, and setting to sync is very bad practice
    as it freezes the entire browser until execution is complete. 

    getData() returns a promise and allows us to call React render upon
    response being returned.
*/




/* ================ GLOBALS ================ */


const url = 'http://localhost:8000/customer_data.json';

// DOM Elements
const domContainer = document.querySelector("#root");
const inputFilter = document.getElementById("filter-input");
const selectRef = document.getElementById("filter-type");


const getData = () => {
    // Return a promise to use in conjunction with async XML response
    return new Promise((resolve, reject) => {

        // Fetch the list via XHR before creating component
        let xhr = new XMLHttpRequest()
        xhr.open('GET', url)
        xhr.send()

        // This ensures data is present and initialized
        xhr.onload = () => {
            if (xhr.status == 200 && xhr.readyState && xhr.response !== "") {
                try {
                    const data = JSON.parse(xhr.response);
                    resolve(data);
                }
                catch (e) {
                    if (e instanceof SyntaxError) {
                        console.warn("Issue while loading JSON. ", e.message, e)
                        console.warn("JSON in question . . . ", xhr.response)
                    }
                    reject(e.message)
                }
            }
        }
    })
}


/* ================ MAIN ================ */
// Get data from json file -> parse it -> load EquipmentList and initialize with data
getData()
    .then(data => {
        ReactDOM.render(<EquipmentList data={data} />, domContainer);
    }, error => console.error(error))


// Define component
class EquipmentList extends React.PureComponent {
    constructor(props) {
        super(props);
        this.state = {
            filteredData: this.props.data,
            filterSearch: "",
            filterType: ""
        };
        this.onSearch = this.onSearch.bind(this);
        this.onSelectFilter = this.onSelectFilter.bind(this);
        this.applyFilters = this.applyFilters.bind(this);
    }




    componentDidMount() {
        // Search field
        inputFilter.addEventListener('keyup', this.onSearch)

        // Select field
        selectRef.addEventListener('change', this.onSelectFilter);
    }




    onSearch() {
        // Search field

        this.setState({ filterSearch: inputFilter.value });
        this.applyFilters();
    }




    onSelectFilter(selectField) {
        // Select field

        this.setState({
            filterType: selectRef.value
        })

        this.applyFilters();
    }




    applyFilters() {
        // Return rows after applying all filters to data
        if (this.state.filterSearch == null && this.state.filterType == null) {
            const allData = this.state.filteredData.map(category => this.state.filteredData[category])
            this.setState({ filteredData: allData })
        }

        const typeMatches = this.state.filterType == "" ? this.props.data : this.props.data.filter(item => item[0] == this.state.filterType)

        // console.log(`typeMatches: ${typeMatches.length}`)

        const searchMatches = this.state.filterSearch == "" ? typeMatches :
            typeMatches.filter(row => {
                // So that search will work with all fields, split each field into lowercase words and then match against array
                // Return true for the ENTIRE row if any fields have a match
                for (var item in row) {
                    // if (row[item].toLowerCase().split(" ").filter(word => word.match(this.state.filterSearch.toLowerCase())).length)
                    if (row[item].toLowerCase().match(this.state.filterSearch.toLowerCase()))
                    return true
                }
                return false
            })

        this.setState({ filteredData: searchMatches })
    }

    render() {

        const list = this.state.filteredData

        console.log(list.length)
        const equipmentList = list.map(item => {
            return (
                <tr key={(item[0] + item[1].toString() + item[2])}>
                    <td>{item[0]}</td>
                    <td>{item[1]}</td>
                    <td>{item[2]}</td>
                </tr>
            )
        })


        return (
            <table className="table table-dark table-striped table-hover" >
                <thead className="thead-light">
                    <tr>
                        <th>Type</th>
                        <th>Serial Number</th>
                        <th>Customer</th>
                    </tr>
                </thead>
                <tbody>
                    {equipmentList}
                </tbody>
            </table >
        )
    }
}