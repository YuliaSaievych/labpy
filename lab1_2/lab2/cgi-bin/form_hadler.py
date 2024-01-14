#!/usr/bin/env python3

import cgi
import http.cookies

# Отримання даних з форми
form = cgi.FieldStorage()

# Отримання значень полів форми
name = form.getvalue("name", "Невідомо")
email = form.getvalue("email", "Невідомо")
gender = form.getvalue("gender", "Невідомо")
interests = form.getlist("interests")

# Встановлення cookies
cookies = http.cookies.SimpleCookie()
cookies["name"] = name
cookies["email"] = email
cookies["gender"] = gender

# Виведення HTML-сторінки
print("Content-type: text/html")
print(cookies.output())
print("\n")

print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CGI Form Processing with Cookies</title>
</head>
<body>
    <h1>Результати введення:</h1>
    <p>Ім'я: {}</p>
    <p>Email: {}</p>
    <p>Стать: {}</p>
    <p>Інтереси: {}</p>
    <p>Значення cookies:</p>
    <ul>
        <li>Ім'я: {}</li>
        <li>Email: {}</li>
        <li>Стать: {}</li>
    </ul>
</body>
</html>
""".format(name, email, gender, ', '.join(interests), cookies["name"].value, cookies["email"].value, cookies["gender"].value))
