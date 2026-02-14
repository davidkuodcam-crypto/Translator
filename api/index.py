from flask import Flask, request, send_file
from gtts import gTTS
import io

app = Flask(__name__)

# 增加一個根目錄路由，用來測試 Python 是否活著
@app.route('/', methods=['GET'])
def home():
    return "Python API is running!", 200

# 您的主功能
@app.route('/api/speak', methods=['GET'])
def speak():
    text = request.args.get('text', '')
    lang = request.args.get('lang', 'zh-TW')
    
    if not text:
        return "錯誤: 請輸入文字", 400

    try:
        # --- gTTS 邏輯 ---
        tts = gTTS(text=text, lang=lang)
        
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        return send_file(
            fp, 
            mimetype="audio/mpeg", 
            as_attachment=False, 
            download_name="speech.mp3"
        )
    except Exception as e:
        # ⚠️ 關鍵：把錯誤訊息回傳給前端，而不是只傳 500
        return f"Server Error details: {str(e)}", 500

# 讓 Vercel 識別 application
application = app

if __name__ == '__main__':
    app.run(debug=True)
