const express = require('express')
const cors = require('cors');

var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var somemod = require("./somemod");

const app = express()
const port = 3000;

var usersRouter = require('./routes/users');

app.use(cors());
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));


app.use('/users', usersRouter);
app.get('/', (req, res) =>{
res.send({ message: 'hey' });})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))