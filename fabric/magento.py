import re
from fabric.api import env, run, hide, task
from envassert import detect, file, port, process, service, user
from hot.utils.test import get_artifacts


def magento_is_responding():
    with hide('running', 'stdout'):
        wget_cmd = ("wget --quiet --output-document - "
                    "--header='Host: example.com' http://localhost/")
        homepage = run(wget_cmd)
        if re.search('Magento Demo Store', homepage):
            return True
        else:
            return False


@task
def check():
    env.platform_family = detect.detect()

    # web server is listening
    assert port.is_listening(80), 'Web port 80 is not listening'

    # redis is listening
    assert port.is_listening(6379), 'Redis port 6379 is not listening'
    assert port.is_listening(6380), 'Redis port 6380 is not listening'
    assert port.is_listening(6381), 'Redis port 6381 is not listening'

    # nginx user is created
    assert user.exists("nginx"), 'nginx user does not exist'
    
    if (env.platform_family == "rhel"):
        assert process.is_up('nginx'), 'nginx is not running'
        assert process.is_up('php-fpm'), 'php-fpm is not running'
        assert service.is_enabled('nginx'), 'nginx is not enabled'
        assert service.is_enabled('php-fpm'), 'php-fpm is not enabled'
    elif (env.platform_family == 'debian'):
        assert process.is_up('nginx'), 'nginx is not running'
        assert process.is_up('php5-fpm'), 'php-fpm is not running'
        assert service.is_enabled('nginx'), 'nginx is not enabled'
        assert service.is_enabled('php5-fpm'), 'php-fpm is not enabled'

    # magento main page is available
    assert magento_is_responding(), 'Magento did not respond as expected.'


@task
def artifacts():
    env.platform_family = detect.detect()
    get_artifacts()
