from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <title>Startseite</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
                background: linear-gradient(to right, grey 50%, blue 50%);
            }

            .container {
                text-align: center;
                color: white;
                z-index: 10;
            }

            h1 {
                font-size: 4em;
                margin-bottom: 0.5em;
                color: transparent;
                -webkit-text-stroke: 2px white;
                background: linear-gradient(to right, grey 50%, blue 50%);
                -webkit-background-clip: text;
                background-clip: text;
                animation: slideInRight 2s ease-in-out forwards, scaleUp 2s ease-in-out forwards;
            }

            p {
                font-size: 1.5em;
                margin-bottom: 1em;
                color: white;
                animation: slideInBack 3s ease-in-out forwards;
            }

            .hidden {
                opacity: 0;
                visibility: hidden;
            }

            .new-content {
                display: none;
            }

            .new-content h2 {
                font-size: 3em;
                margin-bottom: 0.5em;
                color: transparent;
                -webkit-text-stroke: 2px white;
                background: linear-gradient(to right, grey 50%, blue 50%);
                -webkit-background-clip: text;
                background-clip: text;
                animation: slideInLeft 2s ease-in-out forwards;
            }

            .new-content p {
                font-size: 1.5em;
                margin-bottom: 1em;
                color: white;
                padding: 10px;
                border: 2px solid white;
                animation: scaleUp 2s ease-in-out forwards;
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            @keyframes slideInRight {
                from { transform: translateX(100%); }
                to { transform: translateX(0); }
            }

            @keyframes slideInLeft {
                from { transform: translateX(-100%); }
                to { transform: translateX(0); }
            }

            @keyframes slideInBack {
                from { transform: translateZ(-500px); opacity: 0; }
                to { transform: translateZ(0); opacity: 1; }
            }

            @keyframes scaleUp {
                from { transform: scale(0.5); }
                to { transform: scale(1); }
            }
        </style>
    </head>
    <body onclick="toggleContent()">
        <div class="container">
            <div class="content">
                <h1>Willkommen</h1>
                <p>Dies ist eine animierte Startseite mit einem umgebenden, zweigeteilten Hintergrund.</p>
            </div>
            <div class="new-content">
                <h2>Neuer Inhalt</h2>
                <p>Dieser Inhalt erscheint nach einem Klick und ist ebenfalls animiert.</p>
            </div>
        </div>
        <script>
            function toggleContent() {
                const currentContent = document.querySelector('.content');
                const newContent = document.querySelector('.new-content');
                currentContent.classList.add('hidden');
                setTimeout(() => {
                    currentContent.style.display = 'none';  
                    newContent.style.display = 'block';
                    newContent.classList.remove('hidden');
                }, 1000);
            }
        </script>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
