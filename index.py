from flask import Flask, request, send_file, Response
from flask_cors import CORS
from nerm import nerm
from nerm import helper
from nerm.configuration import Configuration
import traceback



cf = Configuration()
ALLOWED_EXTENSIONS = {'txt'}
UPLOAD_FOLDER = cf.input_file_location
DOWNLOAD_FOLDER = cf.output_file_location


app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, NERM!>"


@app.route("/mask-files", methods=['POST'])
def upload_files():
    if 'files' in request.files:
        zipfile = None
        try:
            files = request.files.getlist('files')
            print (files)
            helper.upload(files, UPLOAD_FOLDER)
            zipfile = nerm.call_nerm(UPLOAD_FOLDER, DOWNLOAD_FOLDER, True)
        except Exception as e:
            traceback.print_exc()
            helper.truncate(UPLOAD_FOLDER, DOWNLOAD_FOLDER, cf.mask_input_file_location)
            return Response("Exception occurred in processing nerm:\n" + str(e), status="500 INTERNAL_SERVER_ERROR")
        
        helper.truncate(UPLOAD_FOLDER, DOWNLOAD_FOLDER, cf.mask_input_file_location)
        return send_file(zipfile, mimetype = 'application/zip', as_attachment = True, download_name='masked.zip')
    return Response("File not found", status="BAD REQUEST")

@app.route("/mask-text", methods=['POST'])
def upload_text():
    text = request.form.get("text")
    if (text):
        masked_text = None
        try:
            helper.upload_text(text, UPLOAD_FOLDER)
            masked_text = nerm.call_nerm(UPLOAD_FOLDER, DOWNLOAD_FOLDER, False)
        except Exception as e:
            traceback.print_exc()
            helper.truncate(UPLOAD_FOLDER, DOWNLOAD_FOLDER, cf.mask_input_file_location)
            return Response("Exception occurred in processing nerm:\n" + str(e), status="INTERNAL_SERVER_ERROR")
        
        helper.truncate(UPLOAD_FOLDER, DOWNLOAD_FOLDER, cf.mask_input_file_location)
        return Response(masked_text, status="OK")
    return Response("Text not found, please enter the text to be masked!", status="400 BAD REQUEST")

if __name__ == '__main__':
    app.run(debug=True)
