# CanvasInsights
Cross Collaboration Between Data Science and Computer Science

## **Proposed Data Stack**
- **Data Source**: Canvas API
- **Transactional Database**: Sqlite3
- **Analytical Database**: DuckDB
- **ETL**: Pandas & Polars
- **Model Training, Testing, and Validation**: SciKit-Learn

## How to Get API Access Token
1. Login to Canvas
2. Click your Profile Picture to View the following Sidebar Menu:
 
- ![image](https://github.com/uvucs/canvas-insights/assets/86315514/cc4a64e0-48ca-4f97-a118-d032967c5c77)

3. Click "Settings" on the Sidebar Menu:

- ![image](https://github.com/uvucs/canvas-insights/assets/86315514/3b3d7051-90ff-455f-b074-ac3393f62666)

4. In Settings, Scroll down to where is says "Approved Integrations" and select "New Access Token":

- ![image](https://github.com/uvucs/canvas-insights/assets/86315514/a533d6c0-e3f5-4191-be8c-6b2052a3271a)

5. Copy and paste that Token in a file called `API_KEY.txt` in the same folder as the repo.
**NOTE**: It will not work if you do not name the file `API_KEY.txt` and place it in the same folder as the repo. The file should only contain the token and nothing else.
`API_KEY.txt` is in the `.gitignore` file so it will not be pushed to the repo.

**IF YOU FORGET YOUR TOKEN, YOU WILL NEED TO GET A NEW ONE FOLLOWING THE STEPS ABOVE.**

