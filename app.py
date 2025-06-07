from livereload import Server

from app import create_app

app = create_app()


server = Server(app.wsgi_app)
server.watch("app/templates")
server.watch("app/static")

if __name__ == "__main__":
    server.serve(port=5000)
