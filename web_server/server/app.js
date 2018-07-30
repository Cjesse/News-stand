var cors = require('cors');

var passport = require('passport');

var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var authRouter = require('./routes/auth');
var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');
var newsRouter = require('./routes/news');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, '../client/build'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// app.all('*', function(req, res, next) {
// 	res.header("Access-Control-Allow-Origin", "*");
// 	res.header("Access-Control-Allow-Headers", "X-Requested-With");
// 	next();
// });

// TODO: remove this after development is done
app.use(cors());

var config = require('./config/config.json');
require('./models/main.js').connect(config.mongoDbUri);

app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

// pass the authentication checker middleware
const authCheckMiddleware = require('./middleware/auth_checker');
app.use('/news', authCheckMiddleware);

app.use('/', indexRouter);
app.use('/auth', authRouter);
app.use('/news', newsRouter);

// catch 404 and forward to error handler
app.use(function(req, res) {
  var err = new Error('Not Found');
  err.status = 404;
  res.send('404 Not Found');
});

// // catch 404 and forward to error handler
// app.use(function(req, res, next) {
//   next(createError(404));
// });

// // error handler
// app.use(function(err, req, res, next) {
//   // set locals, only providing error in development
//   res.locals.message = err.message;
//   res.locals.error = req.app.get('env') === 'development' ? err : {};

//   // render the error page
//   res.status(err.status || 500);
//   res.render('error');
// });

module.exports = app;
