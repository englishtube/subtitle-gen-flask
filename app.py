from flask import Flask, request, render_template, flash, send_from_directory, url_for
import os
import whisper
import shutil
import subtitle
import pysrt
import warnings

location = os.getcwd()
video_dir = "video"
video_folder_path = os.path.join(location, video_dir)

srt_file_dir = "srt_files"
srt_folder_path = os.path.join(location, srt_file_dir)

extracted_audio_dir = "extracted_audio"
extracted_folder_path = os.path.join(location, extracted_audio_dir)

VIDEO_UPLOAD_FOLDER = video_folder_path
ALLOWED_EXTENSIONS = {'mp4'}

app = Flask(__name__)
app.config['VIDEO_UPLOAD_FOLDER'] = VIDEO_UPLOAD_FOLDER
app.secret_key = "super secret key"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home
@app.route("/")
def home():
  return render_template('index.html')

# Subtitle Generator
@app.route("/subtitle_gen",methods=['POST','GET'])
def subtitle_gen():
  filename = ""
  data = ""
  json_data = ""
  if(request.method == 'POST'):
    try: 
      isExistinput = os.path.exists(video_folder_path)
      if(isExistinput == True):
        shutil.rmtree(video_folder_path)
        os.mkdir(video_folder_path)
      elif(isExistinput == False):
        os.mkdir(video_folder_path)

      isExistinput = os.path.exists(extracted_folder_path)
      if(isExistinput == True):
          shutil.rmtree(extracted_folder_path)
          os.mkdir(extracted_folder_path)
      elif(isExistinput == False):
        os.mkdir(extracted_folder_path)

      isExistinput = os.path.exists(srt_folder_path)
      if(isExistinput == True):
          shutil.rmtree(srt_folder_path)
          os.mkdir(srt_folder_path)
      elif(isExistinput == False):
          os.mkdir(srt_folder_path)

      video = request.files['upload_video']
      video_url = request.form['video_url']

      if video:
        if video and allowed_file(video.filename):
          filename = os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], "uploaded_video.mp4")
          video.save(filename)

        model_name = "small"
        output_dir = srt_folder_path
        srt_only = True

        if model_name.endswith(".en"):
          warnings.warn(
              f"{model_name} is an English-only model, forcing English detection.")
          args["language"] = "en"

        model = whisper.load_model(model_name)
        audios = subtitle.get_audio(filename)
        english_srt_file = subtitle.get_subtitles(
          audios, srt_only, output_dir, lambda audio_path: model.transcribe(audio_path, fp16=False)
        )
          
        data = {"status":"success", "video" : filename, "english_srt_file" : english_srt_file}
        print("Data : ",data)
        flash("english: English Subtitle is generated successfully !!", "success")
        return render_template('index.html') 

      if video_url:
        downloaded_filename = app.config['VIDEO_UPLOAD_FOLDER']
        download_videos = subtitle.download_video(video_url, downloaded_filename)

        model_name = "small"
        output_dir = srt_folder_path
        srt_only = True

        if model_name.endswith(".en"):
          warnings.warn(
              f"{model_name} is an English-only model, forcing English detection.")
          args["language"] = "en"

        model = whisper.load_model(model_name)

        audios = subtitle.get_audio(download_videos)
        english_srt_file = subtitle.get_subtitles(
          audios, srt_only, output_dir, lambda audio_path: model.transcribe(audio_path, fp16=False)
        )

        json_d = {"status":"success", "video" : filename, "english_srt_file" : english_srt_file}
        print("Data : ",data)
        flash("english: English Subtitle is generated successfully !!", "success")
        return render_template('index.html') 
    except Exception as e:
      data = {"status":"failed","error":str(e)}
      print("Data : ",data)
      flash("englisherror: English Subtitle is not generated!!", "error")
      return render_template('index.html') 

