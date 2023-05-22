import gradio as gr
import modules.extras
import modules.generation_parameters_copypaste as parameters_copypaste

from modules.shared import opts
from modules.ui_components import ToolButton
from modules.call_queue import wrap_gradio_call
from modules import scripts, script_callbacks, shared

class QuickPNGInfo(scripts.Script):
    def title(self):
        return 'Quick PNG Info'

    def describe(self):
        return "Embed PNG Info into the txt2imga and img2img tabs, you can use it without leaving the tab."

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def before_component(self, component, **kwargs):
        if kwargs.get("elem_id") == f"txt2img_gallery":
            tab = "txt2img"
            with gr.Row(variant='compact').style(equal_height=True):
                with gr.Column(min_width=100):
                    image = gr.Image(elem_id=f"{tab}_pnginfo_image", show_label=False, label="PNG Info Source", source="upload", interactive=True, type="pil").style(height=42,width=100)
                with gr.Column(scale=10):
                    with gr.Row(variant='compact'):
                        show_info_text = ToolButton(value='\u2139\uFE0F',visible=not opts.data.get("qpi_always_show_text", False))
                        hide_info_text = ToolButton(value='\u2139\uFE0F',visible=opts.data.get("qpi_always_show_text", False))
                        buttons = parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
            with gr.Row(variant='compact'):       
                with gr.Row(elem_id=f"{tab}_parameters_viewer",visible=opts.data.get("qpi_always_show_text", False)) as parameters_viewer:
                    html = gr.HTML(visible=False)
                    generation_info = gr.Textbox(visible=False, elem_id=f"{tab}_pnginfo_generation_info")
                    html2 = gr.HTML()
                    for tabname, button in buttons.items():
                            parameters_copypaste.register_paste_params_button(parameters_copypaste.ParamBinding(
                            paste_button=button, tabname=tabname, source_text_component=generation_info, source_image_component=image,
                        ))
            with gr.Row():
                htmlt = gr.HTML(value="<span style='display: block; height: 8px;'></span>")     
            image.change(
                fn=wrap_gradio_call(modules.extras.run_pnginfo),
                inputs=[image],
                outputs=[html, generation_info, html2],
            )
            
            show_info_text.click(
                fn=lambda: ({"visible": True, "__type__": "update"}, {"visible": False, "__type__": "update"}, {"visible": True, "__type__": "update"}),
                inputs=[],
                outputs=[parameters_viewer, show_info_text, hide_info_text],
                show_progress = False,
            )
            
            hide_info_text.click(
                fn=lambda: ({"visible": False, "__type__": "update"}, {"visible": False, "__type__": "update"}, {"visible": True, "__type__": "update"}),
                inputs=[],
                outputs=[parameters_viewer, hide_info_text, show_info_text],
                show_progress = False,
            )

        if kwargs.get("elem_id") == f"img2img_gallery":
            tab = "img2img"
            with gr.Row(variant='compact').style(equal_height=True):
                with gr.Column(min_width=100):
                    image = gr.Image(elem_id=f"{tab}_pnginfo_image", show_label=False, label="PNG Info Source", source="upload", interactive=True, type="pil").style(height=42,width=100)
                with gr.Column(scale=10):
                    with gr.Row(variant='compact'):
                        show_info_text = ToolButton(value='\u2139\uFE0F',visible=not opts.data.get("qpi_always_show_text", False))
                        hide_info_text = ToolButton(value='\u2139\uFE0F',visible=opts.data.get("qpi_always_show_text", False))
                        buttons = parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
            with gr.Row(variant='compact'):       
                with gr.Row(elem_id=f"{tab}_parameters_viewer",visible=opts.data.get("qpi_always_show_text", False)) as parameters_viewer:
                    html = gr.HTML(visible=False)
                    generation_info = gr.Textbox(visible=False, elem_id=f"{tab}_pnginfo_generation_info")
                    html2 = gr.HTML()
                    for tabname, button in buttons.items():
                            parameters_copypaste.register_paste_params_button(parameters_copypaste.ParamBinding(
                            paste_button=button, tabname=tabname, source_text_component=generation_info, source_image_component=image,
                        ))
            with gr.Row():
                htmlt = gr.HTML(value="<span style='display: block; height: 8px;'></span>")     
            image.change(
                fn=wrap_gradio_call(modules.extras.run_pnginfo),
                inputs=[image],
                outputs=[html, generation_info, html2],
            )
            
            show_info_text.click(
                fn=lambda: ({"visible": True, "__type__": "update"}, {"visible": False, "__type__": "update"}, {"visible": True, "__type__": "update"}),
                inputs=[],
                outputs=[parameters_viewer, show_info_text, hide_info_text],
                show_progress = False,
            )
            
            hide_info_text.click(
                fn=lambda: ({"visible": False, "__type__": "update"}, {"visible": False, "__type__": "update"}, {"visible": True, "__type__": "update"}),
                inputs=[],
                outputs=[parameters_viewer, hide_info_text, show_info_text],
                show_progress = False,
            )

def create_settings_items():
    section = ('quick_png_info', 'Quick PNG Info')
    opts.add_option("qpi_always_show_text", shared.OptionInfo(
        False, "Display generation info text by default. (Requires restart)", section=section
    ))

scripts.script_callbacks.on_ui_settings(create_settings_items)