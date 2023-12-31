from rolepermissions.roles import AbstractUserRole


class Devops(AbstractUserRole):
    available_permissions = {
        'add_temporary_user': True,

        'read_service': True,
        'add_service': True,
        'delete_service': True,

        'read_remote': True,
        'add_remote': False,
        'delete_remote': False,

        'read_project': True,
        'add_project': False,
        'delete_project': False,

        'read_device': True,
        'add_device': False,
        'delete_device': False,

        'read_log': True,
        'add_log': True,
        'delete_log': True,
    }
