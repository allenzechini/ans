const url = 'http://localhost:8000/r_product_info.txt.python';
// Fetch the list via XHR before creating component
let xhr = new XMLHttpRequest()
xhr.open('GET', url)
xhr.send()

// This ensures data is present and initialized
xhr.onreadystatechange = () => {
    const data = JSON.parse(xhr.response);
    console.log('populateData(): data', data);

    const domContainer = document.querySelector("#root");
    ReactDOM.render(<EquipmentList data={data} />, domContainer);
}


class EquipmentList extends React.PureComponent {
    constructor(props) {
        super(props);
        this.state = { filteredData: null };
        this.onFilterChanage = this.onFilterChanage.bind(this);
    }

    componentDidMount() {
        const inputFilter = document.getElementById("filter-input");

        document.addEventListener('keyup', this.onFilterChanage)
    }

    onFilterChanage(props) {
        const inputFilter = document.getElementById("filter-input");

        const filteredData = this.props.data.map(itemType => {
            return itemType.filter(item => (
                item[0].toLowerCase().startsWith(inputFilter.value.toLowerCase()) ||
                item[1].toLowerCase().startsWith(inputFilter.value.toLowerCase()) ||
                item[2].toLowerCase().startsWith(inputFilter.value.toLowerCase())
            ))
        })
        
        this.setState({ filteredData });
    }

    render() {

        const list = this.state.filteredData ? this.state.filteredData : this.props.data;

        const equipmentList = list.map(itemType => {
            return itemType.map(item => {
                return (
                    <tr key={item[1]}>
                        <td>{item[0]}</td>
                        <td>{item[1]}</td>
                        <td>{item[2]}</td>
                    </tr>
                )
            })
        })

        return (
            <table class="table table-dark table-striped table-hover" >
                <thead class="thead-light">
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

