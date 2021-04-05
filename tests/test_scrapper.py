import json


def test_getting_text(test_app):
    resp = test_app.get('/get_text', data=json.dumps({'url': 'http://127.0.0.1:5000/'}),
                        headers={'Content-Type': 'application/json'})
    json_data = json.loads(resp.data)
    assert resp.status_code == 200
    assert json_data["success"] is True
    assert json_data['msg'] == 'Text saved in the system successfully.'


def test_getting_images(test_app):
    resp = test_app.get('/get_images', data=json.dumps({'url': 'http://127.0.0.1:5000/'}),
                        headers={'Content-Type': 'application/json'})
    json_data = json.loads(resp.data)
    assert resp.status_code == 200
    assert json_data["success"] is True
    assert json_data['msg'] == 'Images saved in the system.'


def test_download_text(test_app):
    resp = test_app.get('/download_text')
    json_data = json.loads(resp.data)
    assert resp.status_code == 200
    assert json_data["success"] is True
    assert json_data['msg'] == 'Text downloaded.'


def test_download_img(test_app):
    resp = test_app.get('/download_images')
    json_data = json.loads(resp.data)
    assert resp.status_code == 200
    assert json_data["success"] is True
    assert json_data['msg'] == 'Images downloaded.'





