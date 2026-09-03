def is_palindrome(word):
    # Reverse the string
    rev = word[::-1]

    # Check if they match
    if word == rev:
        return True
    else:
        return False

print(is_palindrome("racecar"))
