from calendar import month
import datetime
from jugaad_data.nse import bhavcopy_save
import csv
import os
import sys
from jugaad_data.nse import index_csv

def download_csv_from_nse(year , month , day):
    # 0 - not downloaded
    # 1 - downloaded
    try:
        bhavcopy_save(datetime.date(year,month,day) , "./bhav_copy")
        # index_csv(symbol="NIFTY BANK", from_date=datetime.date(year,month,day),
            # to_date=datetime.date(year,month,day), output="./index/bankNifty.csv")
        # index_csv(symbol="NIFTY 50", from_date=datetime.date(2024,3,11),
            # to_date=datetime.date(2024,3,19), output="./index/Nifty50.csv")
    # temporary adding 000 for bank nifty and nifty 50 
        return 1
    except Exception as e:
        print("Error while downloading CSVs : ",e)
        return 0

def read_CSV_and_write_txt(bhav_copy_name , day , month_num , year):
    try:
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
            if line[1] == "EQ" or line[1] == "BE":
                row = line[0] + ',' + date_num_text +','+ line[2] +','+ line[3] +','+ line[4] +','+ line[5]+','+ line[8]+"\n"
                lines.append(row)
        csv_file.close()


        row = "NSENIFTY" +',' + date_num_text + ',0,0,0,0,0,0\n'
        lines.append(row) # temp soln , till juggad_data is fixed
        row = "BANKNIFTY" +',' + date_num_text + ',0,0,0,0,0,0\n'
        lines.append(row) # temp soln , till juggad_data is fixed

        # # nifty 50
        # csv_path  = "./index/Nifty50.csv"
        # csv_file = open(csv_path , "r")
        # csv_reader = csv.reader(csv_file)
        # c = 0
        # for line in csv_reader:
        #     if c == 2:
        #         row = "NSENIFTY" +',' + date_num_text + ',' +line[2] +','+ line[3] +','+ line[4] +','+ line[5]+',0,0\n'
        #         lines.append(row)
        #         break
        #     c+=1
        # csv_file.close()

        # # bank Nifty
        # csv_path  = "./index/bankNifty.csv"
        # csv_file = open(csv_path , "r")
        # csv_reader = csv.reader(csv_file)
        # c = 0
        # for line in csv_reader:
        #     if c == 2:
        #         row = "BANKNIFTY" +',' + date_num_text + ',' +line[2] +','+ line[3] +','+ line[4] +','+ line[5]+',0,0\n'
        #         lines.append(row)
        #         break
        #     c+=1
        # csv_file.close()

        txt_fileName = "./nse/"+year+"-"+month_num+"-"+day+"-NSE-EQ.txt"
        file1 = open(txt_fileName , "a")
        file1.writelines(lines)
        file1.close()
    except Exception as e:
        print("error in read_CSV_and_write_txt function : " ,e )


# bhavcopy_save(date(2023, 4, 6), "./bhav_copy")
# read_CSV_and_write_txt("cm06Apr2023bhav.csv" , "06" , "04" , "2023")
if __name__ == "__main__":
    n = len(sys.argv)
    if n != 4:
        print("Wrong date format please enter date correctly")
        exit()
    try:
        today_date_time = datetime.date(int(sys.argv[3]) , int(sys.argv[2]) , int(sys.argv[1]))
        day = today_date_time.strftime("%d")
        month_shortForm = today_date_time.strftime("%b")
        month_num = today_date_time.strftime("%m")
        year = today_date_time.strftime("%Y")
        if download_csv_from_nse(int(year) , int(month_num) , int(day)) == 1:
            bhav_copy_name = "cm"+day+month_shortForm+year+"bhav.csv"
            read_CSV_and_write_txt(bhav_copy_name , day , month_num , year)
            bhav_copy_path = "./bhav_copy/"+bhav_copy_name
            os.remove(bhav_copy_path)
            # os.remove("./index/Nifty50.csv")
            # os.remove("./index/bankNifty.csv")
        else:
            print("Bhav copy was not found for the input date")

    except Exception as e:
        print("Some error occured in the main function , make sure the format of date entered is correct : ", e)
        exit()