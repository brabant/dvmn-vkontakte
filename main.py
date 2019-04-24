import os
import requests
from random import randint
from dotenv import load_dotenv


class VkResponseError(BaseException):
    pass


def download_file(url, filename):
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)
        return filename


def download_random_xkcd_comics():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    max_comics_id = response.json()['num']
    random_comics_id = randint(1, max_comics_id)

    url = f'https://xkcd.com/{random_comics_id}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()

    url = response.json()['img']
    filename = '{}.{}'.format(response.json()['num'], url.split('.')[-1])
    return download_file(url, filename), response.json()['alt']


def raise_for_error(response):
    response.raise_for_status()
    try:
        raise VkResponseError(response.json()['error']['error_code'], response.json()['error']['error_msg'])
    except KeyError:
        pass


def vk_request(http_method, vk_method, **kwargs):
    url = f'https://api.vk.com/method/{vk_method}'
    response = getattr(requests, http_method)(url, **kwargs)
    raise_for_error(response)
    return response.json()


def get_vk_groups(access_token):
    params = {'access_token': access_token,
              'v': '5.95'}
    return vk_request('get', 'groups.get', params=params)


def get_vk_upload_link(access_token, group_id):
    params = {'access_token': access_token,
              'group_id': group_id,
              'v': '5.95'}
    return vk_request('get', 'photos.getWallUploadServer', params=params)


def upload_file_vk(access_token, group_id, filepath, caption):
    upload_server = get_vk_upload_link(access_token, group_id)['response']

    with open(filepath, 'rb') as file:
        files = {'photo': file}
        response = requests.post(upload_server['upload_url'], files=files)

    raise_for_error(response)
    response_data = response.json()
    if not response_data['photo']:
        raise VkResponseError(0, 'Photo upload error')

    data = {'access_token': access_token,
            'user_id': upload_server['user_id'],
            'group_id': group_id,
            'photo': response_data['photo'],
            'server': response_data['server'],
            'hash': response_data['hash'],
            'caption': caption,
            'v': 5.95}

    return vk_request('post', 'photos.saveWallPhoto', data=data)


def vk_wall_post(access_token, owner_id, from_group, attachments, message):
    params = {'access_token': access_token,
              'owner_id': owner_id,
              'from_group': from_group,
              'attachments': attachments,
              'message': message,
              'v': 5.95}

    return vk_request('get', 'wall.post', params=params)


def main():
    load_dotenv()
    access_token = os.getenv('VK_ACCESS_TOKEN')
    group_id = os.getenv('VK_GROUP_ID')
    (filepath, caption) = download_random_xkcd_comics()

    response = upload_file_vk(access_token, group_id, filepath, caption)['response'][0]
    vk_wall_post(access_token, f'-{group_id}', 1, 'photo{}_{}'.format(response['owner_id'], response['id'], ), caption)

    print('Random XKCD comics published successfully')
    os.unlink(filepath)
    exit(0)


if __name__ == '__main__':
    main()
