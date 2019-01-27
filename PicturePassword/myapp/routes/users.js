var express = require('express');
var router = express.Router();
var somemod = require("../somemod");

/* GET users listing. */
router.get('/:thing1/:thing2/:thing3/:thing4/:thing5', function(req, res, next) {

    console.log('The params:', req.params);
    //console.log("This is returned" + somemod.someMod());
    somemod.someMod(req.params)
    .then((ret)=>{
        res.send(ret);
    }).catch((err)=>{
        console.error(`You done messed up! ${err}`);
        res.end();
    });
    //res.send("Done");
});

module.exports = router;
