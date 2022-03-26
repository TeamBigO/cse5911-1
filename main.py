from webtool import create_app

app = create_app()

# only if we run main.py, will we execute app.run()
if __name__ == '__main__':
    # run flask app on webserver, automatically rerun when we make changes
    app.run(debug=True)