@app.route("/chainesesrt_gen",methods=['POST','GET'])
def chainese():
  try:
    english_srt_file = '/home/testenglishtube/Desktop/subtitle-gen/srt_files/English.srt'
    
    subs = pysrt.open(english_srt_file)

    # Initialize the translator
    translator_object = subtitle.translator()
    dest_language_code = 'zh-CN'

    # Translate each subtitle and replace the text
    for sub in subs:
        sub.text = translator_object.Translate(sub.text,dest_language_code)

    # Save the translated SRT file
    chainese_srt_file = os.path.join(srt_folder_path + "/" + "Chainese.srt")
    subs.save(chainese_srt_file, encoding='utf-8')

    data = {"status":"success", "chainese_srt_file" : chainese_srt_file}
    print("Data : ", data)
    flash("chinese: Chinese Subtitle is generated successfully !!", "success")
    return render_template('index.html', chinese_file=chainese_srt_file) 
  except Exception as e:
    data = {"status":"failed","error":str(e)}
    print("Data : ", data)
    flash("chineseerror: Chinese Subtitle is not generated !!", "error")
    return render_template('index.html') 

@app.route("/japanesesrt_gen",methods=['POST','GET'])
def japanese():
  try:
    english_srt_file = '/home/testenglishtube/Desktop/subtitle-gen/srt_files/English.srt'
    
    subs = pysrt.open(english_srt_file)

    # Initialize the translator
    translator_object = subtitle.translator()
    dest_language_code = 'ja'

    # Translate each subtitle and replace the text
    for sub in subs:
      sub.text = translator_object.Translate(sub.text,dest_language_code)

    # Save the translated SRT file
    japanese_srt_file = os.path.join(srt_folder_path + "/" + "Japanese.srt")
    subs.save(japanese_srt_file, encoding='utf-8')

    data = {"status":"success", "japanese_srt_file" : japanese_srt_file}
    print("Data : ", data)
    flash("japanese: Japanese Subtitle is generated successfully !!", "success")
    return render_template('index.html') 
  except Exception as e:
    data = {"status":"failed","error":str(e)}
    print("Data : ", data)
    flash("japaneseerror: Japanese Subtitle is not generated !!", "error")
    return render_template('index.html') 

@app.route("/koreansrt_gen",methods=['POST','GET'])
def korean():
  try:
    english_srt_file = '/home/testenglishtube/Desktop/subtitle-gen/srt_files/English.srt'
    
    subs = pysrt.open(english_srt_file)

    # Initialize the translator
    translator_object = subtitle.translator()
    dest_language_code = 'ko'

    # Translate each subtitle and replace the text
    for sub in subs:
        sub.text = translator_object.Translate(sub.text,dest_language_code)

    # Save the translated SRT file
    korean_srt_file = os.path.join(srt_folder_path + "/" + "Korean.srt")
    subs.save(korean_srt_file, encoding='utf-8')

    data = {"status":"success", "korean_srt_file" : korean_srt_file}
    print("Data : ", data)
    flash("korean: Korean Subtitle is generated successfully !!", "success")
    return render_template('index.html') 
  except Exception as e:
    data = {"status":"failed","error":str(e)}
    print("Data : ", data)
    flash("koreanerror: Korean Subtitle is not generated !!", "error")
    return render_template('index.html') 

@app.route('/download/english/srt')
def downloadenglishsrt():
  filename = "English.srt"
  path = os.path.join(srt_folder_path, filename)
  if os.path.isfile(path):
    return send_from_directory(srt_folder_path, filename)
  else:
    flash("englishfile: English Subtitle File is not found !!", "error")
  return render_template('index.html') 

@app.route('/download/chainese/srt')
def downloadchainesesrt():
  filename = "Chainese.srt"
  path = os.path.join(srt_folder_path, filename)
  if os.path.isfile(path):
    return send_from_directory(srt_folder_path, filename)
  else:
    flash("chinesefile: Chinese Subtitle File is not found !!", "error")
  return render_template('index.html') 

@app.route('/download/japanese/srt')
def downloadjapanesesrt():
  filename = "Japanese.srt"
  path = os.path.join(srt_folder_path, filename)
  if os.path.isfile(path):
    return send_from_directory(srt_folder_path, filename)
  else:
    flash("japanesefile: Japanese Subtitle File is not found !!", "error")
  return render_template('index.html') 

@app.route('/download/korean/srt')
def downloadkoreansrt():
  filename = "Korean.srt"
  path = os.path.join(srt_folder_path, filename)
  if os.path.isfile(path):
    return send_from_directory(srt_folder_path, filename)
  else:
    flash("koreanfile: Korean Subtitle File is not found !!", "error")
  return render_template('index.html') 

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
