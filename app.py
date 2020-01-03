from flask import Flask, request , jsonify
from tool import googleAutoTranscript

app = Flask(__name__)

@app.route('/api/file' , methods=["POST"])
def test():
    file = request.files['file']
    offset = int(request.form['offset'])
    chunk_duration = int( request.form['chunk_duration'] )
    chunks = max(int(request.form['chunks']) , 10)
    script = request.form['transcript']
    result , last = googleAutoTranscript(file , script , offset, chunks, chunk_duration)
    return jsonify({
        'result': result,
        'offset': offset,
        'chunks': chunks,
        'last': last
    })


@app.teardown_request
def show_teardown(exception):
    print('after with block' , exception)

if __name__ == '__main__':
    app.run(debug=True , threaded=True)