import traceback

from flask import Flask, Response, request, send_file, render_template, after_this_request, redirect
import os

from mosaic.mosaic import create_gradient, create_simple_gradient
from util.logs import get_logger
from mosaic import create_mosaic, creat_mosaic_gif
from data.loader import get_loader, Loader
from data.db import DBClient
from mosaic import batch_preprocess
import os
from mosaic.mosaic import create_mosaic
from werkzeug.contrib.fixers import ProxyFix

from util.translit import to_latin

LOGGER = get_logger('APP')
THIS_FILE_PATH = os.path.join(os.path.dirname(__file__))
FILE_BUFFER_PATH = THIS_FILE_PATH + "/file_buffer"

THIS_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
dbClient: DBClient = DBClient()

app = Flask(__name__)


def get_tags():
    """
    :return: list of allow tags
    """
    return dbClient.get_tags()

# достает из запроса тег и если нужно, выгружает картинки по тегу
def extract_tag_resources_path(request) -> str:
    """
    :param request:
    :return: path with tag sources
    """
    if 'tags' in request.form and len(request.form['tags']) > 0:
        tag = request.form['tags']
    # if new phrase - it'll be theme_tag
    if 'phrase' in request.form and len(request.form['phrase']) > 0:
        tag = request.form['phrase']
    # latinise tag
    eng_tag = to_latin(tag)
    tags = get_tags()

    # если тег новый,
    if eng_tag not in tags:
        LOGGER.debug("Create new theme_tag : " + eng_tag)

        loader: Loader = get_loader()
        results_path: str = loader.load(eng_tag, tag, 15)
        # path to source images of this tag
        tag_path = results_path
        LOGGER.debug("Result path: " + results_path)
        LOGGER.debug("Batch images")
        batch_preprocess(results_path)
        LOGGER.debug("Batch ok")
        LOGGER.debug("Add to DB")
        dbClient.upload_path(eng_tag, results_path)
        LOGGER.debug("Add to DB OK")
    else:
        tag_path = dbClient.get_source_path(eng_tag)

    return tag_path


# СОЗДАЕТ КАРТИНКУ С МОЗАЙКОЙ
@app.route('/make_mosaic', methods=["POST"])
def make_mosaic():
    try:
        if "file" not in request.files:
            json_result = str({"Exception": "Need to add file to request"})
            return Response(response=json_result, status=400)

        f = request.files['file']
        file_name = f.filename

        tag_path = extract_tag_resources_path(request)

        file_path = os.path.join(FILE_BUFFER_PATH, file_name)
        f.save(file_path)

        create_mosaic(
            img_path=file_path,
            source_dirs=tag_path,
            target_path=file_path,
            is_preprocess=True
        )

        LOGGER.debug("Return movie.gif")
        return send_file(file_path,
                         as_attachment=True,
                         attachment_filename="mosaic.jpg")

    except Exception as e:
        LOGGER.error("Exception:"+ str(e))
        json_result = str({"Exception": str(e)})
        return Response(response=json_result, status=500)

# СОЗДАЕТ ГИФКУ
@app.route('/make_gif', methods=["POST"])
def make_gif():
    try:
        if "file" not in request.files:
            json_result = str({"Exception": "Need to add file to request"})
            return Response(response=json_result, status=400)

        f = request.files['file']
        file_name = f.filename

        tag_path = extract_tag_resources_path(request)

        file_path = os.path.join(FILE_BUFFER_PATH, file_name)
        f.save(file_path)

        creat_mosaic_gif(
            img_path=file_path,
            source_dirname=tag_path,
            target_dir=FILE_BUFFER_PATH,
            target_name="movie.gif"
        )
        return send_file(os.path.join(FILE_BUFFER_PATH, "movie.gif"),
                         as_attachment=True,
                         attachment_filename="mosaic.gif")

    except Exception as e:
        LOGGER.error("Exception:"+ str(e))
        json_result = str({"Exception": str(e)})
        return Response(response=json_result, status=500)

# СОЗДАЕТ КАРТИНКУ С ГРАДЕНТОМ
@app.route('/make_gradient', methods=["POST"])
def make_gradient():
    try:
        if "file" not in request.files:
            json_result = str({"Exception": "Need to add file to request"})
            return Response(response=json_result, status=400)

        f = request.files['file']
        file_name = f.filename

        tag_path = extract_tag_resources_path(request)

        file_path = os.path.join(FILE_BUFFER_PATH, file_name)
        res_path = os.path.join(FILE_BUFFER_PATH, "file.jpg")
        f.save(file_path)
        create_simple_gradient(
            img_path=file_path,
            source_dirname=tag_path,
            target_name=res_path
        )
        return send_file(res_path,
                         as_attachment=True,
                         attachment_filename="file.jpg")

    except Exception as e:
        LOGGER.error("Exception:"+ str(e))
        json_result = str({"Exception": str(e)})
        return Response(response=json_result, status=500)


@app.route('/')
def get_form():
    return render_template("upload.html", tags=get_tags())


if __name__ == "__main__":
    # gunicorn -b 0.0.0.0:8034 server:app

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host='0.0.0.0', debug=True)

