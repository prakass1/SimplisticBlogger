from blog_admin import create_admin_app

admin_app = create_admin_app()

if __name__ == '__main__':
    admin_app.run(host="0.0.0.0", port=9001)
