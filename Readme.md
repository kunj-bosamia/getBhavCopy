# getBhavCopy

This application provides a comprehensive solution to download daily bhavcopy files containing open, high, low, close, and volumes of each script, including Nifty50 and BankNifty. The application has two main functionalities: a scheduled cron job and a local GUI app.

## Features

### 1. Scheduled Cron Job
- **Runs Daily:** The cron job runs every day at 9:30 PM.
- **Uploads to Google Drive:** The generated TXT file is automatically uploaded to Google Drive. The drive link is [here](https://drive.google.com/drive/u/0/folders/1wA5duO0osm4mrZ8g5iJuh_pmkr8wD6vG).
- **Manual Trigger:** There is a manual trigger for the cron job, which is accessible only to repo owners.

### 2. Local GUI Application
- **Inputs:** The local GUI app allows users to input a date and a path where they want to generate the file.
- **File Contents:** The generated TXT file includes open, high, low, close, and volumes for each script, as well as Nifty50 and BankNifty.

## Download the Executable

You can download the latest version of the local GUI application [here](https://github.com/kunj-bosamia/getBhavCopy/releases/latest/app.exe).

### How to Use the Local GUI App

1. **Download and Run:** Download the `.exe` file from the link above and run it.
2. **Input Date:** Enter the date for which you want to generate the bhavcopy in the format `YYYY-MM-DD`.
3. **Select Path:** Choose the path where you want the file to be saved.
4. **Generate File:** Click the "Run" button to generate the file at the specified location.

## How the Cron Job Works

The cron job is defined in the `.github/workflows/cron.yml` file. It automatically runs every day at 9:30 PM and uploads the generated TXT file to Google Drive. The file contains the daily market data including open, high, low, close, and volumes of each script, along with Nifty50 and BankNifty data.

### Manual Trigger for Cron Job

The cron job can also be triggered manually by the repo owners using the GitHub Actions tab.

### File Details

The TXT file generated by both the cron job and the local GUI app contains the following information:
- **Open**
- **High**
- **Low**
- **Close**
- **Volumes**

For all traded scripts, including Nifty50 and BankNifty.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
