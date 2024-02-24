import gradio as gr

from modules import scripts, sd_samplers_common


store_latent = sd_samplers_common.store_latent
steps = []


class StepExplorerScript(scripts.Script):
    def title(self):
        return "Step Explorer"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def setup(self, p, *args):
        return super().setup(p, *args)

    def ui(self, is_img2img):
        with gr.Row():
            with gr.Column():
                is_enabled = gr.Checkbox(
                    label="Enable Step Exploration",
                    value=False,
                    elem_id=self.elem_id("is_enabled"),
                )
        gr.HTML("<br />")

        return [is_enabled]

    def process(self, p, is_enabled):
        global steps, store_latent
        if not is_enabled:
            return

        steps = []

        def capture_latent(decoded):
            steps.append(sd_samplers_common.sample_to_image(decoded))
            store_latent(decoded)

        setattr(sd_samplers_common, "store_latent", capture_latent)

    def postprocess(self, p, processed, is_enabled):
        global steps, store_latent
        if not is_enabled:
            return

        processed.images = steps
        processed.index_of_first_image = 0
        prompt, info = processed.infotexts[0].split("\n")
        processed.infotexts = [
            f"{prompt}\nStep: {i+1}, {info}" for i in range(len(steps))
        ]

        setattr(sd_samplers_common, "store_latent", store_latent)
