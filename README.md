# **API Project Week** #  
This project was developed by Katharina, Daria, Martha, Birol, and Dorian. It uses an API and the CTk framework in Python to deliver fun facts from an API and display them in a simple desktop application.  

## **Project Description** ##  
This project aims to fetch random fun facts using an external API, store them in a PostgreSQL database, and display them through a graphical user interface (UI) built with CustomTkinter (CTk). The application allows users to filter facts by their status (seen or unseen) and automatically updates the status after displaying a fact.  

![Image not found (404)](src/images/ReadMe_picture.png)  

## **Installation** ##  
### To set up the project locally, follow these steps: ###  

#### **1. Download the Project** ####  
- Click the green **"Code"** button on the GitHub repository page and select **"Download ZIP"**.  
- Extract the ZIP file to a folder on your computer.  

#### **2. Install Python** ####  
- If you don't have Python installed, download and install it from [python.org](https://www.python.org/).  
- During installation, make sure to check the box **"Add Python to PATH"**.  

#### **3. Install Required Python Modules** ####  
- Open the project in an IDE like **PyCharm** or **VS Code**.  
- Install the required modules using the following steps:  
  1. Open the terminal in your IDE.  
  2. Copy and paste the following commands one by one and press **Enter**:  
     ```
     pip install psycopg2  
     pip install requests  
     pip install customtkinter  
     pip install fastapi  
     pip install uvicorn  
     pip install pyautogui  
     ```  
  - Alternatively, you can install the modules using the IDE's package manager (e.g., in PyCharm: **File > Settings > Project > Python Interpreter > +**).  

#### **4. Set Up PostgreSQL** ####  
- Download and install PostgreSQL from [postgresql.org](https://www.postgresql.org/).  
- During installation, remember the **username** and **password** you set for the PostgreSQL database.  

## **Setup and Usage Instructions** ##  
Please follow the steps below to set up and run the project correctly:  

#### **1. Create the Database** ####  
- Open and execute the file `1.create_fun_facts_db_by_martha.py`.  
- A password prompt will appear. Enter your **PostgreSQL password**.  
- This script will create the `funfact_db` database and the `facts` table.  

#### **2. Export API Data to CSV** ####  
- Open and execute the file `2.API_csv_export_by_birol.py`.  
- This script will fetch 350 random fun facts from the API and save them in the `src/fakten.csv` file.  

#### **3. Load CSV Data into PostgreSQL** ####  
- Open and execute the file `3.load_csv_to_postgres_by_dorian.py`.  
- A password prompt will appear. Enter your **PostgreSQL password**.  
- This script will load the fun facts from the CSV file into the `facts` table.  

#### **4. Run the Fun Fact API** ####  
- Open and execute the file `4.Funfacts_API_by_daria.py`.  
- A password prompt will appear. Enter your **PostgreSQL password**.  
- This will start the FastAPI server on `http://localhost:8000`.  

#### **5. Launch the Application** ####  
- Open and execute the file `5.app_by_katharina.py`.  
- The user interface will open on your desktop.  

#### **6. Get a Random Fun Fact** ####  
- To pick a random fun fact, simply click the **Start** button.  
- Use the radio buttons to filter facts by their status (seen or unseen).  

## **License** ##  
This project is licensed under the MIT License - see the LICENSE file for details.  

## **Contact** ##  
For any questions, you can reach out to the developers:  
- Kateryna: kateryna@example.com  
- Daria: daria@example.com  
- Martha: martha@example.com  
- Birol: birol@example.com  
- Dorian: dorian@example.com  