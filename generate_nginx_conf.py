#!/Users/nabetama/.pyenv/shims/python
# coding: utf-8
import os
import sys
import yaml
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
template = env.get_template('./library/vhost.conf.j2')


class Vhost(object):
    def __init__(self, **args):
        for k, v in args.items():
            self.__dict__[k] = v

def get_conf_path(fqdn):
    cwd = os.getcwd()
    fpath = os.path.join(cwd, 'roles/nx/files/{}.conf'.format(fqdn))
    return fpath


def main():
    module = AnsibleModule(
        argument_spec=dict(
            maintenance=dict(type='bool'),
            fqdn=dict(type='str'),
            app=dict(type='str'),
        ),
        supports_check_mode=True,
    )
    try:
        vhost = Vhost(
            maintenance=module.params['maintenance'],
            fqdn=module.params['fqdn'],
            app=module.params['app'],
        )
        nginx_config = template.render(vhost=vhost)

        if module.check_mode:
            module.exit_json(changed=False,
                             msg='Generated nginx conf: {}.conf'.format(module.params)
                             )

        fpath = get_conf_path(module.params['fqdn'])
        with open(fpath, 'w+') as dest:
            dest.write(nginx_config.encode('utf-8'))
        module.exit_json(changed=True,
                         msg='Generated nginx conf: {}.conf, params are {}'.format(
                             module.params['fqdn'],
                             module.params,
                         ))
    except Exception as e:
        module.fail_json(msg='error occured {}'.format(e))


from ansible.module_utils.basic import *
main()
