from http.server import CGIHTTPRequestHandler, HTTPServer

# Вказати каталог, де розташовані CGI-скрипти
cgi_directory = "/cgi-bin"

# Створити об'єкт CGIHTTPRequestHandler
handler = CGIHTTPRequestHandler
handler.cgi_directories = [cgi_directory]

# Запустити веб-сервер на порту 8000
port = 8000
httpd = HTTPServer(('localhost', port), handler)
print(f"Serving on port {port}")
httpd.serve_forever()
