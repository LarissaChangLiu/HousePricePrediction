import React from 'react';
import './HouseForm.css';

class HouseForm extends React.Component {
    render() {
        return (
            <div className="container">
            <div className="card-panel login-panel">
              <form className="col s12" action="/">
                <div class="row">
                    <div className="input-field col s12">
                    <input ></input>
                    <label for="address">Address</label>
                    </div>
                </div>
                <div className="row">
                    <div className="input-field col s4">
                    <input ></input>
                    <label for="city">City</label>
                    </div>
                    <div className="input-field col s4">
                        <select>
                            <option value="" disabled selected>Choose state</option>
                            <option value="Alabama">Alabama</option>
                            <option value="Alaska">Alaska</option>
                            <option value="Arizona">Arizona</option>
                            <option value="Arkansas">Arkansas</option>
                            <option value="California">California</option>
                            <option value="Calorado">Calorado</option>
                            <option value="Connecticut">Connecticut</option>
                            <option value="Delaware">Delaware</option>
                            <option value="Florida">Florida</option>
                            <option value="Georgia">Georgia</option>
                            <option value="Hawaii">Hawaii</option>
                            <option value="Idaho">Idaho</option>
                            <option value="IIIinois">IIIinois</option>
                            <option value="Indiana">Indiana</option>
                            <option value="Iowa">Iowa</option>
                            <option value="Kansas">Kansas</option>
                            <option value="Kentucky">Kentucky</option>
                        </select>
                        <label>State</label>
                    </div>
                    <div className="input-field col s4">
                        <input id="zipcode" name='zipcode' type="number"></input>
                        <label for="zipcode">Zip Code</label>
                    </div>
                </div>
                <div className="row">
                    <div className="input-field col s4">
                        <input id="sqft" name='sqft' type="number"></input>
                        <label for="sqft">sqft</label>
                    </div>
                    <div className="input-field col s4">
                        <select id='beds' name='beds' type="number">
                            <option value="" disabled selected>Choose # of beds</option>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                        <label>Beds</label>
                    </div>
                    <div className="input-field col s4">
                        <select>
                            <option value="" disabled selected>Choose # of baths</option>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                        <label>baths</label>
                    </div>
                </div>
                <div className="row">
                    <div className="input-field col s4">
                        <div className="switch">
                            <label>
                                No Fencing
                                <input type="checkbox" ></input>
                                <span className="lever"></span>
                                Has Fencing
                            </label>
                        </div>
                    </div>
                    <div className="input-field col s4">
                        <div className="switch">
                            <label>
                                No Gutters
                                <input></input>
                                <span className="lever"></span>
                                Has Gutters
                            </label>
                        </div>
                    </div>
                    <div className="input-field col s4">
                        <select>
                            <option value="" disabled selected>Choose type of floor</option>
                            <option value="4">HardWood</option>
                            <option value="3">Laminate</option>
                            <option value="2">Carpet</option>
                            <option value="1">Tile</option>
                        </select>
                        <label>Floor Type</label>
                    </div>
                </div>
                <div className="row">
                    Year of build
                    <p className="range-field">
                        <input type="range" name='builtYr' id="builtYr" min="1900" max="2017"/>
                    </p>
                </div>
              </form>
            </div>
          </div>
        );
    }
}

export default HouseForm;