from django.contrib.auth.hashers import make_password, check_password
from App_SGC.models import CustomUser  # Use your custom user model

# Find all users with MD5 hashed passwords (assuming MD5 is always 32 characters)
users_with_md5 = CustomUser.objects.filter(password__regex=r'^[a-f0-9]{32}$')

for user in users_with_md5:
    # Replace '123' with the actual plain password (if known), or handle it differently
    if check_password('123', user.password):  # MD5 password check
        # Rehash the password with a secure hasher
        user.password = make_password('123')  # Replace '123' with the actual plain password (if known)
        user.save()

print(f"Migrated {users_with_md5.count()} users to a secure password hasher.")
