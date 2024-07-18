from flask import Flask, request, send_file, render_template, jsonify
import os
import requests
import asyncio

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
async def writeTxtFile(year , month , day):
    try:
        fullBhavCopy , indexData = await asyncio.gather(getFullBhavCopy(year , month , day) , getIndexData(year , month , day))
        if not fullBhavCopy or not indexData:
            return False
        rows = fullBhavCopy + indexData
        txt_fileName = "/tmp/test.txt"
        file1 = open(txt_fileName , "w")
        file1.writelines(rows)
        file1.close()
        return True
    except Exception as e:
        print(f"Error in writing txt file : {e}")
        return False
