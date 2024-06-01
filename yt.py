from flask import Flask, request, render_template_string
import yt_dlp

app = Flask(__name__)

# Opzioni di configurazione predefinite per yt-dlp
default_ydl_opts = {
    'format': 'best',
    'outtmpl': '%(title)s.%(ext)s',
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        format = request.form['format']

        # Imposta le opzioni di yt-dlp in base al formato selezionato dall'utente
        ydl_opts = default_ydl_opts.copy()  # Crea una copia delle opzioni predefinite
        if format == 'mp3':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return render_template_string('''
        <div class="container mt-5">
            <div class="alert alert-success" role="alert">
                <b>Video Downloaded! check the folder</b>
            </div>
            <br>
            <a class="btn btn-primary" font-size: 35px; href="/">Back</a>
        </div>
    ''')

    return render_template_string('''
        <form method="post">
            URL del Video: <input type="text" name="url"><br>
            Format:
            <select name="format">
                <option value="mp4">MP4</option>
                <option value="mp3">MP3</option>
            </select><br>
            <input type="submit" value="Download">
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
