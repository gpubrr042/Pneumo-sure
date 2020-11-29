from app import app
ALLOWED_EXTENSIONS = ['jpeg']
gunicorn --bind=0.0.0.0 --timeout 600 app:myapp
if __name__ == '__main__':
    app.run()
    
  
