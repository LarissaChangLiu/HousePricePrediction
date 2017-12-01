var jayson = require('jayson');

// create a client
var client = jayson.client.http({
  port: 6060,
  hostname: 'localhost'
});

function getPrediction(house, callback) {
  client.request('prediction', [house], function(err, error, response) {
    if (err) throw err;
    console.log(response);
    callback(response);
  });
}

module.exports = {
  getPrediction : getPrediction,
};