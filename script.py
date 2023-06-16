import whisper

openai.api_key = 'YOUR_API_KEY'



youtubelink = ""


def download_video(url):
    try:
        youtube = pytube.YouTube(url)
        video = youtube.streams.get_audio_only()
        video.download()
        return True
    except Exception as e:
        print(f"Error downloading video: {e}")
        return False


download_video(youtubelink)

model = whisper.load_model("base")
result = model.transcribe("DOWNLOAD_FILE_NAME", "transcription.txt")



def generate_chapters(transcript_path):
    try:
        with open(transcript_path, 'r') as file:
            transcript = file.read()

        # Split transcript into sentences
        sentences = [s.strip() for s in transcript.split('.')]

        # Generate chapters using ChatGPT
        chapters = []
        current_chapter = ''
        for sentence in sentences:
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=f'Write a chapter about "{sentence}"\n\n---\n\n',
                max_tokens=100,
                n=1,
                temperature=0.7
            )

            chapter = response.choices[0].text.strip()
            current_chapter += sentence + '. '
            if len(current_chapter) + len(chapter) >= 5000:
                chapters.append(current_chapter.strip())
                current_chapter = chapter
            else:
                current_chapter += chapter

        chapters.append(current_chapter.strip())

        return chapters
    except Exception as e:
        print(f"Error generating chapters: {e}")
        return []


print(generate_chapters("transcription.txt"))