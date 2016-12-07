/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

$("#file").on("change", function() {
    
    $.each($('#file')[0].files, function(i, file) {

        console.log(file);

        var fr = new FileReader(); //Create file reader object
        
        fr.onload = function () {

            //Put the loaded image in the screen
            document.getElementById("img-container").src = fr.result;
            
            //Verify the size of the file is bigger than 250kb
            if(file.size > 500000) {
                
                //Calc the reduction factor of the image
                var reducFactor = file.size / 250000;
                
                console.log(reducFactor);
                
                //Resize image so the server can handle it proper
                imageResize(fr.result, reducFactor, function(img) {
                    
                    console.log("File reduced...");
                    console.log(img);             
                    
                    sendImageBlob(img); 

                });
                
            } else { //If no need of resize is need, just send the file
                console.log("File not reduced...");
                sendImageBlob(file);  
            }                    
        }
        
        fr.readAsDataURL(file);
    });
    
});


function imageResize (imgSrc, factor, callback) {
    
    var image = new Image();
    image.src = imgSrc;
    
    mainCanvas = document.createElement("canvas");
    mainCanvas.width = image.width / factor;
    mainCanvas.height = image.height / factor;
    var ctx = mainCanvas.getContext("2d");
    ctx.drawImage(image, 0, 0, mainCanvas.width, mainCanvas.height);
           
           
           
           

    
    

   
    

    //size = parseInt($('#size').get(0).value, 10);
    
    //while (mainCanvas.width > size) {
        //mainCanvas = halfSize(mainCanvas);
    //}
    console.log([mainCanvas]);
    //return mainCanvas.toDataURL("image/jpeg");
    mainCanvas.toBlob(callback, "image/jpeg", 1);
    
}

/*
    * Draw initial canvas on new canvas and half it's size
    */
var halfSize = function (i) {
    var canvas = document.createElement("canvas");
    canvas.width = i.width / 2;
    canvas.height = i.height / 2;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(i, 0, 0, canvas.width, canvas.height);
    return canvas;
};




function sendImageBlob(imageData) {
   
   var formData = new FormData();
   formData.append("file", imageData);
   
   $.ajax({
        url: 'upload',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        success: function(data){
            console.log(data);
            var dataObj = JSON.parse(data);

            //console.log("Data Received!");
            //console.log(dataObj);

            desenhar(dataObj);
        }
    });   
    
}
