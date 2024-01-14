import cgi
import cgitb

cgitb.enable()  # Увімкнення виведення трейсів для CGI-скриптів

# Встановлюємо заголовок HTML-сторінки
print("Content-type: text/html\n")

# Отримуємо дані з форми
form = cgi.FieldStorage()

# Функція для виведення результатів
def print_results(vehicle, color):
    print("<html>")
    print("<head>")
    print("<title>Результати вибору</title>")
    print("</head>")
    print("<body>")
    print("<h2>Ваш вибір:</h2>")
    print("<p>Техніка: {}</p>".format(vehicle))
    print("<p>Колір: {}</p>".format(color))
    print("<p>Дякуємо за вибір!</p>")
    print("</body>")
    print("</html>")

# Перевіряємо, чи були відправлені дані форми
if "vehicle" in form and "color" in form:
    # Отримуємо значення з форми
    selected_vehicle = form.getvalue("vehicle")
    selected_color = form.getvalue("color")

    # Виводимо результати
    print_results(selected_vehicle, selected_color)
else:
    # Виводимо форму для вибору техніки та кольору
    print("<html>")
    print("<head>")
    print("<title>Вибір техніки</title>")
    print("</head>")
    print("<body>")
    print("<h2>Виберіть улюблену техніку та колір:</h2>")
    print('<form method="post" action="form.py">')
    print('  <label for="vehicle">Техніка:</label><br>')
    print('  <input type="radio" name="vehicle" value="car"> Автомобіль<br>')
    print('  <input type="radio" name="vehicle" value="motorcycle"> Мотоцикл<br>')
    print('  <input type="radio" name="vehicle" value="bike"> Велосипед<br><br>')
    print('  <label for="color">Колір:</label><br>')
    print('  <select name="color">')
    print('    <option value="red">Червоний</option>')
    print('    <option value="blue">Синій</option>')
    print('    <option value="green">Зелений</option>')
    print('  </select><br><br>')
    print('  <input type="submit" value="Відправити">')
    print('</form>')
    print("</body>")
    print("</html>")
