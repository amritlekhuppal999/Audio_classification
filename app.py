# from flask import Flask
from flask import render_template, Flask, request, jsonify, redirect, make_response

import math

app = Flask(__name__)

# from app import routes

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload_media', methods=['POST'])
def json_endpoint():
    # req = request.get_json()
    
    # print(media_file.content_length)
    # If content_length is returning 0, it might be due to the fact that Flask doesn't automatically populate the content_length attribute for file uploads in all cases. The content_length attribute is populated based on the Content-Length header of the HTTP request, and in some cases, it might not be available or accurate for file uploads.

    # Instead of relying on content_length for file size, you can use the stream attribute to read the content and determine the size programmatically. 
    try:
        if 'media_file' in request.files:
            media_file = request.files['media_file']
            action = request.form['action']

            media_file.save('Uploads/'+media_file.filename)
            # using it after media_file.read() is causing issue as the uploaded file does appears corrupted or empty binary txt files. So using it earlier

            # res = make_response(jsonify({"message": "JSON received"}), 200)
            file_content = media_file.read()
            file_size = len(file_content)
            # file_size = round(math.floor(file_size/(1000*1000)), 1)
            file_size_str = round(file_size/(1000*1000), 1)
            
            response = {
                "message": "Got your file, its processed and uploaded.",
                "filename": media_file.filename,
                "mime": media_file.content_type,
                "size": str(file_size_str) + " MB",
            }
        
        return make_response(jsonify(response), 200)
    
    except IOError as e:
        # Handle file save failure
        error_message = {"error": f"Failed to save file. Reason: {str(e)}"}
        return jsonify(error_message), 500

    except Exception as e:
        # Handle any other exceptions
        error_message = {"error": str(e)}
        return jsonify(error_message), 400

if __name__ == '__main__':
    app.run(debug=True)
