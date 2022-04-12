import logging as logger
import random
from random import randint
import string
import datetime

class GenericUtilities():
    """Class for generating random values"""


    def generate_random_name_and_surname(self):
        """Return name and surname at random from 2 tuples."""
        logger.debug("Generating random name and surname.")

        first = ('Crapps', 'Dark Skies', 'Dennis Clawhammer',
                'Dicman', 'Elphonso', 'Fancypants', 'Figgs', 'Foncy', 'Gootsy',
                'Greasy Jim', 'Huckleberry', 'Huggy', 'Ignatious', 'Jimbo')

        last = ('Guster', 'Henderson', 'Hooperbag',
                'Hoosenater', 'Hootkins', 'Jefferson', 'Jenkins')

        first_name = random.choice(first)
        surname = random.choice(last)
        info = {"name":first_name, "surname":surname, "full_name": first_name + ' ' + surname}

        return info

    def random_id_with_N_digits(self,n=5):
        """Return random id."""
        logger.debug("Generating random name and surname.")
        range_start = 10**(n-1)
        range_end = (10**n)-1
        id = randint(range_start, range_end)
        return id


    def generate_random_email_and_password(self, domain=None, email_prefix=None):
        logger.debug("Generating random email login and password.")

        if not domain:
            domain = 'app.com'
        if not email_prefix:
            email_prefix = 'testuser'

        random_email_string_length = 5
        random_string = ''.join(random.choices(string.ascii_lowercase, k=random_email_string_length))

        email = email_prefix + '_' + random_string + '@' + domain

        password_string_length = 6
        password_string = ''.join(random.choices(string.ascii_letters, k=password_string_length))

        password = password_string.title() + str(self.random_id_with_N_digits(n=2)) + '$'

        random_info = {'email': email, 'password': password}

        return random_info

    def generate_random_name(self):

        """Return random name."""
        logger.debug("Generating random name for new  ounit.")

        name = ('Treasury', 'Defense', 'Justice',
                 'Interior', 'Agriculture', 'Fancypants', 'Commerce', 'Veterans Affairs', 'Gootsy',
                 'Homeland Security')

        ou_name = random.choice(name)

        info = {"name": ou_name}

        return info

    def generate_radom_string(self, n=2, capital=True):

        """
        Return random string.
        n - number of charcters
        if capital True - all letters are capital
        """

        logger.debug("Generating random string with n-characters.")
        capital = True
        ran = ''.join(random.choices(string.ascii_letters, k=n))

        if capital == True:
            ran = ran.upper()
        else:
            ran = ran.lower()

        info = {"random_string":ran}

        return info


    def generate_random_bank_account(self):

        """
        Return random string and currency code

        """
        logger.debug("Generating random account number.")

        account = ''.join(random.choices(string.digits, k=26))

        currency_code = ('PLN', 'USD', 'EUR', 'DKK', 'NOK', 'GBP')

        currency = random.choice(currency_code)

        info = {"account": account, "currency":currency}

        return info

    def generate_random_date(self):
        """
        Return random date

        """
        start_date = datetime.datetime(2022, 2, 1, 23, 59, 59)
        end_date = datetime.datetime(2023, 2, 1, 23, 59, 59)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        hours = random.randrange(24)

        random_date = start_date + datetime.timedelta(days=random_number_of_days, hours=random.randrange(23), minutes=random.randrange(59), seconds=random.randrange(59))
        formated_date = random_date.strftime("%Y-%m-%d %H:%M:%S")

        info = {"date":formated_date}

        return info


