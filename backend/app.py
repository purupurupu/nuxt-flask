from flask import Flask, jsonify

app = Flask(__name__)

# health check
@app.route('/')
def hello():
    return jsonify({"message": "Welcome to the API"})

# ChatGPT API
@app.route('/chat', methods=['POST'])
def chat():
    #TODO: ChatGPT APIを呼び出す
    return True

if __name__ == '__main__':
    app.run(debug=True)