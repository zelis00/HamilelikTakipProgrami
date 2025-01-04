#veri girişi var, try-except kullanılmadı if-else ile yaptım. 
#VS Tkinter ile ara yüz uyarladım.
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox, Toplevel
from tkinter import ttk  # ttk importunu ekledim
import pandas as pd
import matplotlib.pyplot as plt #çizim için
import os


# Aşağıda verileri kaydetmek için DataFrame (pandas kütüphanesinde bir nesne olarak geçer/veri yapısı) yapısını gösterdik
def Load_diary(filename='pregnancy_diary.csv'):
    if os.path.exists(filename):
        diary = pd.read_csv(filename)
    else:
        diary = pd.DataFrame(columns=["hafta", "kilo", "ruh hali", "belirtiler", "notlar"])
    return diary

def save_diary(diary, filename='pregnancy_diary.csv'):
    diary.to_csv(filename, index=False)

# Kilo değişimlerinin grafiği:
def plot_weight(diary):
    if "kilo" in diary.columns and not diary["kilo"].isnull().all():
        diary["hafta"] = pd.to_numeric(diary["hafta"], errors='coerce')
        diary["kilo"] = pd.to_numeric(diary["kilo"], errors='coerce')
        diary = diary.dropna(subset=["hafta", "kilo"]).sort_values("hafta")

        plt.figure(figsize=(10, 5))
        plt.plot(diary["hafta"], diary["kilo"], marker='o', color='b')
        plt.title("Hamilelik Sürecindeki Kilo Değişimi")
        plt.xlabel("Hafta")
        plt.ylabel("Kilo (kg)")
        plt.grid()
        plt.show()
    else:
        messagebox.showerror("Veri Yok", "Kilo verisi bulunamadı.")

# Veri girişlerini gösterdik burada
def show_entries(diary):
    entries_window = Toplevel()
    entries_window.title("Veri Girişleri")

    tree = ttk.Treeview(entries_window, columns=("hafta", "kilo", "ruh hali", "belirtiler", "notlar"), show="headings")
    tree.heading("hafta", text="Hafta")
    tree.heading("kilo", text="Kilo (kg)")
    tree.heading("ruh hali", text="Ruh Hali")
    tree.heading("belirtiler", text="Belirtiler")
    tree.heading("notlar", text="Notlar")

    for _, row in diary.iterrows():
        tree.insert("", "end", values=(row["hafta"], row["kilo"], row["ruh hali"], row["belirtiler"], row["notlar"]))

    tree.pack(fill="both", expand=True)

    def delete_entry():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Seçim Yok", "Lütfen silmek istediğiniz bir giriş seçin.")
            return

        item_values = tree.item(selected_item)["values"]
        week_to_delete = item_values[0]

        confirm_delete = messagebox.askyesno("Silme Onayı", f"{week_to_delete}. haftadaki veriyi silmek istediğinize emin misiniz?")
        if confirm_delete:
            diary.drop(diary[diary["hafta"] == week_to_delete].index, inplace=True)
            tree.delete(selected_item)

            save_diary(diary)
            messagebox.showinfo("Silme Başarılı", f"{week_to_delete}. haftadaki veri başarıyla silindi.")

    # Veri silme butonunu eklediğimiz bölüm burası:
    delete_button = tk.Button(entries_window, text="Seçili veriyi Sil", command=delete_entry)
    delete_button.pack(pady=10)

