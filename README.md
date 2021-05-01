# rest2stream-backend
Backend of Rest API 2 Stream data (RATS) 🐀 

## Streaming Content Screenshot
### The content of the example Api streaming
![image](https://user-images.githubusercontent.com/3206118/115251792-744a7800-a15d-11eb-823c-5dc1f738e317.png)


## Installation (FastAPI Backend)
```
pip install -r requirements
```

## How to run development server? (FastAPI Backend)
```
cd /home/{username}/rest2stream-backend/
#uvicorn watchdog always detect changes in SQLlite decided to specify the dir 
uvicorn main:app --reload --reload-dir routers
```
