from asyncio import run

from flask import Blueprint, make_response, render_template, request

from logic.scrapper_logic import extract_text, extract_images, get_page_content, save_images, save_text


scrapper_bp = Blueprint('scrapper_bp', __name__)

scrapper_bp.texts_csv = ''
scrapper_bp.img_links = []


@scrapper_bp.route('/')
def home_page():
    """
    :return: home page including few different tags with text and images
    """
    return render_template('home.html', title='Home')


@scrapper_bp.route('/get_text')
def get_page_text():
    """
    The function reads page url from json object passed from the client.
    Next it extracts text from the page and saves it in memory
    :return: response informing about success or failure.
    """
    data = request.json
    page_url = data['url']
    try:
        page_content = get_page_content(page_url)
        result = extract_text(page_content)
        scrapper_bp.texts_csv = result
        return make_response({'success': True, 'msg': 'Text saved in the system successfully.'}, 200)
    except Exception as error:
        err = 'Something went wrong.'
        return make_response({'success': False, 'err': err, 'error': error}, 500)


@scrapper_bp.route('/get_images')
def get_page_images():
    """
    The function reads page url from json object passed from the client.
    Next it extracts image urls from the page and save them in memory
    :return: response informing about success or failure.
    """
    data = request.json
    page_url = data['url']
    try:
        page_content = get_page_content(page_url)
        result = extract_images(page_content, data['url'])
        scrapper_bp.img_links = result
        return make_response({'success': True, 'msg': 'Images saved in the system.'}, 200)
    except Exception:
        err = 'Something went wrong.'
        return make_response({'success': False, 'err': err}, 500)


@scrapper_bp.route('/download_text')
def download_text():
    """
    Function saves text saved in memory to .csv file.
    :return: response informing about success or failure.
    """
    try:
        save_text(scrapper_bp.texts_csv)
        return make_response({'success': True, 'msg': 'Text downloaded.'}, 200)
    except Exception:
        return make_response({'success': False, 'msg': 'Something went wrong.'}, 500)


@scrapper_bp.route('/download_images')
def download_img():
    """
    Function saves images from memory to .jpeg files.
    :return: response informing about success or failure.
    """
    try:
        run(save_images(scrapper_bp.img_links))
        return make_response({'success': True, 'msg': 'Images downloaded.'}, 200)
    except Exception:
        return make_response({'success': False, 'msg': 'Something went wrong.'}, 500)
