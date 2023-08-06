import os
from flask import Flask, request

meditorFilesRoot = "pypanelFiles/meditor"
app = Flask(__name__)
@app.route("/save-file", methods=['POST'])
def saveFile():
    requestData = request.get_json()
    fileData = requestData['fileContent']
    fileName = requestData['fileName']

    os.makedirs(meditorFilesRoot, exist_ok=True)

    with open(f'{meditorFilesRoot}/{fileName}', 'w') as file:
        file.write(fileData)
        file.close()

    print("File is saved in:")
    print()
    print(f'{meditorFilesRoot}/{fileName}')
    print()
    return 'File Is Saved.'