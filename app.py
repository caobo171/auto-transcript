from flask import Flask, request
from tool import googleAutoTranscript

app = Flask(__name__)

@app.route('/api/file' , methods=["POST"])
def test():
    file = request.files['file']
 
    script = request.form['transcript']
    result  = googleAutoTranscript(file , script)
    print(result)
    return result


if __name__ == '__main__':
    app.run(debug=True)