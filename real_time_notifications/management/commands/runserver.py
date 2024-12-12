from daphne.server import Server
from django.core.management.commands.runserver import Command as RunserverCommand

class Command(RunserverCommand):
    def handle(self, *args, **options):
        if options.get("use_threading", True):
            self.stdout.write("Threading is not supported with Daphne.")
        Server(self.addr, self.port, application="real_time_notifications.asgi:application").run()
