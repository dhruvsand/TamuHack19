'use strict';

const https = require('https');

module.exports = {

    someMod: (params) => {

        return new Promise((resolve, reject)=>{
            
            let callGroup = [
                callBing(params.thing1),
                callBing(params.thing2),
                callBing(params.thing3), 
                callBing(params.thing4), 
                callBing(params.thing5)
            ];


            Promise.all(callGroup).then((vals)=>{
                resolve(vals);
            })
        })
    }
};

function callBing(itemVal){
    return new Promise((resolve, reject)=>{
        let subscriptionKey = '337922ed05b543d58c014c32c086a960';

    let host = 'api.cognitive.microsoft.com';
    let path = '/bing/v7.0/images/search';

    let term = itemVal;

    let response_handler = function (response) {
        let body = '';
        response.on('data', function (d) {
            body += d;
        });
        response.on('end', function () {
            let imageResults = JSON.parse(body);
            if (imageResults.value.length > 0) {
                let firstImageResult = imageResults.value[0];
                resolve(firstImageResult.contentUrl);
            }
            else {
                console.log("Couldn't find image results!");
                reject('Error!');
            }
    });
        response.on('error', function (e) {
            console.log('Error: ' + e.message);
        });
    };

    let bing_image_search = function (search) {
    console.log('Searching images for: ' + term);
    let request_params = {
            method : 'GET',
            hostname : host,
            path : path + '?q=' + encodeURIComponent(search),
            headers : {
                'Ocp-Apim-Subscription-Key' : subscriptionKey,
            }
        };

        let req = https.request(request_params, response_handler);
        req.end();
    }

    if (subscriptionKey.length === 32) {
        bing_image_search(term);
    } else {
        console.log('Invalid Bing Search API subscription key!');
        console.log('Please paste yours into the source code.');
    }
    })

}