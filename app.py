import tkinter as tk
from tkinter import filedialog, messagebox
import os
from datetime import datetime
import requests
import asyncio

def download_files(date_str, download_path):
    # Your function logic here
    # For demonstration, let's just create a dummy file with the given date
    try:
        date_list = date_str.split("-")
        year = date_list[0]
        month = date_list[1]
        day = date_list[2]
        file_name = f'{year}-{month}-{day}-NSE-EQ.txt'
        file_path = os.path.join(download_path, file_name)
        res = asyncio.run(writeTxtFile(year , month , day , file_path))
        if res:
            messagebox.showinfo("Success", f"File downloaded successfully: {file_path}")
        else:
            messagebox.showinfo("Error" , "Maybe data not found for this date , or some other error occurred , try some other date")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# year month and day are of type string
async def getFullBhavCopy(year , month , day):
    try:
        url = f"https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{day}{month}{year}.csv"
        s = requests.Session()
        h = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "accept-encoding": "gzip, deflate, br",
            "accept": """text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9""",
        }
        s.headers.update(h)
        r = s.get(url , timeout=30)
        if r.status_code == 200:
            date_num_text = year+month+day
            lines = r.text.split("\n")
            lines = lines[1:len(lines)-2]
            rows = []
            for line in lines:
                row = line.split(",")
                if row[1].strip() == "EQ" or row[1].strip() == "BE":
                    r = row[0].strip() + ',' + date_num_text +','+ row[4].strip() +','+ row[5].strip() +','+ row[6].strip() +','+ row[8].strip()+','+ row[10].strip()+"\n"
                    rows.append(r)
            return rows
        return False
    except Exception as e:
        print(f"Error in getting full bhav copy function : {e}")
        return False

# year month and day are of type string
async def getIndexData(year , month , day):
    try:
        url = f"https://www.niftyindices.com/Daily_Snapshot/ind_close_all_{day}{month}{year}.csv"
        s = requests.Session()
        h = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "accept-encoding": "gzip, deflate, br",
            "accept": """text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9""",
        }
        s.headers.update(h)
        r = s.get(url , timeout=30)
        if r.status_code == 200:
            date_num_text = year+month+day
            lines = r.text.split("\n")
            lines = lines[1:len(lines)-2]
            rows = []
            for line in lines:
                row = line.split(",")
                if row[0] == "Nifty 50":
                    r = "NSENIFTY," + date_num_text +','+ row[2] +','+ row[3] +','+ row[4] +','+ row[5]+',' + row[8]+"\n"
                    rows.append(r)
                if row[0] == "Nifty Bank":
                    r = "BANKNIFTY," + date_num_text +','+ row[2] +','+ row[3] +','+ row[4] +','+ row[5]+',' + row[8]+"\n"
                    rows.append(r)
            return rows    
        return False
    except Exception as e:
        print(f"Error in getting index data function : {e}")
        return False

# year month and day are of type string
async def writeTxtFile(year , month , day , file_path ):
    try:
        fullBhavCopy , indexData = await asyncio.gather(getFullBhavCopy(year , month , day) , getIndexData(year , month , day))
        if not fullBhavCopy or not indexData:
            return False
        rows = fullBhavCopy + indexData
        
        file1 = open(file_path , "w")
        file1.writelines(rows)
        file1.close()
        return True
    except Exception as e:
        print(f"Error in writing txt file : {e}")
        return False


def browse_path():
    download_path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, download_path)

def run_function():
    date_str = date_entry.get()
    download_path = path_entry.get()
    if not date_str or not download_path:
        messagebox.showerror("Input Error", "Please provide both date and download path.")
        return
    download_files(date_str, download_path)

app = tk.Tk()
app.title("Download App")

tk.Label(app, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
date_entry = tk.Entry(app)
date_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(app, text="Download Path:").grid(row=1, column=0, padx=10, pady=10)
path_entry = tk.Entry(app)
path_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=browse_path).grid(row=1, column=2, padx=10, pady=10)

tk.Button(app, text="Run", command=run_function).grid(row=2, column=1, padx=10, pady=10)

app.mainloop()
