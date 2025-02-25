Finance-Buddy
A valuable tool to help users manage their finances more effectively. Track expenses, monitor income, and gain insights into your financial health with Smart Personal Finance Advisor.
🔗 Live Demo: https://smartfinance-279g.onrender.com/

⚠️ IMPORTANT: After login or signup, please navigate to https://smartfinance-279g.onrender.com/income_add/ and add your income first. The dashboard will only be visible after you've added income.

Features

📊 Visualize expense distribution with interactive charts
💰 Track daily income and expenses
📈 Monitor your financial balance
📱 Responsive design for all devices
📧 Email notifications when expenses exceed income
🔐 Secure user authentication

Setup Instructions
Follow these steps to set up and run the Finance-Buddy Django application:
1. Clone the Repository
bashCopygit clone https://github.com/yourusername/finance-buddy.git
cd finance-buddy
2. Create a Virtual Environment
First, ensure you have Python 3.11 installed. Then, create and activate a virtual environment:
bashCopypython -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install Dependencies
Install the required packages using pip:
bashCopypip install -r requirements.txt
4. Set Up Environment Variables
Create a .env file in the root of your project directory and fill it with the following template:
CopySECRET_KEY=your_django_secret_key
SENDGRID_API_KEY=your_sendgrid_api_key
5. Run Migrations
Apply database migrations:
bashCopypython manage.py makemigrations
python manage.py migrate
6. Start the Application
Run the Django development server:
bashCopypython manage.py runserver
Your Django application will be available at http://127.0.0.1:8000/.
Technologies Used

Backend: Django
Database: PostgreSQL
Frontend: HTML, CSS, JavaScript, Chart.js
Email: SendGrid

Deployment
The application is deployed on Render. For deployment on your own Render instance:

Create a new Web Service on Render
Connect your GitHub repository
Configure environment variables (SECRET_KEY and SENDGRID_API_KEY)
Set the build command: pip install -r requirements.txt && python manage.py collectstatic --noinput
Set the start command: gunicorn smartfinance.wsgi:application

WEBSITE LOOK 

![image](https://github.com/user-attachments/assets/faf9d6dd-5dbb-4896-ab3d-7eee5b52be63)

![image](https://github.com/user-attachments/assets/f52958a7-687a-4c71-86f7-0c4ab219081e)


![image](https://github.com/user-attachments/assets/77c16d5d-70c9-4c93-8842-e0c4ce9a6e1d)
![image](https://github.com/user-attachments/assets/965226fb-5ffc-415e-8fa3-9e679f3ca123)

![image](https://github.com/user-attachments/assets/4b94cd27-bfb9-4b75-8300-403de09f715a)

![image](https://github.com/user-attachments/assets/0e19d1cd-b346-4819-b4af-40320a6ec9d3)

![image](https://github.com/user-attachments/assets/8df11f65-a3fc-4e5b-a549-4633a699ca8d)





License
MIT License
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
