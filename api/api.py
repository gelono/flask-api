from flask import Flask, request, jsonify
from OpenSSL import SSL

context = SSL.Context(SSL.TLSv1_2_METHOD)
context.use_privatekey_file(r'C:\wacs\crt\vm5043127.43ssd.had.wf-key.pem')
context.use_certificate_file(r'C:\wacs\crt\vm5043127.43ssd.had.wf-crt.pem')

app = Flask(__name__)


def check_token(token):
    with open('../storage/tokens.txt', 'r') as file:
        tokens = file.read().splitlines()
        return token in tokens


@app.route('/hello', methods=['POST'])
def hello_world():
    if request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            if check_token(token):
                return jsonify({"message": "Hello world"}), 200
            else:
                return jsonify({"error": "Invalid token"}), 401
        else:
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
    else:
        return jsonify({"error": "Method not allowed"}), 405


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='vm5043127.43ssd.had.wf', port=5000, ssl_context=context)
