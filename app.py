from flask import Flask, request, send_file, render_template, jsonify
from io import StringIO, BytesIO
from calendar import month
import datetime
import csv
import os
import sys
from jugaad_data.nse import full_bhavcopy_save , bhavcopy_index_save
import shutil
import tempfile


app = Flask(__name__)

# year month and day are integer inputs
def download_csv_from_nse(year , month , day):
    try:
        if not os.path.exists("/tmp/bhav_copy"):
            os.makedirs("/tmp/bhav_copy")
        if not os.path.exists("/tmp/index"):
            os.makedirs("/tmp/index")
        
        full_bhavcopy_save(datetime.date(year,month,day) , "/tmp/bhav_copy")
        bhavcopy_index_save(datetime.date(year,month,day), "/tmp/index")
        return True
    except Exception as e:
        print("Error while downloading CSVs : ",e)
        return False

# day month_num year are of type string
def read_CSV_and_write_txt(bhav_copy_name , day , month_num , year):
    try:
        if not os.path.exists("/tmp/nse"):
            os.makedirs("/tmp/nse")
        
        txt_fileName = "/tmp/nse/"+year+"-"+month_num+"-"+day+"-NSE-EQ.txt"

        if os.path.exists(txt_fileName):
            return True

        
        #bhav copy
        csv_path  = "/tmp/bhav_copy/"+bhav_copy_name
        csv_file = open(csv_path , "r")
        csv_reader = csv.reader(csv_file)
        date_num_text = year+month_num+day
        lines = []
        c = 0
        for line in csv_reader:
            if c == 0:
                c += 1
                continue
            if line[1].strip() == "EQ" or line[1].strip() == "BE":
                row = line[0].strip() + ',' + date_num_text +','+ line[4].strip() +','+ line[5].strip() +','+ line[6].strip() +','+ line[8].strip()+','+ line[10].strip()+"\n"
                lines.append(row)
        csv_file.close()

        # index
        csv_path  = "/tmp/index/"+"ind_close_all_"+day+month_num+year+".csv"
        csv_file = open(csv_path , "r")
        csv_reader = csv.reader(csv_file)
        c = 0
        for line in csv_reader:
            if c == 0:
                c+= 1
                continue
            if line[0] == "Nifty 50":
                row = "NSENIFTY," + date_num_text +','+ line[2] +','+ line[3] +','+ line[4] +','+ line[5]+',' + line[8]+"\n"
                lines.append(row)
            if line[0] == "Nifty Bank":
                row = "BANKNIFTY," + date_num_text +','+ line[2] +','+ line[3] +','+ line[4] +','+ line[5]+',' + line[8]+"\n"
                lines.append(row)
        
        file1 = open(txt_fileName , "w")
        file1.writelines(lines)
        file1.close()
        return True
    except Exception as e:
        print("error in read_CSV_and_write_txt function : " ,e )
        return False


@app.route('/')
def index():
    bhav_copy_temp_dir = tempfile.mkdtemp()
    print(bhav_copy_temp_dir)
    print("_____________________________________")
    if not os.path.exists("/tmp/nse"):
            os.makedirs("/tmp/nse")
    file1 = open("/tmp/nse/ok.txt" , "w")
    file1.writelines(["hii" , "byee"])
    
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        date_str = request.form['date']
        # Assume the CSV file is named based on the date (e.g., '2023-07-06.csv')
        print(date_str)
        date_list = date_str.split("-")
        year_str = date_list[0]
        month_num_str = date_list[1]
        day_str = date_list[2]

        file_name = year_str+"-"+month_num_str+"-"+day_str+"-NSE-EQ.txt"
        file_path = os.path.join("/tmp/nse" , file_name)

        today_date_time = datetime.date(int(year_str) , int(month_num_str) , int(day_str))
        month_shortForm = today_date_time.strftime("%b")
        bhav_copy_name = "sec_bhavdata_full_"+day_str+month_shortForm+year_str+"bhav.csv"

        if download_csv_from_nse(int(year_str)  , int(month_num_str) , int(day_str)):
            if read_CSV_and_write_txt(bhav_copy_name , day_str , month_num_str , year_str):
                if os.path.exists(file_path):
                    if os.path.exists("/tmp/bhav_copy"):
                        shutil.rmtree("/tmp/bhav_copy")
                    if os.path.exists("/tmp/index"):
                        shutil.rmtree("/tmp/index")
                    return send_file(file_path, mimetype='text/csv', as_attachment=True, attachment_filename=file_name)
                else:
                    raise FileNotFoundError("File not found")
            else:
                raise Exception("Data not found for the entered date or error in read csv and write function")
        else:
            raise Exception("Data not found for the entered date")

        
    except Exception as e:
        error_response = {
            "error": str(e),
            "message": "An error occurred while processing your request"
        }
        if os.path.exists("/tmp/bhav_copy"):
            shutil.rmtree("/tmp/bhav_copy")
        if os.path.exists("/tmp/index"):
            shutil.rmtree("/tmp/index")
        return jsonify(error_response), 500

if __name__ == '__main__':
    # app.run(debug=True)
    bhav_copy_temp_dir = tempfile.mkdtemp()
    print(bhav_copy_temp_dir)
    
    app.run(host='0.0.0.0')
