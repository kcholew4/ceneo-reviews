# ceneo-reviews

Display, filter and display statistics about products found on Ceneo.pl

> Deployed version does not work correctly because of Ceneo.pl anti-bot protection. Apparently DigitalOcean's ip addresses are blacklisted.

### How to run

`app/` and `server/` are seperate modules and can be deployed separately.

#### 1. Download the repo
```
git clone https://github.com/kcholew4/ceneo-reviews/
cd ceneo-reviews
```

#### 2. Run server module
```
cd server
pip install -r requirements.txt
#Set MONGO_DB_CONNECTION_STRING env variable to mongo db connection string (you can put this inside .env file)
#Set PORT env variable
python app.py
```

#### 3. Run app module

```
cd ../app
npm install
#Set PUBLIC_API_URL env variable to the api url (can be put inside .env file)
npm run dev
```
