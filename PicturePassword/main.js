function saveItems(){
    console.log("Submit button was hit")
    var i1 = document.getElementById("item1").value;
    var i2 = document.getElementById("item2").value;
    var i3 = document.getElementById("item3").value;
    var i4 = document.getElementById("item4").value;
    var i5 = document.getElementById("item5").value;
    var items = [i1, i2, i3, i4, i5]

    localStorage.setItem("item1", i1)
    localStorage.setItem("item2", i2)
    localStorage.setItem("item3", i3)
    localStorage.setItem("item4", i4)
    localStorage.setItem("item5", i5)

    var allInputs = document.getElementById("allInput");
    allInputs.parentNode.removeChild(allInputs);
    var para = document.createElement("P");                       // Create a <p> node
    var t = document.createTextNode("Thank you, your items have been saved.");      // Create a text node
    para.appendChild(t);                                       // Append the text to <p>
    document.getElementById("itemAddSuccess").appendChild(para);           // Append <p> to <div> with id="myDIV"

    // Create a request variable and assign a new XMLHttpRequest object to it.
    var request = new XMLHttpRequest();

    var randomObjects = ['Gatorade', 'Bevo', 'Vodka', 'Aluminum', 'Chair'];

    // Open a new connection, using the GET request on the URL endpoint
    //http://localhost:3000/users/:thing1/:thing2/:thing3/:thing4/:thing5
    request.open('GET', 'http://localhost:3000/users/:' + items[Math.floor(Math.random() * items.length)] + "/:" + randomObjects[Math.floor(Math.random() * randomObjects.length)] +
    "/:" + items[Math.floor(Math.random() * items.length)] + "/:" + randomObjects[Math.floor(Math.random() * randomObjects.length)] + "/:" + items[Math.floor(Math.random() * items.length)], true);

    request.onload = function () {
        // Begin accessing JSON data here
        // Begin accessing JSON data here
        var data = JSON.parse(this.response);
        console.log(data)

        for (let index = 0; index < data.length; index++) {
            console.log(data[index]);
            var myImage = new Image(200, 200);
            myImage.src = data[index];
            myImage.id = "item"+index;
            document.getElementById("generatePic").appendChild(myImage);
        }
    }
    // Send request
    request.send();

    var howManyMissingDiv = document.getElementById("howManyMissing");
    howManyMissingDiv.style.display = "flex";
}

function onLoadFunc(){
    if(localStorage.getItem("item1") != null){
        var allInputs = document.getElementById("allInput");
        allInputs.parentNode.removeChild(allInputs);
        var para = document.createElement("P");                       // Create a <p> node
        var t = document.createTextNode("Thank you, your items have been saved.");      // Create a text node
        para.appendChild(t);                                       // Append the text to <p>
        document.getElementById("itemAddSuccess").appendChild(para);           // Append <p> to <div> with id="myDIV"
    }
}