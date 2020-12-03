from blog import create_app
from blog_admin import create_admin_app

app = create_app()

if __name__ == '__main__':
    app.run(port=9000, host="0.0.0.0")