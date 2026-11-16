from parkease import ParkEase


def before_scenario(context, scenario):
    """Technical set-up (a hook): every scenario starts with a fresh, empty ParkEase."""
    context.app = ParkEase()
    context.plate = None
    context.parked = None
    context.result = None
