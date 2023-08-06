import os

from uhugo.post_install.detect_providers import check_hugo_file, check_providers_fs, Provider


def test_check_hugo_file_toml():
    assert check_hugo_file() == Provider(name='cloudflare', project='gollahalli-com', file_name=None,
                                         api_key='env:cloudflare_key', account_id='env:cloudflare_account_id',
                                         email_address='env:cloudflare_email', path=None)


def test_check_hugo_file_yaml():
    os.remove(os.path.join(os.getcwd(), 'config.toml'))
    assert check_hugo_file() == Provider(name='cloudflare', project='gollahalli-com', file_name=None,
                                         api_key='env:cloudflare_key', account_id='env:cloudflare_account_id',
                                         email_address='env:cloudflare_email', path=None)


def test_check_hugo_file_no_file():
    os.remove(os.path.join(os.getcwd(), 'config.yaml'))
    assert check_hugo_file() == Provider()


def test_check_providers_fs():
    assert check_providers_fs() == [Provider(name='vercel', project=None, file_name=None, api_key=None, account_id=None,
                                             email_address=None, path=os.path.join(os.getcwd(), 'vercel.json')),
                                    Provider(name='netlify', project=None, file_name=None, api_key=None,
                                             account_id=None, email_address=None, path=os.path.join(os.getcwd(),
                                                                                                    'netlify.toml'))]
