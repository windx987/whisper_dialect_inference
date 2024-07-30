import gradio as gr
import requests

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
    return "\n".join(chat_logs), None  # Reset the audio input

def generate_chat_summary(chat_logs):
    # Access Gemini API for prompt engineering (replace with actual API call)
    summary_prompt = f"Provide a concise summary of the doctor-patient conversation based on the following dialogue:\n{chat_logs}"
    # summary = Gemini.generate_text(summary_prompt, max_length=150)
    summary = f'this is mock up summary from following logs.\n{summary_prompt}'
    return summary

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