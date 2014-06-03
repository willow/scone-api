import reversion

from src.aggregates.profile.models import Profile


reversion.register(Profile)
