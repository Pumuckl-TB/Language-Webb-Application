from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_sum', methods=['GET']) 
def get_sum():
    x = request.args.get('x')
    y = request.args.get('y')
    result = int(x) + int(y)
                     
    return '{}'.format(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug = True)
