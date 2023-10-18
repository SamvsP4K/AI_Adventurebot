from re import template
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
from langchain.memory import CassandraChatMessageHistory, ConversationBufferMemory
from langchain.llms import OpenAI
from langchain import LLMChain, PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.cassandra import Cassandra
from config import API_KEY, KEYSPACE
from template import ruleset

#cloud configuration files to connect to astra vector database
cloud_config={
    "secure_connect_bundle":"secure-connect-ai-db.zip"
}

#loads json file required to database configuration
with open("ai_db-token.json") as ai_db:
    secrets = json.load(ai_db)


CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]
ASTRA_DB_KEYSPACE = KEYSPACE
OPENAI_API_KEY = API_KEY

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config,auth_provider=auth_provider)
session = cluster.connect()

#this section initializes DB memory
message_history = CassandraChatMessageHistory(
    session_id="anything",
    session=session,
    keyspace=ASTRA_DB_KEYSPACE,
    ttl_seconds=3600
)

message_history.clear()

cass_buff_memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=message_history
)

#this ruleset is a string that contains all the rules and parameters of the game
template=ruleset

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"],
    template=template
)

#This section uses langchain to interact with the OpenAI API
llm = OpenAI(openai_api_key=OPENAI_API_KEY)
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=cass_buff_memory
)

#this while loop runs the game until "The End" is detected in final response

choice = "start"

while True:
    response = llm_chain.predict(human_input=choice)
    print(response.strip())

    if "The End." in response:
        break

    choice = input("Your Reply: ")

