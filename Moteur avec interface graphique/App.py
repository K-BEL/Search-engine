import tkinter as tk
import tkinter.font as tkFont
import Search as s
import os
import re 

class App:
    def __init__(self, root):
        #setting title
        root.title("Moteur de recherche")
        #setting window size
        self.width=600
        self.height=500
        self.screenwidth = root.winfo_screenwidth()
        self.screenheight = root.winfo_screenheight()
        self.alignstr = '%dx%d+%d+%d' % (self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2)
        root.geometry(self.alignstr)
        root.resizable(width=False, height=False)

        self.q = tk.IntVar()
        self.q.set(0)
        
        self.base_dir = r"E:\Downloads\cours\S5\Technologie de moteurs de recherche\Projet\Moteur de recherche\Projet\projectCorpus"
        self.file_list = os.listdir(self.base_dir)
    
        self.dict = s.create_dict(self.base_dir)
        self.pdict = s.create_permuterm(self.dict.keys())
        
        self.GButton_13=tk.Button(root)
        self.GButton_13["bg"] = "#efefef"
        self.ft = tkFont.Font(family='Times',size=10)
        self.GButton_13["font"] = self.ft
        self.GButton_13["fg"] = "#000000"
        self.GButton_13["justify"] = "center"
        self.GButton_13["text"] = "Search"
        self.GButton_13.place(x=410,y=150,width=150,height=32)
        self.GButton_13["command"] = self.GButton_13_command

        self.GLineEdit_248=tk.Entry(root)
        self.GLineEdit_248["borderwidth"] = "1px"
        self.ft = tkFont.Font(family='Times',size=10)
        self.GLineEdit_248["font"] = self.ft
        self.GLineEdit_248["fg"] = "#333333"
        self.GLineEdit_248["justify"] = "center"
        self.GLineEdit_248["text"] = "Key Word"
        self.GLineEdit_248.place(x=30,y=150,width=350,height=32)

        self.GRadio_146=tk.Radiobutton(root)
        self.ft = tkFont.Font(family='Times',size=10)
        self.GRadio_146["font"] = self.ft
        self.GRadio_146["fg"] = "#333333"
        self.GRadio_146["justify"] = "center"
        self.GRadio_146["text"] = "Query Search"
        self.GRadio_146.place(x=10,y=40,width=133,height=59)
        # GRadio_146["command"] = self.GRadio_146_command
        self.GRadio_146["variable"] = self.q
        self.GRadio_146["value"] = 1
        

        self.GRadio_440=tk.Radiobutton(root)
        self.ft = tkFont.Font(family='Times',size=10)
        self.GRadio_440["font"] = self.ft
        self.GRadio_440["fg"] = "#333333"
        self.GRadio_440["justify"] = "center"
        self.GRadio_440["text"] = "Generate Global Text  Table"
        self.GRadio_440.place(x=130,y=40,width=214,height=59)
        # GRadio_440["command"] = self.GRadio_440_command
        self.GRadio_440['variable'] = self.q
        self.GRadio_440['value'] = 2 
        
        self.GRadio_610=tk.Radiobutton(root)
        self.ft = tkFont.Font(family='Times',size=10)
        self.GRadio_610["font"] =self.ft
        self.GRadio_610["fg"] = "#333333"
        self.GRadio_610["justify"] = "center"
        self.GRadio_610["text"] = "Generate Permuterm Index Table"
        self.GRadio_610.place(x=370,y=40,width=226,height=59)
        # GRadio_610["command"] = self.GRadio_610_command
        self.GRadio_610["variable"] = self.q
        self.GRadio_610["value"] = 3
        
        self.GListBox_799=tk.Listbox(root)
        self.GListBox_799["borderwidth"] = "1px"
        self.ft = tkFont.Font(family='Times',size=10)
        self.GListBox_799["font"] = self.ft
        self.GListBox_799["fg"] = "#333333"
        self.GListBox_799["justify"] = "center"
        self.GListBox_799.place(x=30,y=240,width=511,height=165)
        
        
        self.scrollbar = tk.Scrollbar(root )
        self.scrollbar.pack( side = tk.RIGHT, fill = tk.Y )
        self.GListBox_799.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.GListBox_799.yview)
        
    def GButton_13_command(self):
        # if self.q == 1 :
        input_query = self.GLineEdit_248.get()
        mode = self.q.get()
        # self.GListBox_799.clear()
        result = []
        if  mode : 
          
            if self.GListBox_799.size() > 0 :
                self.GListBox_799.delete(0,tk.END)
            
            if mode == 1 and input_query :
                input_terms = s.sp_text(input_query)
                w_query_terms = []
                b_query_terms = []
                for w in input_terms:
                    if '*' in w:
                        w_query_terms.append(w)
                    else:
                        b_query_terms.append(w)
                      
                if len(w_query_terms) > 0:
                    result1 = s.wc_query(self.dict, self.pdict, w_query_terms) 
                    result.append(result1)  
    
                matches = re.findall(r'\"(.+?)\"', input_query)
                ph_query = ",".join(matches)
                p_query_list = ph_query.split(",")
                
                result2 = []
                if ph_query != "":
                    for p_query in p_query_list:
                        temp = s.phrase_query(self.dict, p_query)
                        
                        if len(result2) == 0:
                            result2 = temp
                        else:
                            result2 = [x for x in result2 if x in temp]
                    result.append(result2)
                    
                if len(b_query_terms) > 0:
                    result3 = s.boolean_query(self.dict, b_query_terms)
                    result.append(result3)
                 
            if len(result) > 0:       
                result_set = set(result[0]).intersection(*result)
                result = list(result_set)
            
                if len(result) > 0:
                    result = [x[:-4] for x in result]
                    self.GListBox_799.insert(tk.END , *result)
                else:
                    self.GListBox_799.insert(tk.END , "désolé pas de correspondance")
                
            elif mode == 2 :
                 for key, value in self.dict.items():
                    self.GListBox_799.insert(tk.END , '{} \n'.format(key))
            elif mode == 3 :
                for key, value in self.pdict.items():
                    self.GListBox_799.insert(tk.END , '{}  : {} \n'.format(key, value))
            else :
                pass


    

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
