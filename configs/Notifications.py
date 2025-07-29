import time
from plyer import notification
import configs.InfraConfigs as config


def spawnNotification(title, message):
    if config.isNOtificationEnabled():
        notification.notify(title=title, message=message, timeout=10)
