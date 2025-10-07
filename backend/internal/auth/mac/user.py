from internal.auth.user import UserAuthorize
from internal.objects.user import User


class MACUserAuthorize(UserAuthorize):
    """The MACUserAuthorize authorizes Users using mandatory access control."""

    @classmethod
    def authorize(self, user: User, _: User.Action, action_user: User) -> bool:
        """Authorize a User to perform an action on a User resource.

        Args:
            user: The User resource
            action: The action to perform on the User resource
            action_user: The user performing the action

        Returns:
            bool: Whether the user is authorized to perform the action
        """
        return user.id == action_user.id
