import React from 'react';
import HouseForm from './HousePage';
// import PropTypes from 'prop-types';

class HousePage extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      house: {
        address:'',
        city:'',
        state:'',
        zipcode:0,
        flooring: 0,
		fencing: 0,
		baths: 0,
		beds: 0,
		builtYr:0,
		gutters: 0,
		sqft:0
      }
    };

    this.processForm = this.processForm.bind(this);
  }

  processForm(event) {
    // event.preventDefault();
    // // Post house data.
    // fetch('http://' + window.location.hostname + ':3000/auth/login/', {
    //   method: 'POST',
    //   cache: false,
    //   headers: {
    //     'Accept': 'application/json',
    //     'Content-Type': 'application/json',
    //   },
    //   body: JSON.stringify({
    //     flooring:this.house.flooring,
    //     password:this.state.user.password
    //   })
    // }).then(response => {
    //   if (response.status === 200) {
    //     this.setState({ errors: {}});

    //     response.json().then(json => {
    //       console.log(json);
    //       Auth.authenticateUser(json.token, email);
    //       this.context.router.replace('/');
    //     });
    //   } else {
    //     console.log('Login failed.');
    //     response.json().then(json => {
    //       const errors = json.errors ? json.erros : {};
    //       errors.summary = json.message;
    //       this.setState({errors});
    //     });
    //   }
    // });
  }

  changeState(event){
      const field = event.target.name;
      const house = event.target.house;
      house[field] = event.target.value;
      this.setState({house});
  }


  render() {
    return  (
      <HouseForm
       onSubmit={this.processForm}
       onChange={this.changeState}
       house={this.state.house}
      />
    );
  }
}

// // To make react-router work
// HousePage.contextTypes = {
//   router: PropTypes.object.isRequired
// };

export default HousePage;