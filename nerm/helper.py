from index import ALLOWED_EXTENSIONS
import os
from werkzeug.utils import secure_filename
import traceback
import shutil
from pathlib import Path



MASKING_TEXT_FILE = "data.txt"
ALLOWED_EXTENSIONS = ['txt']

def expected_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload(files, upload_directory):
    directory = upload_directory + "/deploy/"
    os.makedirs(directory, exist_ok=True)
    for file in files:
        if file and expected_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(directory, filename))
        else:
            raise ValueError("Exception occurred in finding files with allowed extension!")
    print("Files are uploaded successfully!")

def upload_text(text, upload_directory):
    directory = upload_directory + "/deploy/"
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, MASKING_TEXT_FILE), "w") as text_file:
        text_file.write(text)

def truncate_files(directory):
    try:
        filenames = [ f for f in os.listdir(directory)]
        for filename in filenames:
            path = os.path.join(directory, filename)
            if os.path.isfile(path) or os.path.islink(path):
                # remove file
                os.remove(path)
            elif os.path.isdir(path):
                # remove directory and all its content
                shutil.rmtree(path)
        print("Files are deleted successfully at ", directory)
    except:
        traceback.print_exc()
        print ("Error occurred in deleting the files at ", directory)

def truncate_ann_file(directory):
    filenames = [ f for f in os.listdir(directory) if f.endswith(".ann")]
    for filename in filenames:
        os.remove(os.path.join(directory, filename))
    print("Files are deleted successfully!")

def truncate(upload_directory, download_directory, intermediate_directory):
    truncate_files(upload_directory)
    truncate_files(download_directory)
    truncate_files(intermediate_directory)

def get_zip_file(directory):
    truncate_ann_file(directory)
    return shutil.make_archive("masked", 'zip', directory)

def get_masked_text(directory):
    filepath = os.path.join(directory, MASKING_TEXT_FILE)
    text_file = Path(filepath)
    if text_file.is_file():
        with open(filepath) as f:
            masked_text = f.read()
            return masked_text
    else:
        raise ValueError("Error occurred in masking given text")


