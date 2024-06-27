# Job Recommendation System API

The Recommendation System API.

## Create Python Virtual Environment

```bash
# Create virtual env
python -m venv .venv

# Activate virtual env
source .venv/Scripts/activate
```

## Install Packages

```bash
pip install -r requirements.txt
```

## Run Project

```bash
python app.py
```

## Connect

- On Local Machine:
  - http://localhost:4000/api/get_recommendations

## Test

- Method:
  - `[POST]`
- Request Body:
  - ```json
    {
      "profile": "Engineer",
      "location": "San Francisco, CA",
      "count": 5
    }
    ```
- Response Body:
  - ```json
    {
      "data": {
        "profiles": [
          "Machine Learning Engineer implementing ML algorithms for data analysis",
          "Data Engineer building and maintaining data pipelines",
          "Civil Engineer designing and overseeing construction projects",
          "Frontend Engineer skilled in JavaScript"
        ],
        "locations": [
          "Project Manager with excellent communication and leadership skills",
          "AI Researcher focused on deep learning and natural language processing",
          "UX/UI Designer creating user-friendly and visually appealing interfaces",
          "Sales Manager experienced in B2B relationships and market analysis",
          "Business Analyst identifying business needs and process improvements"
        ]
      }
    }
    ```
