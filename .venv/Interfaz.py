from flet import *
import flet
from PyPDF2 import *

# Definición de colores 
dark_color = "#222831"
red_color = "#E23E57"
purple_color = "#9153F4"
blue_color = "#387ADF"
text_color = "#ffffff"

def go_to_route(page, route): # Función para redireccionar las rutas de la app
        page.go(route)

# Definición de componente reutilizables
# Para crear componentes reutilizables siempre se deben usar clases
class Cards(UserControl):
    def __init__(self, title, content, bgcolor, icon): # Inicializador de la clase
        super().__init__()
        self.title = title
        self.content = content
        self.bgcolor = bgcolor
        self.icon = icon
        self.card = Card()
    
    def handle_on_hover(self, e): # Efecto hover de las cartas
        if e.data == 'true':
            self.card.content.scale = Scale(1.04)
        else:
            self.card.content.scale = Scale(1)
        self.update()
        
    def build(self): # Constructor de las cartas
        self.card.content = Container(
            content=Column(
                [
                    Image(src=self.icon, width=50, height=50, fit=ImageFit.CONTAIN),
                    Text(self.title, theme_style=TextThemeStyle.TITLE_MEDIUM, color=text_color),
                    Text(self.content, color=text_color, text_align=TextAlign.JUSTIFY),
                ],
            ),
            width=300,
            height=200,
            padding=15,
            bgcolor=self.bgcolor,
            border_radius=10,
            on_hover=self.handle_on_hover
        )
        return self.card

