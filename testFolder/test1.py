def is_palindrome(word):

    rev = word[::-1]

    if word == rev:
        return True
    else:
        return False


print(is_palindrome("racecar"))
