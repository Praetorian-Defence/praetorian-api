from object_checker.base_object_checker import AbacChecker

from apps.core.models import User, UserProjectDevice


class ProjectObjectChecker(AbacChecker):
    @staticmethod
    def check_project(user: User, obj):
        has_object = False

        if UserProjectDevice.objects.filter(user=user, project=obj).exists():
            has_object = True

        return has_object