class Windows(UserControl):
    def __init__(self, wcolor, title, subtitle, nroute1, nroute2, icon1, icon2, route1, route2, page, action_button_title):
        super().__init__()
        self.wcolor = wcolor # Color de botones y sidebar
        self.title = title # Título de las páginas
        self.subtitle = subtitle # Subtítulo de las páginas
        self.nroute1 = nroute1 # Nombre de las rutas de la sidear
        self.nroute2 = nroute2
        self.icon1 = icon1 # Íconos de las rutas
        self.icon2 = icon2
        self.route1 = route1 # Rutas del path de la sidebar
        self.route2 = route2
        self.action_button_title = action_button_title
        self.archivos = [] # Lista donde se guardarán todos los archivos
        self.page = page # Pasamos el parametro de página para hacer referenciaa la página actual donde estamos
        self.progress_bar = ProgressBar(width= 300, color= self.wcolor, visible= False)
        #Inicalización del filepicker 
        self.list_files = ListView(spacing= 10, padding= 20)
        self.file_picker = FilePicker(on_result= self.file_picker_result) # File picker para controlar los eventos de archivos
        self.save_file_picker = FilePicker(on_result= self.upload_progress) # File picker para controlar los eventos de archivos
        self.page.overlay.append(self.file_picker) # Muestra el explorador para poder seleccionar archivos
        self.page.overlay.append(self.save_file_picker) # Muestra el explorador para poder seleccionar archivos
        self.container_files = Container(
            content= self.list_files, # Este container es usado para contener el List View
            bgcolor= self.wcolor,
            height= 250,
            width= 400,
            border= border.all(1, colors.WHITE),
            visible= False
        )
        self.cancel_button = ElevatedButton(
            "Cancelar",
            style= ButtonStyle(
                shape= RoundedRectangleBorder(radius= 10),
                bgcolor= self.wcolor,
                color= text_color,
            ),
            width= 120, 
            height= 40,
            on_click= lambda _: self.cancelFun(), # Manda a llamar a la función cancelar
            visible= False
        )
        self.action_button = ElevatedButton( # El boton nos ayuda a manejar el evento de la acción que queremos hacer 
            self.action_button_title,
            style= ButtonStyle(
                shape= RoundedRectangleBorder(radius= 10),
                bgcolor= self.wcolor,
                color= text_color,
            ),
            width= 120,
            height= 40,
            # El save_file_picker es diferente al file_picker anterior y solo se utliza para sacar el explorador de archivos y obtener el path
            on_click= lambda _: self.save_file_picker.save_file(dialog_title="Guardar como", allowed_extensions= ["pdf"]),
            visible= False
        )
    
    def cancelFun(self): # La función es utilzada para ocultar y limpiar todos los elementos del contenedor de los archivos
        self.container_files.visible = False
        self.container_files.clean()
        self.action_button.visible = False
        self.cancel_button.visible = False
        self.container_files.update()
        self.action_button.update()
        self.cancel_button.update()
        
    def file_picker_result(self, e: FilePickerResultEvent):
        if e.files:
            self.container_files.content.clean() # Limpia los controles para que no haya nada agregado
            self.list_files.controls.clear()
            for file in e.files:
                self.list_files.controls.append(Text(file.name)) # Muestra en la propiedad Text cada nombre del archivo
                self.archivos.append(file.path) # Guarda en una lista del path de todos los archivos que se le adjuntan 
            self.container_files.visible = True
            self.action_button.visible = True
            self.cancel_button.visible = True
            self.list_files.update() # Actualiza para que se visulice en la interfaz 
            self.container_files.update()
            self.action_button.update()
            self.cancel_button.update()
        else:
            self.container_files.visible = False
            self.container_files.update()
        
    def upload_progress(self, e: FilePickerResultEvent): 
        if self.action_button_title == "Unir":
            merger = PdfMerger() # Crear un merger 
            for pdf in self.archivos:
                self.progress_bar.visible = True
                merger.append(pdf)
                self.progress_bar.update()
            self.progress_bar.visible = False
            self.container_files.visible = False
            self.cancel_button.visible = False
            self.action_button.visible = False
            self.list_files.clean()
            self.container_files.clean()
            self.progress_bar.update()
            self.container_files.update()
            self.action_button.update()
            self.cancel_button.update()
            merger.write(e.path + ".pdf")
            merger.close()
            
        elif self.action_button_title == "Dividir":
            writer = PdfWriter()
            print(self.archivos)
            for pdf in self.archivos:
                self.progress_bar.visible = True
                reader = PdfReader(pdf)
                for page_num, page in enumerate(reader.pages, 1):
                    writer.add_page(page)
                    path = f"{e.path}{page_num}.pdf"
                    with open(path, "wb") as output:
                        writer.write(output)
            self.progress_bar.visible = False
            self.container_files.visible = False
            self.cancel_button.visible = False
            self.action_button.visible = False
            self.list_files.clean()
            self.container_files.clean()
            self.progress_bar.update()
            self.container_files.update()
            self.action_button.update()
            self.cancel_button.update() 
            print(self.archivos)       
        else:
            writer = PdfWriter()
            for pdf in self.archivos:
                self.progress_bar.visible = True
                reader = PdfReader(pdf)
                for page in reader.pages:
                    page.compress_content_streams()
                    writer.add_page(page)
                writer.write(e.path + ".pdf")
                writer.close()
                self.progress_bar.update()
            self.progress_bar.visible = False
            self.container_files.visible = False
            self.cancel_button.visible = False
            self.action_button.visible = False
            self.list_files.clean()
            self.container_files.clean()
            self.progress_bar.update()
            self.container_files.update()
            self.action_button.update()
            self.cancel_button.update()
            
    def build(self):
        return Container(
            content= Row(
                [
                    # Side bar
                    Container(
                        content= Column(
                            [
                                Container(
                                    Row(controls=[Text("Más opciones", theme_style= TextThemeStyle.HEADLINE_LARGE, color= text_color)]),
                                    margin= margin.only(25, 10, 0, 20),
                                ),
                                Container(
                                    Row(
                                        controls=[
                                            Icon(icons.ARROW_BACK, color=text_color),
                                            Text("Volver al inicio", color=text_color, size=17, weight=FontWeight.BOLD)
                                        ]
                                    ),
                                    margin=margin.only(0, 10, 0, 10),
                                    on_click=lambda _: go_to_route(self.page, "/") 
                                ),
                                Container(
                                    Row(
                                        controls=[
                                            Image(src= self.icon1, width=25, height=25, fit=ImageFit.CONTAIN),
                                            Text(self.nroute1, color=text_color, size=17, weight=FontWeight.BOLD)
                                        ],
                                    ),
                                    margin=margin.only(0, 10, 0, 10),
                                    on_click=lambda _: go_to_route(self.page, self.route1)
                                ),
                                Container(
                                    Row(
                                        controls=[
                                            Image(src=self.icon2, width=25, height=25, fit=ImageFit.CONTAIN),
                                            Text(self.nroute2, color=text_color, size=17, weight=FontWeight.BOLD)
                                        ]
                                    ),
                                    margin=margin.only(0, 10, 0, 10),
                                    on_click=lambda _: go_to_route(self.page, self.route2),
                                ),
                            ],
                            alignment= MainAxisAlignment.START,
                            expand= True
                        ),
                        width= 300,
                        padding=20,
                        bgcolor= self.wcolor,
                    ),
                    
                    # Contenido Principal de la página 
                    Container(
                        content= Column(
                            [
                                Text(self.title, theme_style= TextThemeStyle.DISPLAY_LARGE, color= text_color, weight= FontWeight.BOLD),
                                Text(self.subtitle, theme_style= TextThemeStyle.HEADLINE_SMALL, color= text_color),
                                ElevatedButton(
                                    "Seleccionar Archivos",
                                    icon= icons.FOLDER_OPEN,
                                    style= ButtonStyle(
                                        shape= RoundedRectangleBorder(radius= 10),
                                        bgcolor= self.wcolor,
                                        color= text_color,
                                    ),
                                    width= 300,
                                    height= 50,
                                    on_click= lambda _: self.file_picker.pick_files(allow_multiple= True, allowed_extensions= ["pdf"])
                                ),
                                self.progress_bar,
                                Column(
                                    [
                                        self.container_files,
                                        Row([
                                            self.action_button,
                                            self.cancel_button
                                        ], alignment= "center")
                                    ],
                                    alignment= "center",
                                    horizontal_alignment= "center"
                                ),
                            ],
                            expand= True,
                            alignment= "center",
                            horizontal_alignment= "center"
                        ),
                        expand= True
                    ),
                ],
                expand= True,
            ), 
            expand= True,
            height= 650
        )