class App:
    def __init__(self, root):
        self.root = root
        self.diary = Load_diary()

        # Pencere ayarlarını buradan ayarlıyoruz
        root.title("Hamilelik Dönemi Takip Günlüğü❤️")
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # Hafta etiketi ve giriş alanı:
        self.week_label = tk.Label(root, text="Hafta:", font=("Times", 10))
        self.week_label.place(x=10, y=30, width=70, height=25)

        self.week_entry = tk.Entry(root, font=("Times", 10))
        self.week_entry.place(x=130, y=30, width=182, height=30)

        # Kilo etiketi ve giriş alanı:
        self.weight_label = tk.Label(root, text="Kilo (kg):", font=("Times", 10))
        self.weight_label.place(x=10, y=80, width=70, height=25)

        self.weight_entry = tk.Entry(root, font=("Times", 10))
        self.weight_entry.place(x=130, y=80, width=181, height=30)

        # Ruh hali etiketi ve giriş alanı:
        self.mood_label = tk.Label(root, text="Ruh Hali:", font=("Times", 10))
        self.mood_label.place(x=10, y=130, width=70, height=25)

        self.mood_entry = tk.Entry(root, font=("Times", 10))
        self.mood_entry.place(x=130, y=130, width=181, height=30)

        # Belirtiler etiketi ve giriş alanı:
        self.symptoms_label = tk.Label(root, text="Belirtiler:", font=("Times", 10))
        self.symptoms_label.place(x=10, y=180, width=70, height=25)

        self.symptoms_entry = tk.Entry(root, font=("Times", 10))
        self.symptoms_entry.place(x=130, y=180, width=180, height=30)

        # Notlar etiketi ve giriş alanı:
        self.notes_label = tk.Label(root, text="Notlar:", font=("Times", 10))
        self.notes_label.place(x=10, y=230, width=70, height=25)

        self.notes_entry = tk.Entry(root, font=("Times", 10))
        self.notes_entry.place(x=130, y=220, width=181, height=60)

        # Veri/Bilgi ekle butonu:
        self.add_button = tk.Button(root, text="Veri/Bilgi Ekle", font=("Times", 10), command=self.add_entry)
        self.add_button.place(x=430, y=30, width=141, height=30)

        # Kilo değişim grafiği butonu:
        self.plot_button = tk.Button(root, text="Kilo Değişim Grafiği", font=("Times", 10), command=self.plot_weight)
        self.plot_button.place(x=430, y=70, width=141, height=30) 
        self.show_button = tk.Button(root, text="Veri Girişlerini Göster", font=("Times", 10), command=self.show_entries)
        self.show_button.place(x=430, y=110, width=144, height=45)

    # Yeni giriş ekleme:
    def add_entry(self):
        week = self.week_entry.get()
        weight = self.weight_entry.get()
        mood = self.mood_entry.get()
        symptoms = self.symptoms_entry.get()
        notes = self.notes_entry.get()

        if not week or not weight:
            messagebox.showerror("Eksik Bilgi", "Lütfen hafta numarasını ve kilo bilgilerini giriniz.")
            return
        
        # Hafta ve Kilo girişlerinin sayısal olup olmadığını kontrol et
        if not week.isdigit():
            messagebox.showerror("Geçersiz Hafta", "Lütfen bir hafta bilgisi girin.")
            return

        if not weight.replace('.', '', 1).isdigit() or weight.count('.') > 1:  # Sayısal ve ondalıklı sayı kontrolü
            messagebox.showerror("Geçersiz Kilo", "Lütfen bir kilo bilgisi girin.")
            return

        week = int(week)

        if week > 40:
            messagebox.showerror("Geçersiz Hafta", "Hamilelik süreci maksimum 40 hafta sürer.")
            return

        new_entry = pd.DataFrame({
            "hafta": [week],
            "kilo": [weight],
            "ruh hali": [mood],
            "belirtiler": [symptoms],
            "notlar": [notes]
        })
        self.diary = pd.concat([self.diary, new_entry], ignore_index=True)
        save_diary(self.diary)

        # Alanları temizle
        self.week_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.mood_entry.delete(0, tk.END)
        self.symptoms_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)

    # Kilo değişim grafiği:
    def plot_weight(self):
        plot_weight(self.diary)

    # Veri girişlerini gösterme:
    def show_entries(self):
        show_entries(self.diary)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
