import smtplib
from email.message import EmailMessage
import mimetypes
import logging
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog, messagebox

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_sender.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enviador de E-mails Profissional")
        self.root.geometry("500x400")
        
        load_dotenv()
        
        # Variáveis de controle
        self.sender_email = tk.StringVar(value=os.getenv('SENDER_EMAIL', ''))
        self.sender_password = tk.StringVar()
        self.recipient_email = tk.StringVar()
        self.subject = tk.StringVar(value="Seu currículo!")
        self.body = tk.StringVar(value="Olá,\n\nAqui está o documento solicitado.\n\nAtenciosamente,\n")
        self.attachment_path = tk.StringVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Campos do formulário
        tk.Label(main_frame, text="De:").grid(row=0, column=0, sticky=tk.W, pady=2)
        tk.Entry(main_frame, textvariable=self.sender_email, width=40).grid(row=0, column=1, pady=2)
        
        tk.Label(main_frame, text="Senha:").grid(row=1, column=0, sticky=tk.W, pady=2)
        tk.Entry(main_frame, textvariable=self.sender_password, show="*", width=40).grid(row=1, column=1, pady=2)
        
        tk.Label(main_frame, text="Para:").grid(row=2, column=0, sticky=tk.W, pady=2)
        tk.Entry(main_frame, textvariable=self.recipient_email, width=40).grid(row=2, column=1, pady=2)
        
        tk.Label(main_frame, text="Assunto:").grid(row=3, column=0, sticky=tk.W, pady=2)
        tk.Entry(main_frame, textvariable=self.subject, width=40).grid(row=3, column=1, pady=2)
        
        tk.Label(main_frame, text="Mensagem:").grid(row=4, column=0, sticky=tk.NW, pady=2)
        tk.Text(main_frame, width=40, height=5).grid(row=4, column=1, pady=2)
        text_widget = tk.Text(main_frame, width=40, height=5)
        text_widget.grid(row=4, column=1, pady=2)
        text_widget.insert(tk.END, self.body.get())
        self.body_widget = text_widget
        
        tk.Label(main_frame, text="Anexo:").grid(row=5, column=0, sticky=tk.W, pady=2)
        tk.Entry(main_frame, textvariable=self.attachment_path, width=32, state='readonly').grid(row=5, column=1, pady=2, sticky=tk.W)
        tk.Button(main_frame, text="Procurar", command=self.browse_file).grid(row=5, column=1, sticky=tk.E)
        
        # Botão de envio
        tk.Button(main_frame, text="Enviar E-mail", command=self.send_email, bg="green", fg="white").grid(row=6, column=1, pady=10, sticky=tk.E)
    
    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.attachment_path.set(filename)
    
    def send_email(self):
        sender = self.sender_email.get()
        password = self.sender_password.get()
        recipient = self.recipient_email.get()
        subject = self.subject.get()
        body = self.body_widget.get("1.0", tk.END)
        attachment = self.attachment_path.get() if self.attachment_path.get() else None
        
        if not all([sender, password, recipient, subject, body]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return
        
        try:
            msg = EmailMessage()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.set_content(body.strip())
            
            if attachment:
                mime_type, _ = mimetypes.guess_type(attachment)
                if mime_type is None:
                    mime_type = 'application/octet-stream'
                
                maintype, subtype = mime_type.split('/', 1)
                
                with open(attachment, 'rb') as file:
                    msg.add_attachment(
                        file.read(),
                        maintype=maintype,
                        subtype=subtype,
                        filename=os.path.basename(attachment)
                    )
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)
            
            messagebox.showinfo("Sucesso", "E-mail enviado com sucesso!")
            logger.info(f"E-mail enviado para {recipient}")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao enviar e-mail:\n{str(e)}")
            logger.error(f"Erro ao enviar e-mail: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()