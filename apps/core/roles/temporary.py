from rolepermissions.roles import AbstractUserRole


class Temporary(AbstractUserRole):
    available_permissions = {
        'add_temporary_user': False,

        'read_service': True,
        'add_service': False,
        'delete_service': False,

        'read_remote': True,
        'add_remote': False,
        'delete_remote': False,

        'read_project': True,
        'add_project': False,
        'delete_project': False,

        'read_device': False,
        'add_device': False,
        'delete_device': False,

        'read_log': False,
        'add_log': True,
        'delete_log': False,
    }
