from fastai.vision.all import *
import gradio as gr

learn_inf = load_learner('export.pkl')
categories = ('radiohead', 'voidkandy', 'king_gizzard')
def classify_specs(img):
    pred, idx, probs = learn_inf.predict(img)
    return dict(zip(categories, map(float,probs)))
image = gr.inputs.Image(shape=(192,192))
label = gr.outputs.Label()

intf = gr.Interface(fn=classify_specs, inputs=image, outputs=label)
intf.launch(inline=False, share=True)