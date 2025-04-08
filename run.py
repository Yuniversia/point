from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host=app.config['IP'],  port=app.config['PORT'])