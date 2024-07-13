from flask import Flask, request, send_file, render_template, jsonify
from io import StringIO, BytesIO
from calendar import month
import datetime
import csv
import os
import sys
from jugaad_data.nse import full_bhavcopy_save , bhavcopy_index_save


app = Flask(__name__)

# year month and day are integer inputs
def download_csv_from_nse(year , month , day):
    try:
        if not os.path.exists("./bhav_copy"):
            os.makedirs("./bhav_copy")
        if not os.path.exists("./index"):
            os.makedirs("./index")
        
        full_bhavcopy_save(datetime.date(year,month,day) , "./bhav_copy")
        bhavcopy_index_save(datetime.date(year,month,day), "./index")
        return True
    except Exception as e:
        print("Error while downloading CSVs : ",e)
        return False

# day month_num year are of type string
def read_CSV_and_write_txt(bhav_copy_name , day , month_num , year):
    try:
        if not os.path.exists("./nse"):
            os.makedirs("./nse")
        
        txt_fileName = "./nse/"+year+"-"+month_num+"-"+day+"-NSE-EQ.txt"

        if os.path.exists(txt_fileName):
            return True

        
        #bhav copy
        csv_path  = "./bhav_copy/"+bhav_copy_name
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
        csv_path  = "./index/"+"ind_close_all_"+day+month_num+year+".csv"
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
        file_path = os.path.join("./nse" , file_name)

        today_date_time = datetime.date(int(year_str) , int(month_num_str) , int(day_str))
        month_shortForm = today_date_time.strftime("%b")
        bhav_copy_name = "sec_bhavdata_full_"+day_str+month_shortForm+year_str+"bhav.csv"

        if download_csv_from_nse(int(year_str)  , int(month_num_str) , int(day_str)):
            if read_CSV_and_write_txt(bhav_copy_name , day_str , month_num_str , year_str):
                if os.path.exists(file_path):
                    return send_file(file_path, mimetype='text/csv', as_attachment=True, attachment_filename=file_name)
                else:
                    raise FileNotFoundError("File not found")
            else:
                raise FileNotFoundError("File not found")
        else:
            raise FileNotFoundError("File not found")

        
    except Exception as e:
        error_response = {
            "error": str(e),
            "message": "An error occurred while processing your request"
        }
        return jsonify(error_response), 500

if __name__ == '__main__':
    app.run(debug=True)
