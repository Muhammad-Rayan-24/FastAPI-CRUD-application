#This code is quite self explanatory but comments are given in essential places to show why something was used and where

#This is currently not connected to any database and will be using the browser memory to save the user data


from fastapi import FastAPI, HTTPException        #using httpexception to automatically return an appropriate HTTP response with a status code and detail message.
from pydantic import BaseModel, Field                 #firld is used to set validation of default value
from typing import Dict, List
from uuid import uuid4                            #to create a uique id (Universal Unique id)

app = FastAPI()

class SubTopic(BaseModel):
    name: str
    id: str = Field(default_factory=lambda: str(uuid4()))            #setting a default uuid and using field ot default it and validate it 

class Topic(BaseModel):
    name: str
    bot_id: str
    sub_topics: Dict[str, SubTopic] = Field(default_factory=dict)       #the default_factory initializes the dictionary as empty by default

# In-memory storage for topics
topics_store: Dict[str, Topic] = {}     #this creates a dictionary to store the topics in which we also have another dictionary to store subtopics

#the following code snippet is to generate the initial dataset which will be shown in the first get function when you run the api

def generate_initial_dataset():
    # Create subtopics
    subtopic1 = SubTopic(name="Subtopic1", id=str(uuid4()))
    subtopic2 = SubTopic(name="Subtopic2", id=str(uuid4()))
    subtopic3 = SubTopic(name="Subtopic3", id=str(uuid4()))

    # Create topics
    topic1 = Topic(name="Topic1", bot_id="bot_1", sub_topics={subtopic1.id: subtopic1})
    topic2 = Topic(name="Topic2", bot_id="bot_2", sub_topics={subtopic2.id: subtopic2, subtopic3.id: subtopic3})

    # Store topics in the dictionary
    topics_store[topic1.name] = topic1
    topics_store[topic2.name] = topic2

    print("Initial dataset generated and stored in topics_store")

generate_initial_dataset()

""" below is to validate in terminal regarding the initial dataset generated you will also be able to view this data in the first get function in the api""" 

# print(topics_store)           



#the following is for creating user data
@app.post("/topics/", description="Here, additional prop has been added to allow you to add up to 3 subtopics.")
async def create_topic(topic: Topic):
    if topic.name in topics_store:
        raise HTTPException(status_code=400, detail="Topic with this name already exists")
    
    topics_store[topic.name] = topic
    return topic


#the follwoing is to show the initial generated dataset
@app.get("/topics/" )
async def get_topic_names():
    return {"topic_names": list(topics_store.keys())}


#the following is for the read functionality 
@app.get("/topics/{name}" , description="Retrieve a topic by its name.")
async def get_topic(name: str):
    if name not in topics_store:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    return topics_store[name]


#the following is for updation section
@app.put("/topics/{name}", description="You are at the initial stage for the path you have provided. If you leave an area as is, then it will be simply saved as 'string' in the data.")
async def update_topic(name: str, updated_topic: Topic):
    if name not in topics_store:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Check if the name is being updated
    if name != updated_topic.name:
        # Remove the old entry
        topics_store.pop(name)
    
    # Save the updated topic
    topics_store[updated_topic.name] = updated_topic
    return updated_topic



#the following is for the delete section
@app.delete("/topics/{name}", description="you can remove a topic by entering its name in this section")
async def delete_topic(name: str):
    if name not in topics_store:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    deleted_topic = topics_store.pop(name)
    return deleted_topic
