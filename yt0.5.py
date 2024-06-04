from flask import Flask, request, render_template_string
import yt_dlp

app = Flask(__name__)

# Default options for yt-dlp
default_ydl_opts = {
    'format': 'best',
    'outtmpl': '%(title)s.%(ext)s',
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        format = request.form.get('format')
        quality = request.form.get('quality', 'best')
        filename = request.form.get('filename')
        use_tor = 'use_tor' in request.form
        include_channel_name = 'include_channel_name' in request.form

        # Customize options based on form input
        ydl_opts = default_ydl_opts.copy()
        ydl_opts['format'] = f'{quality}/best'
        if filename:
            ydl_opts['outtmpl'] = f'{filename}.%(ext)s'
        elif include_channel_name:
            ydl_opts['outtmpl'] = '%(uploader)s - %(title)s.%(ext)s'
    
        if format == 'mp3':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        
        if "shorts" in url:
            ydl_opts['format'] = 'bestvideo+bestaudio/best'

        if "instagram.com/reel" in url:
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
                    
        if "tiktok.com" in url:
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
            
        if use_tor:
            ydl_opts['proxy'] = 'socks5://127.0.0.1:9050'
            
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            message = "Video Downloaded! Check the folder."
            alert_class = "alert-success"
        except Exception as e:
            message = f"An error occurred: {str(e)}"
            alert_class = "alert-danger"
        
        return render_template_string(f'''
        <div class="container mt-5">
            <div class="alert {alert_class}" role="alert">
                <b>{message}</b>
            </div>
            <br>
            <a class="btn btn-primary" href="/">Back</a>
        </div>
        ''')
    
    return render_template_string('''
    <form method="post" class="form-group">
        <div class="mb-3">
            <label for="url" class="form-label">URL del Video:</label>
            <input type="text" name="url" class="form-control" id="url" required>
        </div>
        <div class="mb-3">
            <label for="format" class="form-label">Format:</label>
            <select name="format" class="form-select" id="format">
                <option value="mp4">MP4</option>
                <option value="mp3">MP3</option>
            </select>
        </div>
        <div class="mb-3">
            <label for="filename" class="form-label">File Name (optional):</label>
            <input type="text" name="filename" class="form-control" id="filename">
        </div>
        <div class="mb-3 form-check">
            <input type="checkbox" name="include_channel_name" class="form-check-input" id="include_channel_name" checked>
            <label for="include_channel_name" class="form-check-label">YT Channel Name</label>
        </div>
        <button type="submit" class="btn btn-primary">Download</button>
    </form>
    ''')
    
if __name__ == '__main__':
    app.run(debug=True)
#        <div class="mb-3 form-check">
            #<input type="checkbox" name="use_tor" class="form-check-input" id="use_tor">
          #<label for="use_tor" class="form-check-label">Use Tor (work in progress)</label>
        #</div>