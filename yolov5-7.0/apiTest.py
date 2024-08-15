from flask import Flask, request, jsonify
from dashscope import Generation
import dashscope
from http import HTTPStatus

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS(app, origins="http://localhost:5055") # 修改为新的前端端口
CORS(app)
# 设置你的API密钥
dashscope.api_key = "sk-8e3f56d9445a44b8825f24576f5488c0"

def call_with_stream(messages):
    responses = Generation.call(
        model="qwen-turbo",
        messages=messages,
        result_format='message',
        stream=True,
        incremental_output=True
    )
    full_content = ""
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            full_content += response.output.choices[0].message.content
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
    return full_content

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    messages = [
        {'role': 'system', 'content': 'you are a helpful assistant'}
    ]
    messages.append({'role': 'user', 'content': user_input})
    assistant_response = call_with_stream(messages)
    messages.append({'role': 'assistant', 'content': assistant_response})

    return jsonify({'reply': assistant_response})

if __name__ == '__main__':
    app.run(port=5050)

