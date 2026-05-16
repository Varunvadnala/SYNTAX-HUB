# CSV to Excel Converter - Web Application

A professional web application for uploading, editing, and converting CSV files to Excel format.

## ⚡ Quick Start

### Windows
```bash
double-click run_web_app.bat
```
Or manually:
```bash
pip install -r requirements.txt
python app.py
```

### Mac/Linux
```bash
pip install -r requirements.txt
python app.py
```

Then open: **http://localhost:5000**

---

## ✨ Features

✅ Upload CSV files (drag & drop)  
✅ Live data editing in browser  
✅ Add/delete rows and columns  
✅ Download as Excel (styled) or CSV  
✅ Auto data cleaning & validation  
✅ Professional UI design  
✅ Mobile-responsive  
✅ No database needed  

---

## 📁 Project Structure

```
.
├── app.py                 # Flask backend
├── requirements.txt       # Dependencies
├── run_web_app.bat       # Windows launcher
├── run_web_app.sh        # Mac/Linux launcher
├── sample_data.csv       # Test data
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Functionality
└── uploads/              # Temporary files
```

---

## 🔧 Requirements

- Python 3.6+
- Flask 2.0+
- pandas
- openpyxl

All installed via: `pip install -r requirements.txt`

---

## 📝 Usage

1. **Upload** - Drag CSV file to browser
2. **Edit** - Click cells to modify data
3. **Manage** - Add/delete rows and columns
4. **Download** - Export as Excel or CSV

---

## 🌐 Access

Once running, open your browser to:
- **Local**: http://localhost:5000
- **Network**: http://<your-ip>:5000

---

## 🛑 Stop Server

Press `CTRL+C` in the terminal

---

## 📞 Support

Check terminal output for logs and debugging information.
