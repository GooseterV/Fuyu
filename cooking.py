import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/upload')
def index():

	return r"""
    <style>
	    @import url('https://fonts.googleapis.com/css2?family=Baloo+Bhai+2&family=Noto+Sans+JP&family=Red+Hat+Display:wght@300&display=swap');
	    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@100&family=Montserrat:wght@300;500&display=swap');
	    * {
		    font-family:"Montserrat";
	    }
     
        #upload_widget {
            position:absolute;
            top:50%;
            left:50%;
            transform:translate(-50%, -50%);
        }
    </style>

    <button id="upload_widget" class="cloudinary-button">Upload files</button>

    <script src="https://upload-widget.cloudinary.com/global/all.js" type="text/javascript"></script>  

    <script type="text/javascript">  
        var myWidget = cloudinary.createUploadWidget({
	        cloudName: 'gooseterv', 
	        uploadPreset: 'lt62f4ih'}, (error, result) => { 
	    if (!error && result && result.event === "success") { 
		    console.log('Done! Here is the image info: ', result.info); 
	    }
    })

    document.getElementById("upload_widget").addEventListener("click", function(){
	    myWidget.open();
    }, false);
    </script>
    """


if __name__ == "__main__":
	app.run(debug=True)