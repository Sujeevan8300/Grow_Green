# Software Overview: E-Commerce App with Integrated Crop Recommendation System  

## Overview  
This project is a **full-stack web application** that combines an **e-commerce platform** with an **AI-powered crop recommendation system**. Built using Flask, the app allows farmers or agricultural buyers to browse products while also receiving personalized crop suggestions based on environmental factors like soil type, climate, and rainfall.  

## Key Features  
✅ **E-Commerce Platform**  
- Product listings with categories  
- User authentication (login/signup)  
- Shopping cart functionality  
- Order management  

✅ **Crop Recommendation System**  
- Machine Learning model (Random Forest) trained on agricultural datasets  
- Input fields for soil parameters (N, P, K levels, pH, rainfall, temperature)  
- Real-time crop suggestions with confidence scores  

✅ **Admin Panel**  
- **Admin Login**:  
  - Email: `admin@gmail.com`  
  - Password: `123456`  
- **Product Management**: Add, edit, delete, and categorize products.  
- **User Management**: View, block/unblock, or delete users.  
- **Category Management**: Create, update, or remove product categories.
- **Order Management**: Create, update, or remove Customer Orders.  

✅ **Technical Stack**  
- **Frontend**: HTML, CSS, JavaScript, Bootstrap (responsive design)  
- **Backend**: Python (Flask)  
- **Database**: SQLite  
- **Machine Learning**: Scikit-learn (Random Forest), Jupyter Notebook for model training  

## How It Works  
1. **Admin Access**:  
   - Log in to the admin panel using the credentials above.  
   - Manage products, users, and categories via the dashboard.  
2. **User Input**: Farmers enter soil and climate data.  
3. **AI Prediction**: The trained model processes input and recommends suitable crops.  
4. **E-Commerce Integration**: Users can explore/purchase farming products related to recommended crops.  

## Setup & Installation  
1. Clone the repository:  
   ```bash  
   git clone [GitHub_Repo_URL]  
   ```  
2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  
3. Run the Flask app:  
   ```bash  
   python app.py  
   ```  

## Screenshots  
- *Include images of the UI, admin panel, recommendation results, and product pages.*  

## Future Enhancements  
- Expand product catalog  
- Add payment gateway integration  
- Improve ML model with larger datasets
- Add AI ChatBot

## GitHub Repository  
🔗 [GitHub Link](https://github.com/Sujeevan8300/Grow_Green) *(https://github.com/Sujeevan8300/Grow_Green)*  

