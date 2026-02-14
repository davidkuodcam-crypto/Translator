from flask import Flask, request, send_file
from gtts import gTTS
import io

app = Flask(__name__)

# Vercel 需要這個來處理 CORS (如果前後端不同源)，
# 但因為我們都在同一個 Vercel 專案下，通常不需要額外設定 CORS。

@app.route('/api/speak', methods=['GET'])
def speak():
    text = request.args.get('text', '')
    lang = request.args.get('lang', 'zh-TW')
    
    # 簡單的錯誤處理
    if not text:
        return "Missing text", 400

    try:
        # --- gTTS 邏輯 ---
        # lang 參數對應: zh-TW, en, ja, vi (gTTS 都支援)
        tts = gTTS(text=text, lang=lang)
        
        # 使用 BytesIO 在記憶體中處理檔案，不要寫入硬碟
        # 因為 Vercel Serverless 環境是唯讀的 (除了 /tmp)
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
        return str(e), 500

# 為了讓 Vercel 能夠正確識別
if __name__ == '__main__':
    app.run(debug=True)
