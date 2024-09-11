FROM python:3.7

# Expose port you want your app on

WORKDIR /app
# Upgrade pip and install requirements
COPY . .

RUN pip install -U pip && pip install -r requirements.txt

EXPOSE 8080

# Run
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
