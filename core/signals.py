from django.db.models.signals import post_migrate, pre_migrate
from django.dispatch import receiver
from .funcs import func3, func2, func1
import asyncio

@receiver(post_migrate)
async def after_migrate_hooks(sender, **kwargs):
    print("Executing after_migrate hooks...")
    await func1()
    await func2()
    await func3()
    post_migrate.disconnect(after_migrate_hooks)


@receiver(pre_migrate)
async def before_migrate_hooks(sender, **kwargs):
    print("Executing before_migrate hooks...")
    await func1()
    await func2()
    await func3()
    pre_migrate.disconnect(before_migrate_hooks)


async def after_start():
    print("Executing setup hooks...")
    await func1()
    await func2()
    await func3()

asyncio.run(after_start())

