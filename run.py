from SecureWebApp import create_app
from waitress import serve

app = create_app()
# FOR DEVELOPMENT
app.run(debug=True)

# FOR PRODUCTION
# serve(app, host="0.0.0.0", port=80)
# serve(app, host="0.0.0.0", port=8080)
# serve(app, host="127.0.0.1", port=5000)
