/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

hideSvg();

$("#file").on("change", function() {
    
    hideSvg();
    
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
                imageResize(fr.result, reducFactor, function(reducedFile) {
                    
                    console.log("File reduced...");      
                    
                    sendImageBlob(reducedFile); 

                });
                
            } else { //If no need of resize is need, just send the file
                console.log("File not reduced...");
                sendImageBlob(file);  
            }                    
        }
        
        fr.readAsDataURL(file);
    });
    
});

function hideSvg() {
    $("#svg-container").hide();
}

function showSvg() {
    $("#svg-container").show();
}


function imageResize (imgSrc, factor, callback) {
    
    var newImage = new Image();
    
    newImage.onload = function() {
        
        mainCanvas = document.createElement("canvas");
        mainCanvas.width = newImage.width / factor;
        mainCanvas.height = newImage.height / factor;
        var ctx = mainCanvas.getContext("2d");
        ctx.drawImage(newImage, 0, 0, mainCanvas.width, mainCanvas.height);
    
        mainCanvas.toBlob(callback, "image/jpeg", 0.5);       
    }
    
    newImage.src = imgSrc;
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
            
            desenhar(dataObj);
            
            if(dataObj['faces'].length > 0)
                showSvg()
        }
    });   
    
}
