from flask import Flask, request, send_file, render_template, jsonify
import os
import requests

# year month and day are of type string
def getFullBhavCopy(year , month , day):
    try:
        url = f"https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{day}{month}{year}.csv"
        s = requests.Session()
        h = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "accept-encoding": "gzip, deflate, br",
            "accept": """text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9""",
        }
        s.headers.update(h)
        r = s.get(url , timeout=4)
        if r.status_code == 200:
            lines = r.text.split("\n")
            return lines[1:len(lines)-2]
        return False
    except Exception as e:
        print(f"Error in getting full bhav copy function : {e}")
        return False

# year month and day are of type string
def getIndexData(year , month , day):
    try:
        url = f"https://www.niftyindices.com/Daily_Snapshot/ind_close_all_{day}{month}{year}.csv"
        s = requests.Session()
        h = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "accept-encoding": "gzip, deflate, br",
            "accept": """text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9""",
        }
        s.headers.update(h)
        r = s.get(url , timeout=4)
        if r.status_code == 200:
            lines = r.text.split("\n")
            return lines[1:len(lines)-2]
        return False
    except Exception as e:
        print(f"Error in getting index data function : {e}")

# year month and day are of type string
def writeTxtFile(year , month , day):
    try:
        fullBhavCopy = getFullBhavCopy(year , month , day)
        indexData = getIndexData(year , month , day)
        date_num_text = year+month+day
        if not fullBhavCopy or not indexData:
            return False

        rows = []
        for line in fullBhavCopy:
            row = line.split(",")
            if row[1].strip() == "EQ" or row[1].strip() == "BE":
                r = row[0].strip() + ',' + date_num_text +','+ row[4].strip() +','+ row[5].strip() +','+ row[6].strip() +','+ row[8].strip()+','+ row[10].strip()+"\n"
                rows.append(r)
        
        for line in indexData:
            row = line.split(",")
            if row[0] == "Nifty 50":
                r = "NSENIFTY," + date_num_text +','+ row[2] +','+ row[3] +','+ row[4] +','+ row[5]+',' + row[8]+"\n"
                rows.append(r)
            if row[0] == "Nifty Bank":
                r = "BANKNIFTY," + date_num_text +','+ row[2] +','+ row[3] +','+ row[4] +','+ row[5]+',' + row[8]+"\n"
                rows.append(r)
        
        txt_fileName = "/tmp/"+year+"-"+month+"-"+day+"-NSE-EQ.txt"
        file1 = open(txt_fileName , "w")
        file1.writelines(rows)
        file1.close()
        return True
    except Exception as e:
        print(f"Error in writing txt file : {e}")
        return False


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        date_str = request.form['date']
        date_list = date_str.split("-")
        year = date_list[0]
        month = date_list[1]
        day = date_list[2]

        txt_file_path = "/tmp/"+year+"-"+month+"-"+day+"-NSE-EQ.txt"
        txt_file_name = year+"-"+month+"-"+day+"-NSE-EQ.txt"
        if not os.path.exists(txt_file_path):
            if not writeTxtFile(year , month , day):
                raise Exception("Either data not found for this day , or some error occurred in writeTxtFile check logs")
        return send_file(txt_file_path, mimetype='text/csv', as_attachment=True, attachment_filename=txt_file_name)
    except Exception as e:
        error_response = {
            "error": str(e),
            "message": "An error occurred while processing your request"
        }
        return jsonify(error_response), 500

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')
