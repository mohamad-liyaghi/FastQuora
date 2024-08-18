from faker import Faker


fake = Faker()


def generate_fake_user_data() -> dict:
    """
    Generate a dictionary with fake data for the User model.
    """
    return {
        "email": fake.email(),
        "nickname": fake.user_name(),
        "biography": fake.text(max_nb_chars=255),
        "password": fake.password(),
    }
