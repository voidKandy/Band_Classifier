from fastai.vision.all import *
import gradio as gr

learn_inf = load_learner('export.pkl')
categories = ('radiohead', 'voidkandy', 'king_gizzard')
def classify_specs(img):
    img = img.reshape((-1, 256, 256, 3))
    pred, idx, probs = learn_inf.predict(img)
    return dict(zip(categories, map(float,probs)))

image = gr.inputs.Image(shape=(192,192))
label = gr.outputs.Label()

intf = gr.Interface(fn=classify_specs, inputs=image, outputs=label)
intf.launch(inline=False)