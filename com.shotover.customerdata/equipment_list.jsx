// Component to pull and display customer equipment data

/*
    XHR defaults to async, and setting to sync is very bad practice
    as it freezes the entire browser until execution is complete. 

    getData() returns a promise and allows us to call React render upon
    response being returned.
*/



/* ================ GLOBALS ================ */

const url = 'http://localhost:8000/r_product_info.json';
const domContainer = document.querySelector("#root");

const getData = () => {
    // Return a promise to use in conjunction with async XML response
    return new Promise((resolve, reject) => {

        // Fetch the list via XHR before creating component
        let xhr = new XMLHttpRequest()
        xhr.open('GET', url)
        xhr.send()
        
        // This ensures data is present and initialized
        xhr.onload = () => {
            if (xhr.status == 200 && xhr.readyState && xhr.response !== ""){
                try { 
                    const data = JSON.parse(xhr.response)["data"];
                    resolve(data);
                }
                catch(e) {
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
            filters: []
        };
        this.onFilterChange = this.onFilterChange.bind(this);
    }

    componentDidMount() {
        const inputFilter = document.getElementById("filter-input");

        inputFilter.addEventListener('keyup', this.onFilterChange)
    }

    onFilterChange(props) {
        const inputFilter = document.getElementById("filter-input");

        const filteredData = this.props.data.map(itemType => {
            return itemType.filter(item => (
                // So that search will work wiill all fields, split each field into lowercase words and then match against array
                // Return true for the ENTIRE row if any fields have a match
                item[0].toLowerCase().split(" ").filter(word => word.match(inputFilter.value.toLowerCase())).length ||
                item[1].toLowerCase().split(" ").filter(word => word.match(inputFilter.value.toLowerCase())).length ||
                item[2].toLowerCase().split(" ").filter(word => word.match(inputFilter.value.toLowerCase())).length
            ))
        })

        this.setState({ filteredData });
    }

    render() {

        const list = this.state.filteredData ? this.state.filteredData : this.props.data;

        const equipmentList = list.map(itemType => {
            return itemType.map(item => {
                return (
                    <tr key={(item[1].toString() + item[2])}>
                        <td>{item[0]}</td>
                        <td>{item[1]}</td>
                        <td>{item[2]}</td>
                    </tr>
                )
            })
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