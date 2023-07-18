import gradio as gr
import openai

openai.api_key = "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"

message_history = []

def predict(input):
    global message_history
    message_history.append({"role":"user", "content":input})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = message_history
    )
    reply_content = completion.choices[0].message.content
    message_history.append({"role":"assistant", "content":reply_content})
    response = [(message_history[i]["content"], message_history[i + 1]["content"]) for i in range(0, len(message_history) - 1, 2)]
    return response

def modify():
    global message_history
    if len(message_history) == 0:
        return
    message_history.append({"role":"system", "content":"User is not pleased with your answer, please modify it."})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = message_history
    )
    reply_content = completion.choices[0].message.content
    message_history.append({"role":"assistant", "content":reply_content})
    response = [(message_history[i]["content"], message_history[i + 1]["content"]) for i in range(0, len(message_history) - 1, 2)]
    return response

def clear():
    global message_history
    message_history = []
    return

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Type your message here")
        txt.submit(predict, txt, chatbot)
        # txt.submit(lambda: "", None, txt)
        txt.submit(None, None, txt, _js="() => {''}")

    button = gr.Button(value="Modify")
    button.click(fn=modify, inputs=None, outputs=chatbot)

    button = gr.Button(value="Reset")
    button.click(fn=clear, inputs=None, outputs=chatbot)

demo.launch()