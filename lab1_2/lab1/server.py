import socket
import datetime
import logging

# Налаштування логування для сервера
logging.basicConfig(filename='server.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('server')

# Встановлюємо адресу сервера і порт для слухання
server_address = ('localhost', 12346)

# Створюємо сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Прив'язуємо сокет до адреси сервера і порту
server_socket.bind(server_address)

# Починаємо слухати підключення
server_socket.listen(1)
print("Сервер готовий приймати підключення...")

while True:
    # Очікуємо підключення клієнта
    client_socket, client_address = server_socket.accept()
    print(f"Підключився клієнт з адреси {client_address}")

    try:
        # Обробка повідомлень в циклі
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break  # Виходити з циклу при завершенні з'єднання

            # Виводимо отримані дані та час отримання
            print(f"Отримано від клієнта: {data}")
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Час отримання: {current_time}")

            # Перевірка на команду закриття
            if data == "закрити":
                break  # Виходити з циклу при команді "закрити"

            # Відправка відповіді клієнту
            response = "Ваше повідомлення отримано та оброблено."
            client_socket.send(response.encode('utf-8'))

        print("З'єднання з клієнтом було закрито.")
    except ConnectionResetError:
        print("З'єднання з клієнтом було припинено.")
    finally:
        # Закриваємо з'єднання з клієнтом
        client_socket.close()
