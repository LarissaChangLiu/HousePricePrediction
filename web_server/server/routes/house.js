var express = require('express');
var rpc_client = require('../rpc_client/model_service_client');
var router = express.Router();

router.post('/getPrediction', function(req, res, next) {
  console.log(req.body);
  var house = {
      'flooring': req.body.flooring,
      'fencing': req.body.fencing,
      'baths': req.body.baths,
      'beds': req.body.beds,
      'zip_code': req.body.zip_code,
      'built_yr': req.body.built_yr,
      'gutters': req.body.gutters,
      'sqft': req.body.sqft
  }
  rpc_client.getPrediction(house, function(response) {
    res.json({'price': response})
  });
});

module.exports = router;