"""
Create permission groups
Create permissions to models for a set of groups
python manage.py create_groups 로 실행
"""
import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

MODELS = ['Product', 'ProductImage']  # 모델 이름 리스트
PERMISSIONS = ['add', 'delete', 'change', 'view']

class Command(BaseCommand):
    help = 'Creates permission groups for users'

    def handle(self, *args, **options):
        new_group, created = Group.objects.get_or_create(name='Sellers')
        for model_name in MODELS:
            # 모델 클래스를 동적으로 불러옵니다.
            model = ContentType.objects.get(model=model_name.lower()).model_class()
            if model is None:
                logging.warning(f"Model not found for {model_name}.")
                continue

            for permission_codename in PERMISSIONS:
                # ContentType과 함께 권한 코드명을 사용하여 Permission 객체를 가져옵니다.
                try:
                    permission = Permission.objects.get(content_type=ContentType.objects.get_for_model(model), codename=f"{permission_codename}_{model_name.lower()}")
                except Permission.DoesNotExist:
                    logging.warning(f"Permission not found for {permission_codename} {model_name}.")
                    continue

                new_group.permissions.add(permission)
                print(f"Adding permission: {permission_codename} {model_name}")

        print("Created default group and permissions.")
