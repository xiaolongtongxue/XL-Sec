import json
import os
from flask import Blueprint, request, Response
from werkzeug.utils import secure_filename

from config import TEMPLATE_FOLDER, UPLOAD_LOG_PATH

API_rules_uploader = Blueprint('RulesUploader', __name__, template_folder=TEMPLATE_FOLDER)


@API_rules_uploader.route('/rules/uploader/', methods=['POST'])
def uploader():
    # f = request.files['file']
    # print(request.files)
    # f.save(os.path.join(UPLOAD_LOG_PATH, secure_filename(f.filename)))
    # import subprocess
    # subprocess.run(["pwd"])
    return "ok"
