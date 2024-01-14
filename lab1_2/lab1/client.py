import socket

# Встановлюємо адресу сервера і порт для підключення
server_address = ('localhost', 12346)

# Створюємо сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Підключаємось до сервера
client_socket.connect(server_address)

try:
    while True:
        # Введення тексту користувачем
        message = input("Введіть текст для сервера (або 'закрити' для завершення): ")

        # Відправляємо дані на сервер
        client_socket.send(message.encode('utf-8'))

        if message.lower() == 'закрити':
            break  # Виходимо з циклу при команді "закрити"

        # Очікуємо підтвердження від сервера
        confirmation = client_socket.recv(1024).decode('utf-8')
        print(f"Сервер відповів: {confirmation}")

except KeyboardInterrupt:
    print("Закриваємо з'єднання з сервером.")
except ConnectionRefusedError:
    print("Не вдалося підключитися до сервера.")
finally:
    # Закриваємо з'єднання з сервером
    client_socket.close()
