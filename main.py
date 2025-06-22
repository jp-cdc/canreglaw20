import tkinter as tk
import tkinter.filedialog
import os
import sub  #サブモジュールをインポート(自作)

class TKinterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("がん登録推進法20条情報＋α加工ツール")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        
        label = tk.Label(self.root, text="\n日付情報を診断日を起点とした日数に変換します。\n対象ファイル・出力フォルダを選びましょう。\n 出力フォルダには元ファイル＋'-out'というファイルが作成されます。")
        label.pack(pady=15)

        button = tk.Button(self.root, text="①元ファイルを選択", width=20)
        button.bind('<ButtonPress>', self.select_file)
        button.pack(pady=5)

        self.file_name = tk.StringVar()
        self.file_name.set('未選択')

        file_label = tk.Label(self.root, textvariable=self.file_name)
        file_label.pack(pady=20)

        button2 = tk.Button(self.root, text="②出力フォルダを選択", width=20)
        button2.bind('<ButtonPress>', self.select_folder)
        button2.pack(pady=5)

        self.outfolder = tk.StringVar()
        self.outfolder.set("未選択") 

        folder_label = tk.Label(self.root, textvariable=self.outfolder)
        folder_label.pack(pady=15)

        button3 = tk.Button(self.root, text="③処理実行", width=20)
        button3.bind('<ButtonPress>', self.process_files)
        button3.pack(pady=15)

        button4 = tk.Button(self.root, text="終了", width=20, command=self.root.destroy)
        button4.bind('<ButtonPress>')
        button4.pack(pady=15)
        self.root.mainloop()
        
    def select_file(self, event):
        fTyp = [("院内がん登録 file", "*.csv"), ("All files", "*.*")]
        iDir = os.path.dirname(__file__)
        filename = tk.filedialog.askopenfilename(filetypes=fTyp, title="元ファイルの選択", initialdir=iDir)
        if filename:
            self.file_name.set(filename)
            with open(filename) as f:
                first_line = f.readline().strip()
                if not first_line.startswith('施設番号'):
                    tk.messagebox.showerror("エラー", "１行目が項目行ではないので適切なファイルではありません。")
                    self.file_name.set("未選択")
                else:
                    first_line_list = first_line.split(',')
                    if len(first_line_list) < 70:
                        tk.messagebox.showerror("エラー", "項目が足りないので適切なファイルではありません。")
                        self.file_name.set("未選択")
                    else:
                        # サブモジュールの関数を呼び出して開始日と日付番号を取得
                        self.start, self.dateitems = sub.create_list(first_line_list)
        else:
            self.file_name.set("未選択")

    def select_folder(self, event):
        iDir = os.path.dirname(__file__)
        foldername = tk.filedialog.askdirectory(initialdir=iDir, title="出力フォルダを選択")
        if foldername:
            self.outfolder.set(foldername)
        else:
            self.outfolder.set("未選択")

    def process_files(self, event):
        input_file = self.file_name.get()
        output_folder = self.outfolder.get()
        outbasefile = os.path.basename(input_file)[:-4] + '-out.csv'
        if input_file == "未選択" or output_folder == "未選択":
            tk.messagebox.showwarning("警告", "ファイルと出力先フォルダを選択してください。")
            return
        if not os.path.exists(input_file):
            tk.messagebox.showerror("エラー", f"選択された{input_file}が存在しません。")
            return
        if not os.path.exists(output_folder):
            tk.messagebox.showerror("エラー", f"選択された出力先フォルダ{output_folder}が存在しません。")
            return
        while os.path.exists(output_folder+"/"+outbasefile):
            outbasefile = outbasefile.split('.')[0] + '-n' + '.csv'

        sub.fileconvert(input_file, self.start, self.dateitems, output_folder+ "/" + outbasefile)
        tk.messagebox.showinfo("情報", f"{outbasefile}を出力しました。")
        self.root.destroy()

TKinterApp()

#        start = 21
#        dateitems = [22, 23, 24, 46, 50, 54, 59, 63, 67, 77, 78]
