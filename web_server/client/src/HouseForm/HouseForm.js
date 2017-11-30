import 'materialize-css/dist/css/materialize.min.css';
import 'materialize-css/dist/js/materialize.js';
import React from 'react';
import './HouseForm.css';
class HouseForm extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            address:'',
            city:'',
            stateName:'',
            zipcode:0,
            flooring: 0,
            fencing: false,
            baths: 0,
            beds: 0,
            builtYr:0,
            gutters: false,
            sqft:0
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }


    handleChange(event){
        const field = event.target.name;
        const tempState = this.state
        if ((field==='fencing' || field==='gutters') && event.target.value === 'on'){
            tempState[field] = true;
        } else if (field==='flooring' && event.target.id ==='None'){
            tempState[field] = 0;
        } else if (field==='flooring' && event.target.id==='Tile'){
            tempState[field] = 1;
        } else if (field==='flooring' && event.target.id==='Carpet'){
            tempState[field] = 2;
        } else if (field==='flooring' && event.target.id==='Laminate'){
            tempState[field] = 3;
        } else if (field==='flooring' && event.target.id==='HardWood'){
            tempState[field] = 4;
        } else {
            tempState[field] = event.target.value;
        }
        console.log(tempState)
        this.setState({tempState});
    }

    handleSubmit(event) {
        event.preventDefault();
        fetch('http://' + window.location.hostname + ':6060/prediction/', {
            method: 'POST',
            cache: false,
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                flooring:this.state.flooring,
                fencing:this.state.fencing,
                baths:this.state.baths,
                beds:this.state.beds,
                zip_code:this.state.zipcode,
                built_yr:this.state.built_yr,
                gutters:this.state.gutters,
                sqft:this.state.sqft
            })
          }).then(response => {
            if (response.status === 200) {
              console.log(response.body)
            } else {
              console.log('submit failed.');
            }
          });
    }
    render() {
        return (
            <div className="container">
            <div className="card-panel login-panel">
              <form className="col s12" action="/" onSubmit={this.handleSubmit}>
                <div className="row">
                    <div className="input-field col s12">
                    <input type='text' value={this.state.address} name='address' onChange={this.handleChange}></input>
                    <label htmlFor="address">Address</label>
                    </div>
                </div>
                <div className="row">
                    <div className="input-field col s4">
                    <input type='text' value={this.state.city} name='city' onChange={this.handleChange}></input>
                    <label htmlFor="city">City</label>
                    </div>
                    <div className="input-field col s4">
                        <input id="stateName" value={this.state.stateName} name='stateName' type="text" onChange={this.handleChange}></input>
                        <label htmlFor="stateName">State</label>
                    </div>
                    <div className="input-field col s4">
                        <input id="zipcode" value={this.state.zipcode} name='zipcode' type="number" onChange={this.handleChange}></input>
                        <label htmlFor="zipcode">Zip Code</label> 
                    </div>
                </div>
                <div className="row">
                    <div className="input-field col s4">
                        <input id="sqft" value={this.state.sqft} name='sqft' type="number" onChange={this.handleChange}></input>
                        <label htmlFor="sqft">sqft</label>
                    </div>
                    <div className="input-field col s4">
                        <input id="beds" value={this.state.beds} name='beds' type="number" onChange={this.handleChange}></input>
                        <label htmlFor="beds">beds</label>
                    </div>
                    <div className="input-field col s4">
                        <input id="baths" value={this.state.baths} name='baths' type="number" onChange={this.handleChange}></input>
                        <label htmlFor="baths">baths</label>
                    </div>
                </div>
                <div className="row">
                    <div className="input-field col s4 fixed">
                        <input type="checkbox" name="fencing" id="fencing" checked={this.state.fencing} onChange={this.handleChange}></input>
                        <label htmlFor='fencing'>Fencing</label>
                    </div>
                    <div className="input-field col s4 fixed">
                        <input type="checkbox"  name="gutters" id="gutters" checked={this.state.gutters} onChange={this.handleChange}></input>
                        <label htmlFor="gutters">Gutters</label>
                    </div>
                </div>
                <div className="row">
                    <div className="input-field col s4 fixed">
                        <input className="with-gap" name="flooring" type="radio" id="None" onChange={this.handleChange}></input>
                        <label htmlFor="None">None</label>
                        <input className="with-gap" name="flooring" type="radio" id="Tile" onChange={this.handleChange}></input>
                        <label htmlFor="Tile">Tile</label>
                        <input className="with-gap" name="flooring" type="radio" id="Carpet" onChange={this.handleChange}></input>
                        <label htmlFor="Carpet">Carpet</label>
                        <input className="with-gap" name="flooring" type="radio" id="Laminate" onChange={this.handleChange}></input>
                        <label htmlFor="Laminate">Laminate</label>
                        <input className="with-gap" name="flooring" type="radio" id="HardWood" onChange={this.handleChange}></input>
                        <label htmlFor="HardWood">HardWood</label>
                    </div>
                </div>
                <div className="row">
                    <label htmlFor='builtYr'>Year of build</label>
                    <p className="range-field">
                        <input type="range" name='builtYr' id="builtYr" min="1900" max="2017" onChange={this.handleChange}/>
                    </p>
                </div>
                <div className="row right-align">
                    <input type="submit" className="waves-effect waves-light btn indigo lighten-1" value='Submit'/>
                </div>
              </form>
            </div>
          </div>
        );
    }
}

export default HouseForm;