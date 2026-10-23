import os, tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import date
from pathlib import Path
from src.core import DocumentEngine, TYPES, read_rows, OUTPUT, ROOT

BG = "#F3F6F5"
GREEN = "#245A50"
DARK = "#20312F"

class AtelierApp:
    def __init__(self, root):
        self.root = root
        root.title("Atelier de documents")
        root.geometry("1020x700")
        root.minsize(850, 600)
        self.engine = DocumentEngine()
        self.page = tk.StringVar(value="Créer")
        self.kind = tk.StringVar(value="Attestation")
        self.civilite = tk.StringVar(value="M.")
        self.nom = tk.StringVar()
        self.prenom = tk.StringVar()
        self.date = tk.StringVar(value=date.today().strftime("%d/%m/%Y"))
        self.motif = tk.StringVar()
        self.montant = tk.StringVar(value="0")
        self.note = tk.StringVar(value="0")
        self.email = tk.StringVar()
        self.pdf = tk.BooleanVar(value=True)
        self.word = tk.BooleanVar(value=False)
        self.file = tk.StringVar()
        self.batch_kind = tk.StringVar(value="Attestation")
        self.status = tk.StringVar(value="Prêt")
        self._layout()
        self.show_page("Créer")

    def _layout(self):
        self.root.configure(bg=BG)
        shell = tk.Frame(self.root, bg=BG)
        shell.pack(fill="both", expand=True)
        side = tk.Frame(shell, bg=DARK, width=205)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        tk.Label(side, text="ATELIER\nDOCUMENTS", bg=DARK, fg="white",
                 font=("Segoe UI", 17, "bold"), justify="left").pack(anchor="w", padx=20, pady=(25,35))
        tk.Label(side, text="ESPACE DE TRAVAIL", bg=DARK, fg="#AFC7C1",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=20, pady=(0,10))
        for name, desc in [("Créer","Nouveau document"),("Importer","Liste Excel / CSV"),
                           ("Modèles","Textes et gabarits"),("Historique","Fichiers produits")]:
            tk.Button(side, text=f"  {name}   ›", anchor="w", relief="flat", bd=0,
                      bg=DARK, fg="white", activebackground=GREEN, activeforeground="white",
                      font=("Segoe UI", 11), padx=18, pady=12,
                      command=lambda n=name:self.show_page(n)).pack(fill="x", padx=8, pady=2)
        tk.Label(side, text="Projet pédagogique\nPython • PDF • Word", bg=DARK, fg="#AFC7C1",
                 font=("Segoe UI", 9), justify="left").pack(side="bottom", anchor="w", padx=20, pady=20)
        main = tk.Frame(shell, bg=BG)
        main.pack(side="left", fill="both", expand=True)
        top = tk.Frame(main, bg="white", height=76)
        top.pack(fill="x")
        top.pack_propagate(False)
        self.page_title = tk.Label(top, text="Créer un document", bg="white", fg=DARK,
                                   font=("Segoe UI", 18, "bold"))
        self.page_title.pack(side="left", padx=25, pady=18)
        tk.Button(top, text="Ouvrir le dossier", command=self.open_output,
                  bg="#E3EFEB", fg=GREEN, relief="flat", padx=14, pady=8).pack(side="right", padx=20)
        self.content = tk.Frame(main, bg=BG)
        self.content.pack(fill="both", expand=True, padx=24, pady=20)
        tk.Label(main, textvariable=self.status, bg="#E6ECE9", fg="#43534F",
                 anchor="w", padx=12, pady=7).pack(fill="x", side="bottom")

    def clear(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_page(self, page):
        self.page.set(page)
        self.clear()
        self.page_title.configure(text={"Créer":"Créer un document","Importer":"Générer depuis une liste",
                                        "Modèles":"Personnaliser les modèles","Historique":"Historique des fichiers"}[page])
        {"Créer":self.build_create, "Importer":self.build_import,
         "Modèles":self.build_templates, "Historique":self.build_history}[page]()

    def card(self, parent, title, subtitle=None):
        frame = tk.Frame(parent, bg="white", highlightbackground="#DCE5E1", highlightthickness=1)
        frame.pack(fill="x", pady=(0,14))
        tk.Label(frame, text=title, bg="white", fg=DARK, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=18, pady=(15,3))
        if subtitle:
            tk.Label(frame, text=subtitle, bg="white", fg="#71807B", font=("Segoe UI", 9)).pack(anchor="w", padx=18, pady=(0,12))
        return frame

    def field(self, parent, label, var, row, col=0, width=30):
        box = tk.Frame(parent, bg="white")
        box.grid(row=row, column=col, sticky="ew", padx=10, pady=7)
        tk.Label(box, text=label, bg="white", fg="#586762", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0,4))
        if label == "Civilité":
            ttk.Combobox(box, textvariable=var, values=["M.","Mme","Mlle"], state="readonly", width=width-2).pack(fill="x")
        else:
            ttk.Entry(box, textvariable=var, width=width).pack(fill="x")
        return box

    def build_create(self):
        intro = tk.Frame(self.content, bg=BG)
        intro.pack(fill="x", pady=(0,14))
        tk.Label(intro, text="Préparez votre document en quelques étapes.", bg=BG, fg="#65746F",
                 font=("Segoe UI", 10)).pack(anchor="w")
        card = self.card(self.content, "1. Type de document", "Choisissez le modèle qui correspond à votre besoin.")
        ttk.Combobox(card, textvariable=self.kind, values=list(TYPES), state="readonly", width=28).pack(anchor="w", padx=18, pady=(0,16))
        card2 = self.card(self.content, "2. Informations", "Les champs sont utilisés pour remplir automatiquement le modèle.")
        grid = tk.Frame(card2, bg="white")
        grid.pack(fill="x", padx=8, pady=(0,12))
        for col in range(3): grid.columnconfigure(col, weight=1)
        fields = [("Civilité",self.civilite),("Nom",self.nom),("Prénom",self.prenom),
                  ("Date",self.date),("Email",self.email),("Objet / motif",self.motif),
                  ("Montant",self.montant),("Note sur 20",self.note)]
        for i,(label,var) in enumerate(fields):
            self.field(grid,label,var,i//3,i%3)
        card3 = self.card(self.content, "3. Format de sortie", "Vous pouvez produire un PDF, un fichier Word, ou les deux.")
        options = tk.Frame(card3,bg="white"); options.pack(anchor="w",padx=18,pady=(0,15))
        tk.Checkbutton(options,text="PDF",variable=self.pdf,bg="white",activebackground="white").pack(side="left",padx=(0,20))
        tk.Checkbutton(options,text="Word (.docx)",variable=self.word,bg="white",activebackground="white").pack(side="left")
        tk.Button(self.content,text="Créer le document  →",command=self.create_document,
                  bg=GREEN,fg="white",activebackground="#337569",relief="flat",
                  font=("Segoe UI",10,"bold"),padx=20,pady=11).pack(anchor="e")

    def create_document(self):
        formats = (["PDF"] if self.pdf.get() else []) + (["Word"] if self.word.get() else [])
        if not formats:
            messagebox.showwarning("Format manquant","Cochez PDF et/ou Word.")
            return
        data = {"civilite":self.civilite.get(),"nom":self.nom.get(),"prenom":self.prenom.get(),
                "date":self.date.get(),"email":self.email.get(),"motif":self.motif.get(),
                "montant":self.montant.get(),"note":self.note.get()}
        try:
            number, paths = self.engine.generate(self.kind.get(),data,formats)
            self.status.set(f"Créé : {number}")
            messagebox.showinfo("Document créé",f"Numéro : {number}\n\nFichier(s) créé(s) :\n" + "\n".join(str(p) for p in paths))
        except Exception as e:
            messagebox.showerror("Impossible de créer le document",str(e))

    def build_import(self):
        card = self.card(self.content,"Importer un fichier","Les colonnes recommandées sont : type, nom, prenom, date, motif, montant, note.")
        row=tk.Frame(card,bg="white"); row.pack(fill="x",padx=18,pady=(0,12))
        ttk.Entry(row,textvariable=self.file).pack(side="left",fill="x",expand=True,padx=(0,8))
        tk.Button(row,text="Parcourir…",command=self.choose_file).pack(side="left")
        row2=tk.Frame(card,bg="white"); row2.pack(fill="x",padx=18,pady=(0,16))
        tk.Label(row2,text="Type par défaut :",bg="white").pack(side="left")
        ttk.Combobox(row2,textvariable=self.batch_kind,values=list(TYPES),state="readonly",width=18).pack(side="left",padx=10)
        tk.Button(row2,text="Utiliser le CSV d'exemple",command=self.load_example).pack(side="left",padx=10)
        self.batch_log=tk.Text(self.content,height=16,wrap="word",font=("Consolas",9),bd=0)
        self.batch_log.pack(fill="both",expand=True,pady=8)
        tk.Button(self.content,text="Générer tous les documents",command=self.run_batch,
                  bg=GREEN,fg="white",relief="flat",padx=16,pady=10).pack(anchor="e",pady=8)

    def choose_file(self):
        path=filedialog.askopenfilename(filetypes=[("Excel ou CSV","*.xlsx *.csv")])
        if path: self.file.set(path)

    def load_example(self):
        path=ROOT/"data"/"exemple.csv"
        self.file.set(str(path))
        self.batch_log.delete("1.0","end")
        self.batch_log.insert("end",f"Fichier sélectionné : {path}\n")

    def run_batch(self):
        try:
            path=self.file.get().strip()
            if not path: raise ValueError("Sélectionnez un fichier.")
            rows=read_rows(path)
            self.batch_log.insert("end",f"\n{len(rows)} ligne(s) à traiter.\n")
            done=0
            for i,row in enumerate(rows,1):
                row={str(k).strip().lower():v for k,v in row.items()}
                raw=str(row.get("type") or self.batch_kind.get()).strip().lower()
                aliases={"attestation":"Attestation","convocation":"Convocation","recu":"Reçu","reçu":"Reçu","bulletin":"Bulletin"}
                kind=aliases.get(raw,self.batch_kind.get())
                data={k:("" if v is None else str(v)) for k,v in row.items()}
                try:
                    number, paths=self.engine.generate(kind,data,["PDF"])
                    self.batch_log.insert("end",f"OK ligne {i} : {number} — {', '.join(p.name for p in paths)}\n")
                    done+=1
                except Exception as exc:
                    self.batch_log.insert("end",f"ERREUR ligne {i} : {exc}\n")
            self.batch_log.insert("end",f"\nTerminé : {done}/{len(rows)} document(s) créé(s).\n")
            self.status.set(f"Import terminé : {done}/{len(rows)}")
        except Exception as e:
            messagebox.showerror("Import impossible",str(e))

    def build_templates(self):
        card=self.card(self.content,"Textes des documents","Modifiez le texte et gardez les variables entre doubles accolades, par exemple {{ nom }}.")
        row=tk.Frame(card,bg="white"); row.pack(fill="x",padx=18,pady=(0,8))
        self.template_kind=tk.StringVar(value="Attestation")
        ttk.Combobox(row,textvariable=self.template_kind,values=list(TYPES),state="readonly",width=20).pack(side="left")
        tk.Button(row,text="Charger",command=self.load_template).pack(side="left",padx=8)
        tk.Button(row,text="Enregistrer",command=self.save_template).pack(side="left")
        self.template_editor=tk.Text(card,height=20,wrap="word",font=("Consolas",10),bd=1,relief="solid")
        self.template_editor.pack(fill="both",expand=True,padx=18,pady=(0,18))
        self.load_template()

    def load_template(self):
        try:
            text=self.engine.read_template(self.template_kind.get())
            self.template_editor.delete("1.0","end")
            self.template_editor.insert("1.0",text)
        except Exception as e: messagebox.showerror("Modèle",str(e))

    def save_template(self):
        try:
            self.engine.save_template(self.template_kind.get(),self.template_editor.get("1.0","end-1c"))
            messagebox.showinfo("Enregistré","Le modèle a été enregistré.")
        except Exception as e: messagebox.showerror("Modèle",str(e))

    def build_history(self):
        card=self.card(self.content,"Documents dans le dossier de sortie","Les fichiers PDF et Word produits apparaissent ici.")
        listbox=tk.Listbox(card,height=18,font=("Consolas",10),bd=0)
        listbox.pack(fill="both",expand=True,padx=18,pady=(0,16))
        files=sorted(OUTPUT.glob("*"),key=lambda p:p.stat().st_mtime,reverse=True)
        if not files: listbox.insert("end","Aucun document généré pour le moment.")
        for path in files: listbox.insert("end",f"{path.name}    ({path.stat().st_size} octets)")
        row=tk.Frame(self.content,bg=BG); row.pack(fill="x")
        tk.Button(row,text="Ouvrir le dossier de sortie",command=self.open_output,bg=GREEN,fg="white",relief="flat",padx=14,pady=9).pack(anchor="e")

    def open_output(self):
        OUTPUT.mkdir(exist_ok=True)
        os.startfile(str(OUTPUT))

def main():
    root=tk.Tk()
    AtelierApp(root)
    root.mainloop()

if __name__=="__main__":
    main()
