import customtkinter as ctk
from gui.ventana_principal import VentanaPrincipal
from tkinter import messagebox

class AppLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ingreso - GestionFacil PRO")
        self.geometry("400x450")
        self.eval('tk::PlaceWindow . center')
        
        ctk.CTkLabel(self, text="Bienvenido a", font=("Roboto", 16)).pack(pady=(40, 5))
        ctk.CTkLabel(self, text="GestionFacil", font=("Roboto", 28, "bold"), text_color="#3498db").pack(pady=(0, 30))

        self.opt_rol = ctk.CTkOptionMenu(self, values=["Admin", "Cajero"], width=250)
        self.opt_rol.pack(pady=10)

        self.ent_pass = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=250)
        self.ent_pass.pack(pady=15)

        ctk.CTkButton(self, text="INICIAR SESIÓN", command=self.verificar_login, height=40, font=("Roboto", 14, "bold")).pack(pady=30)
        ctk.CTkLabel(self, text="Claves por defecto:\nAdmin: admin | Cajero: cajero", font=("Roboto", 12), text_color="gray").pack(side="bottom", pady=20)

    def verificar_login(self):
        rol = self.opt_rol.get()
        password = self.ent_pass.get()
        
        # Validaciones de seguridad
        if (rol == "Admin" and password == "admin") or (rol == "Cajero" and password == "cajero"):
            self.destroy() # Cerramos el login
            self.iniciar_sistema(rol)
        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")

    def iniciar_sistema(self, rol):
        ventana_raiz = ctk.CTk()
        app = VentanaPrincipal(ventana_raiz, rol)
        ventana_raiz.mainloop()

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    app = AppLogin()
    app.mainloop()