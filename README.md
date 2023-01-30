# DeFi Yield Demo

## Task
Here is our Rect Database: https://defiyield.app/rekt-database
Task: 
- prepare the visualization of risk vectors and how it evolves over time?
- share a jupyter notebook (or equivalent) in case of this task.

We expected just a few visualizations to highlight what are the most important insights from our database. 

The doc about the API: https://docs.defiyield.app/api/api
The API key: 

The test query:
```
query {
  rekts(
    pageNumber:1
    pageSize:10
    searchText: “terra”
    orderBy: {
      fundsLost: desc
    }
  ) {
    id
    projectName
    description
  }
}
```

## How to run
- Create .env file from .env.example file
- add API key to .env file
- execute main.py

## Results
Results (graphs in pdf format) are stored in ./graphs folder.
