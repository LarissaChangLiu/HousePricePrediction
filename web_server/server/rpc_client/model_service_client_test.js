var client = require('./model_service_client');
var house = {
    "flooring": 1,
    "fencing": 1,
    "baths": 2,
    "beds": 3,
    "zip_code":75035,
    "built_yr":1998,
    "gutters": 1,
    "sqft":2000
}
// Invoke "getPrediction"
client.getPrediction(house, function(response) {
  console.assert(response != null);
});
