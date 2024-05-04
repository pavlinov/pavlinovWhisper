import os
import torch
import whisper
from quart import Quart, request, jsonify

PORT=5002

# Check if NVIDIA GPU is available
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Whisper model:
model = whisper.load_model("medium", device=DEVICE)


app = Quart(__name__)
upload_folder = 'public/upload'
os.makedirs(upload_folder, exist_ok=True)  # Ensure the upload directory exists

@app.route('/')
async def heartbeat():
    return jsonify({"status": "alive", "message": f"Server is running on {PORT}"}), 200

@app.route('/upload', methods=['POST'])
async def upload_files():
    files = await request.files
    file_details = []

    # Loop over every file that the user submitted.
    for file_key in files:
        file = files[file_key]
        if file and allowed_file(file.filename):
            filepath = os.path.join(upload_folder, file.filename)
            await file.save(filepath)

            result = model.transcribe(filepath)

            file_details.append({
                "filename": file.filename,
                'transcript': result['text'],
                "status": "uploaded"
                })

    if not file_details:
        return jsonify({"message": "No valid files provided"}), 400
    return jsonify({"message": "Files uploaded successfully", "files": file_details}), 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3', 'wav', 'ogg'}


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=PORT)
