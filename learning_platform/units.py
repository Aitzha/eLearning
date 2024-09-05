import secrets
import string

from learning_platform.models import UserProfile


def user_has_permission(user, perm_codename):
    """
    Check if a user has a specific permission based on their role.

    Args:
        user (User): The user object for whom the permission check is being made.
        perm_codename (str): The codename of the permission to check (e.g., 'add_course').

    Returns:
        bool: True if the user has the permission, False otherwise or if the user profile does not exist.
    """
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.role.permissions.filter(codename=perm_codename).exists()
    except UserProfile.DoesNotExist:
        return False


def generate_random_password(length=12):
    """
    Generate a secure random password.

    Args:
        length (int): The length of the password to be generated

    Returns:
        str: The password of given length
    """

    # Add possible character for password in 'alphabet' variable (ASCII letters and digits)
    alphabet = string.ascii_letters + string.digits

    # Randomly choose characters from 'alphabet' using secrets module
    return ''.join(secrets.choice(alphabet) for _ in range(length))