def main(page: Page):
    page.window.maximized = True # La app se abrirá maximizada
    page.title = "PDF Tools" # Título de la ventana
    page.bgcolor = dark_color # Fondo de la ventana
    page.padding = 0 # Quita el relleno de la ventana 

    # Ventana de inicio de la app
    body = Container(
        Column([
            Container(
                Row(
                    controls=[
                        Text(
                            "Bienvenido a PDF Tools, elije lo que desees realizar:",  # Título de la página de inicio
                            theme_style=TextThemeStyle.HEADLINE_LARGE, 
                            color=text_color,
                            weight=FontWeight.BOLD
                        ),
                    ],
                    alignment="center",
                ),
                margin=margin.only(0, 150, 0, 5)
            ),
            Container(
                ResponsiveRow(
                    controls=[
                        Container( # Contenedor de las cartas
                            Cards(
                                title="Unir PDF",
                                content="Une PDFs y ponlos en el orden que prefieras. Rápido y fácil. 😉",
                                bgcolor=red_color,
                                icon="icons/unir2.png",
                            ),
                            col={"sm": 6, "md": 4, "xl": 3},
                            on_click=lambda _: go_to_route(page, "/unir")
                        ),
                        Container(
                            Cards(
                                title="Dividir PDF",
                                content="Extrae una o varias páginas de tu PDF o convierte cada página del PDF en un archivo independiente. 😃",
                                bgcolor=blue_color,
                                icon="icons/dividido2.png",
                            ),
                            col={"sm": 6, "md": 4, "xl": 3},
                            on_click=lambda _: go_to_route(page, "/dividir")
                        ),
                        Container(
                            Cards(
                                title="Comprimir PDF",
                                content="Consigue que tu documento PDF pese menos y al mismo tiempo manten la máxima calidad posible. 👌",
                                bgcolor=purple_color,
                                icon="icons/comprimir2.png",
                            ),
                            col={"sm": 6, "md": 4, "xl": 3},
                            on_click=lambda _: go_to_route(page, "/comprimir")
                        )
                    ],
                    alignment="center",
                    expand=True, # Para que ocupe el espacio disponible de la ventana
                ),
                margin=margin.only(0, 20, 0, 15)
            )
        ]),
        expand=True
    )
    
    #Ventana donde se unen PDFs
    unir = Windows(
        wcolor= red_color,
        title= "Unir archivos PDF",
        subtitle= "Une PDFs y ponlos en el orden que prefieras.",
        nroute1= "Dividir",
        nroute2= "Comprimir",
        icon1= "icons/dividido2.png",
        icon2= "icons/comprimir2.png",
        route1= "/dividir",
        route2= "/comprimir",
        page= page,
        action_button_title= "Unir",
    )
    
    #Ventana donde se dividen PDFs
    dividir = Windows(
        wcolor= blue_color,
        title= "Divide archivos PDF",
        subtitle= "Extrae una o varias páginas de tu PDF.",
        nroute1= "Unir",
        nroute2= "Comprimir",
        icon1= "icons/unir2.png",
        icon2= "icons/comprimir2.png",
        route1= "/unir",
        route2= "/comprimir",
        page= page,
        action_button_title= "Dividir"
    )
    
    #Ventana donde se comprimen PDFs
    comprimir = Windows(
        wcolor= purple_color,
        title= "Comprimir archivos PDF",
        subtitle= "Consigue que tu documento PDF pese menos.",
        nroute1= "Dividir",
        nroute2= "Unir",
        icon1= "icons/dividido2.png",
        icon2= "icons/unir2.png",
        route1= "/dividir",
        route2= "/unir",
        page= page,
        action_button_title= "Comprimir"
    )
    
    # Función que nos indica en que ruta estamos y que se utiliza para cambiarlas
    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                "/", 
                [body]
            )
        )
        if page.route == "/unir":
            page.views.append(
                View(
                    "/unir",
                    [unir]
                )
            )
        elif page.route == "/dividir":
            page.views.append(
                View(
                    "/dividir",
                    [dividir]
                )
            )
        elif page.route == "/comprimir":
            page.views.append(
                View(
                    "/comprimir",
                    [comprimir]
                )
            )
        page.update()

    # Función que ayuda a regresar a la ruta anterior 
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        
    page.on_route_change = route_change # Se inicializa la ruta en la página de inicio
    page.on_view_pop = view_pop
    page.go(page.route)
    
app(target=main)