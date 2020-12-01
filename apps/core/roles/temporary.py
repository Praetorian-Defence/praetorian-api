from rolepermissions.roles import AbstractUserRole


class Temporary(AbstractUserRole):
    available_permissions = {
        'read_project': True,
        'read_remote': True
    }
