from internal.auth.recipe import RecipeAuthorize
from internal.objects.recipe import Recipe
from internal.objects.user import User


class RBACRecipeAuthorize(RecipeAuthorize):

    ROLE_ACTION_MAPPING = {
        Recipe.Role.UNDEFINED: {},
        Recipe.Role.VIEWER: {
            Recipe.Action.GET
        },
        Recipe.Role.EDITOR: {
            Recipe.Action.GET,
            Recipe.Action.GET_METADATA,
            Recipe.Action.GET_MESSAGES,
            Recipe.Action.UPDATE,
            Recipe.Action.MESSAGE
        },
        Recipe.Role.OWNER: {
            Recipe.Action.GET,
            Recipe.Action.GET_METADATA,
            Recipe.Action.GET_MESSAGES,
            Recipe.Action.CREATE,
            Recipe.Action.UPDATE,
            Recipe.Action.DELETE,
            Recipe.Action.MESSAGE
        }
    }

    @classmethod
    def authorize(cls, recipe: Recipe, action: Recipe.Action, action_user: User) -> bool:
        """Authorize a User to perform an action on a Recipe resource.

        Args:
            recipe: The Recipe resource
            action: The action to perform on the User resource
            action_user: The user performing the action

        Returns:
            bool: Whether the user is authorized to perform the action
        """
        role = recipe.user_role_mapping.get(action_user.id, Recipe.Role.UNDEFINED)

        if recipe.private and role is Recipe.Role.UNDEFINED:
            return False

        if role is Recipe.Role.UNDEFINED:
            role = Recipe.Role.VIEWER

        if action in Recipe.generative_ai_actions and not action_user.can_call_generative_ai:
            return False

        return action in cls.ROLE_ACTION_MAPPING[role]
