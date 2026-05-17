from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class PanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'panel'

    def ready(self):
        from django.contrib.auth.models import User
        
        @receiver(post_migrate)
        def create_default_user(sender, **kwargs):
            if sender.name == 'django.contrib.auth':
                if not User.objects.exists():
                    User.objects.create_superuser(
                        username='admin',
                        email='admin@secondchance.com',
                        password='admin123'
                    )
                    print('✓ Usuario inicial creado: admin / admin123')
        
        post_migrate.connect(create_default_user)
