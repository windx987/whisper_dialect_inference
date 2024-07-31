import gradio as gr
import requests

import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def get_completion(chat_logs):

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(chat_logs)
    return response.text

url = 'http://localhost:8000/transcribe/'

def transcribe(audio, speaker):
    
    files = {'file': open(audio, 'rb')}
    response = requests.post(url, files=files)
    transcription = response.json()
    # print(transcription)

    if speaker == "Doctor":
        return f"Doctor: {transcription}"
    elif speaker == "Patient":
        return f"Patient: {transcription}"

chat_logs = []

def update_chat_logs(audio, speaker):
    global chat_logs
    new_entry = transcribe(audio, speaker)
    chat_logs.append(new_entry)
    return "\n".join(chat_logs), None  # Reset the audio  input

def generate_chat_summary(chat_logs):
    
    # chat_logs = """   
    # Doctor: สวัสดีครับ คุณมีอาการอะไรบ้าง
    # Patient: สวัสดีครับ ผมมีอาการปวดหัวและคลื่นไส้มา 3 วันแล้วครับ
    # Doctor: มีไข้ไหมครับ
    # Patient: ใช่ครับ มีไข้สูงประมาณ 38.5 องศาเซลเซียส
    # Doctor: เข้าใจแล้วครับ เดี๋ยวจะตรวจร่างกายเพิ่มเติมนะครับ
    # """
    
    prompt = f"""
    Your task is to generate a short summary of a conversation \
    between a doctor and a patient in Thai language. \

    Summarize the conversation below, delimited by triple \
    backticks, in at most 30 words, focusing on what the patient is sick with. \

    chat_logs: ```{chat_logs}```
    """
    response = get_completion(prompt)
    return response

def summarize_chat_logs():
    global chat_logs
    chat_summary = generate_chat_summary("\n".join(chat_logs))
    return chat_summary

def clear_chat_logs():
    global chat_logs
    chat_logs = []
    return "", ""

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Doctor-Patient Dialogue Transcription")
    
    with gr.Row():
        with gr.Column():
            doctor_audio = gr.Audio(type="filepath", label="Record Doctor")
            doctor_button = gr.Button("Transcribe Doctor")
        
        with gr.Column():
            patient_audio = gr.Audio(type="filepath", label="Record Patient")
            patient_button = gr.Button("Transcribe Patient")
    
    chat_output = gr.Textbox(label="Chat Logs", lines=20, interactive=False)
    
    doctor_button.click(fn=update_chat_logs, inputs=[doctor_audio, gr.State("Doctor")], outputs=[chat_output, doctor_audio])
    patient_button.click(fn=update_chat_logs, inputs=[patient_audio, gr.State("Patient")], outputs=[chat_output, patient_audio])

    summary_button = gr.Button("Generate Chat Summary")
    chat_summary_output = gr.Textbox(label="Chat Summary", lines=5, interactive=False)
    
    summary_button.click(fn=summarize_chat_logs, inputs=[], outputs=chat_summary_output)

    clear_button = gr.Button("Clear Chat Logs")
    clear_button.click(fn=clear_chat_logs, inputs=[], outputs=[chat_output, chat_summary_output])

demo.launch(share=True)