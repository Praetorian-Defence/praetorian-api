from object_checker.base_object_checker import AbacChecker

from apps.core.models import User, UserProjectDevice


class RemoteObjectChecker(AbacChecker):
    @staticmethod
    def check_remote(user: User, obj):
        has_object = False

        if UserProjectDevice.objects.filter(user=user, project__remotes=obj).exists():
            has_object = True

        return has_object
