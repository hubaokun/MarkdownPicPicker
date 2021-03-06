from qiniu import Auth, put_file, BucketManager
import os
import sys


class Uploader(object):
    def __init__(self, config_info):
        self.upload_handler = None
        self.url = config_info['url']
        self.container_name = config_info.get('container_name')
        self.upload_handler = Auth(config_info.get('access_key'), config_info.get('secret_key'))

    def upload(self, picture_path_list, link_only=False):
        if self.upload_handler:
            success_uploaded_list = []
            for picture_path in picture_path_list:
                picture_name = os.path.basename(picture_path)
                token = self.upload_handler.upload_token(self.container_name, picture_name, 3600)
                ret, info = put_file(token, picture_name, picture_path)
                bucket = BucketManager(self.upload_handler)
                success = bucket.stat(self.container_name, picture_name)
                print(success)
            self.write_markdown_picture_url(picture_path_list, link_only)

    def write_markdown_picture_url(self, picture_path_list, link_only=False):
        uploaded_url_list = []
        for picture_path in picture_path_list:
            picture_name = os.path.basename(picture_path)
            if link_only:
                markdown_picture_url = self.url.format(picture_name)
                uploaded_url_list.append(markdown_picture_url)
            else:
                markdown_picture_url = '![]({})'.format(self.url.format(picture_name))
                uploaded_url_list.append(markdown_picture_url)
        platform = sys.platform
        command = ''
        if platform == 'win32':
            command = 'echo {} | clip'.format('\n'.join(uploaded_url_list))
        elif platform == 'darwin':
            command = 'echo "{}" | pbcopy'.format('\n'.join(uploaded_url_list))
        os.system(command)
        print('the url is already in your clipboard!')

if __name__ == '__main__':
    config_info = {
        'url': 'http://7sbpmp.com1.z0.glb.clouddn.com/{}',
        'access_key': 'Q6sS422O0asdffd5aVqM3FsdfdfpF36tqvyQ75Zvzw',
        'secret_key': '6QtAqqTfasdZP - 2uoXsdfaeeLX2CCmoOaB2aLObM',
        'container_name': 'picturebed'
    }
    uploader = Uploader(config_info)
    uploader.upload('1.png')
