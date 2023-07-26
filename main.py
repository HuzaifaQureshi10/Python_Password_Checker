import requests
import hashlib


# Function to get a response from the API
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + str(query_char)
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Undesirable Status Code {res.status_code}")
    return res


# Function to get the number of times our password has been found in the leaked database
def num_of_occurrences(response, tail):
    tuple_of_lists = (line.split(':') for line in response.text.splitlines())
    for hash_tail, count in tuple_of_lists:
        if hash_tail == tail:
            return int(count)
    return 0


# The function that does everything in an order
def pwned_api_check(password):
    # convert password to hash and get the first 5 chars and tail
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_5, tail = sha1password[:5], sha1password[5:]

    # invoke request function to get api response
    response = request_api_data(first_5)

    # invoke function that processes the response and compares with tail to find out occurrences
    occurrences = num_of_occurrences(response, tail)

    # Self-explanatory
    if occurrences > 0:
        print(f"Password is insecure. It has been found {occurrences} times ")
    else:
        print("Password is secure. No occurrences found.")


if __name__ == '__main__':
    while True:
        passwrd = input("Please enter the password to be checked: ")
        pwned_api_check(passwrd)











