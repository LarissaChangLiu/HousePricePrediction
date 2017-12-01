var bodyParser = require('body-parser');
var express = require('express');
var path = require('path');
var index = require('./routes/index');
var house = require('./routes/house');

var app = express();
app.use(bodyParser.json());
// view engine setup
app.set('views', path.join(__dirname, '../client/build'));
app.set('view engine', 'jade');
//important 
app.use('/static', express.static(path.join(__dirname, '../client/build/static')));
app.all('*', function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  next();
});
app.use('/', index);
app.use('/house', house);
app.use(function(req, res, next) {
  res.status(404);
});


module.exports = app;
