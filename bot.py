import gradio as gr
import openai

openai.api_key = "YOUR_API_KEY"

message_history = []

def predict():
    global message_history
    message_history.append({"role":"User", "content":input})
    completion = openai.Completion.create(
        model = "text_davinci_003",
        messages = message_history
    )
    reply_content = completion.choices[0].message.content
    message_history.append({"role":"assistant", "content":reply_content})
    response = [(message_history[i]["content"], message_history[i + 1]["content"]) for i in range(len(message_history) - 1, 2)]
    return response
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Type your message here").style(container=False)
        txt.submit(predict, txt, chatbot)
        # txt.submit(lambda: "", None, txt)
        txt.submit(None, None, txt, _js="() => ('')")

    demo.launch()