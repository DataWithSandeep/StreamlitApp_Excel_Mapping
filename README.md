# 🏗️ Streamlit App for Data Mapping  

This is a **Streamlit-based web application** that processes and maps data from Excel files. The app allows users to upload two Excel files and generate a processed output file. Additionally, users can specify the final filename for the Excel output.  

---

## 🚀 Features  
✅ Upload two Excel files for processing  
✅ Automatically map and transform data  
✅ Download the processed Excel file  
✅ Option to specify the output filename  
✅ Simple and interactive UI powered by **Streamlit**  

---

## 📂 Folder Structure  
```
📦 project-root/
 ┣ 📜 app.py             # Main Streamlit App
 ┣ 📜 requirements.txt   # Dependencies
 ┗ 📜 README.md          # Project Documentation
```

---

## 📌 Requirements  
Ensure you have **Python 3.8+** installed. Install dependencies using:  
```sh
pip install -r requirements.txt
```

---

## 🛠️ Running the App Locally  
To run the Streamlit app on your local machine:  
```sh
streamlit run app.py
```
This will start a web server and open the app in your browser at:  
```
http://localhost:8501
```

---

## 🌍 Deploying on Render  
You can easily **deploy this app on Render** for free by following these steps:  

### 1️⃣ **Push Your Code to GitHub**
If your project is not in GitHub, push it:  
```sh
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/yourrepo.git
git push -u origin main
```

### 2️⃣ **Create `requirements.txt` (If Not Already Created)**
Run:  
```sh
pip freeze > requirements.txt
```
Then remove unnecessary dependencies, keeping only:  
```
streamlit
pandas
openpyxl
xlsxwriter
```
Commit the changes:  
```sh
git add requirements.txt
git commit -m "Added requirements.txt"
git push origin main
```

### 3️⃣ **Deploy on Render**
1. **Go to** [Render](https://render.com) and log in.  
2. Click **"New Web Service"** → Connect your GitHub repository.  
3. **Set up deployment:**
   - **Build Command:**  
     ```sh
     pip install -r requirements.txt
     ```
   - **Start Command:**  
     ```sh
     streamlit run app.py --server.port=10000 --server.headless=true
     ```
   - Select **Python 3.x** as the environment.  
4. Click **Deploy** 🚀  

After deployment, your app will be available at:  
```
https://yourapp.onrender.com
```

---

## 🛠️ Customizing the App  
- Modify **`app.py`** to change UI or logic.  
- Adjust **Excel processing** logic inside `mapping_fun()`.  

---

## 📬 Feedback & Contributions  
Feel free to **open an issue** or **submit a pull request** if you have suggestions or improvements!  

---

## 📜 License  
This project is **open-source** and free to use under the **MIT License**.

---

### **🎯 Happy Coding! 🚀**
