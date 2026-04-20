from canvas_converter import convert_canvas_to_png, convert_png_to_canvas
from ugctex_converter import convert_png_to_ugctex, convert_ugctex_to_png
import dearpygui.dearpygui as dpg
from pathlib import Path
import time

def defaultPromptCB(s, ad, userdata):
    dpg.delete_item(userdata[0])

#fixed version of https://github.com/hoffstadt/DearPyGui/discussions/1002
def show_info(title, message, selection_callback):
    with dpg.mutex():
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        with dpg.window(label=title, modal=True, no_close=True) as modal_id:
            dpg.add_text(message)
            with dpg.group(horizontal=True) as group:
                dpg.add_button(label="Ok", width=75, user_data=(modal_id, True), callback=selection_callback, parent=group)
                dpg.add_button(label="Cancel", width=75, user_data=(modal_id, False), callback=selection_callback, parent=group)

    time.sleep(0.04) #fucked way to wait one frame but whatever
    width = dpg.get_item_width(modal_id)
    height = dpg.get_item_height(modal_id)
    dpg.set_item_pos(modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])

def filePathCallback(sender, appdata: str):
    daaPath: str = appdata.replace("\"", "")
    global paths
    if not "," in daaPath:
        paths = [daaPath]
    else:
        paths = daaPath.split(",")
    if len(paths) <= 1:
        if daaPath.lower().endswith(".png"):
            dpg.set_item_label("isugctex", "Convert to ugctex")
        else:
            dpg.set_item_label("isugctex", "Is ugctex")
    else:
        dpg.set_item_label("isugctex", "Convert to/Is ugctex")

def browseFiles(sender, appdata):
    filePath: str = appdata['file_path_name'].replace("\\", "/")
    if len(appdata['selections']) > 1:
        sel: dict = appdata['selections']
        stuffs:str = ""
        for thing in sel.values():
            stuffs += "\"" + thing.replace("\\", "/").strip() + "\","
        stuffs = stuffs.strip()
        filePath = stuffs[0:len(stuffs)-1]
        
    dpg.set_value("filepath", filePath)
    filePathCallback(sender, filePath)

def convertFile():
    daaPath: str = dpg.get_value("filepath").replace("\"", "")
    successfuls = 0
    global paths
    if not "," in daaPath:
        paths = [daaPath]
    else:
        paths = daaPath.split(",")
    for daPath in paths:
        cwdPath = Path.cwd() / daPath
        ugctex: bool = dpg.get_value("isugctex")
        if daPath.lower().endswith(".png"):
            if ugctex:
                convert_png_to_ugctex(cwdPath)
            else:
                convert_png_to_canvas(cwdPath)
            successfuls += 1
        elif daPath.lower().endswith(("canvas.zs", ".canvas")):
            convert_canvas_to_png(cwdPath)
            successfuls += 1
        elif daPath.lower().endswith(("ugctex.zs", ".ugctex")):
            convert_ugctex_to_png(cwdPath)
            successfuls += 1
        elif daPath.lower().endswith(".zs"):
            if ugctex:
                convert_ugctex_to_png(cwdPath)
            else:
                convert_canvas_to_png(cwdPath)
        else:
            show_info("Error", "Error: File type unreconized. Please put a valid file type.", defaultPromptCB)
            continue
    if successfuls > 0:
        show_info("Success!", "This operation has completed successfully.", defaultPromptCB)
    
    

def main():
    dpg.create_context()
    dpg.create_viewport(title="Tomodachi Life Converter", width=1080, height=720)
    with dpg.file_dialog(tag="filedialog", directory_selector=False, show=False, callback=browseFiles, cancel_callback=lambda: dpg.hide_item("filedialog"), width=700, height=400):
        dpg.add_file_extension(".png")
        dpg.add_file_extension(".zs")
        dpg.add_file_extension(".canvas")
        dpg.add_file_extension(".ugctex")

    with dpg.window(tag="woahh"):
        dpg.add_text("Tomodachi Life Converter")
        dpg.add_group(label="group", tag="hor", horizontal=True)
        dpg.add_text("Path:", parent="hor")
        dpg.add_input_text(default_value="", tag="filepath", callback=filePathCallback, parent="hor")
        dpg.add_button(label="Browse Files", tag="browse", callback=lambda: dpg.show_item("filedialog"), parent="hor")
        dpg.add_checkbox(label="Is ugctex", tag="isugctex")
        dpg.add_button(label="Convert", tag="convert", callback=convertFile)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("woahh", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()