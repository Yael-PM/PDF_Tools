from flet import *
import flet

def main(page: Page):
    page.window_width= 300
    
    txt_me = Text("Hello this file will write")
    
    def mysavefile(e: FilePickerResultEvent):
        save_location = e.path
        if save_location:
            try:
                with open(save_location, "r", encoding="utf-8") as file:
                    print("Save succsess")
                    file.write()
            except Exception as e:
                print("error saved", e)
        page.update()
    
    saveme = FilePicker(on_result= mysavefile)
    page.overlay.append(saveme)
    page.add(
        Column(
            [
                ElevatedButton("Save file",
                               on_click=lambda _: saveme.save_file())
            ]
        )
    )
    
flet.app(target= main)