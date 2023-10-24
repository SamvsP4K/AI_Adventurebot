# AI Adventure Bot

The main code for this project is in the ***main.py*** file in this repository.

### Project Purpose:

The project creates Choose Your Own Adventure or Dice Roller RPG game buddy. The AI will generate a storyline for you and keep track of your characters attributes and progress. Each story is dynamic and different and the AI serves as a game master.

### Database Requirements:

This project uses a vector-enabled database from Datastax. Vector databses are great for AI projects because they store data in a way that enables efficient retrieval of similar items. This is excellent for this RAG or Retrieval-augmented generation framework. The RAG framework allows for a model to reference it's trained data in combination with more accurate user input data. 
This allows for more reliable and up to date data retrieval. This is relevant for this project because the AI model will use a string of rules to reference while it interacts with the user who is inputting relevant information about their character. The AI combines both of it's knowledge bases to come up with a scenario. 

For more information on Vector databases and the RAG framework:

* [RAG](https://research.ibm.com/blog/retrieval-augmented-generation-RAG)
* [Vector Databases](https://www.pinecone.io/learn/vector-database/)

### Procedure

#### Configure Vector Database and Langchain
As mentioned above, after signing up for Datastax a vector database was very easy to get up and running. Once in the Astra console after sign up, there is a "quick start" section that has a step by step guide on how to spin up a database. It only takes about a minute get one up and running.

Taken from the Datastax website here is an example of what is required to configure your database and verify connection. You'll need a database token and a secure-connection bundle which is downloadable once your database is spun up in the Astra console. Make sure that your database token and secure connect bundle are in the same directory as your program code or has the correct path to where the files are. In the below example the area where you see "your db here" or "your json name" here may already be automatically filled out by datastax. Double check those sections.

![datastax_db_edit](https://github.com/SamvsP4K/ai_adveturebot/assets/110923091/5ce36dab-f395-4e09-b005-20fa078edc8e)

Create a virtual environment and install the required libraries. 
For this project you will need:
* langchain
* cassandra-driver
* json

You can a langchain quick start find [HERE](https://python.langchain.com/docs/get_started/quickstart).
You can find the documentation regarding CassandraChatMessageHistory [HERE](https://python.langchain.com/docs/integrations/memory/cassandra_chat_message_history).

Here we initialize the database memory.

![cassandra_driver](https://github.com/SamvsP4K/ai_adveturebot/assets/110923091/973194c8-bb41-45b1-9ae9-5b6353691adc)

In the code above we create an instance of the CassandraChatMessageHistory class. 
The session_id can be given any name you'd like. 
The session parameter keeps track of the current chat session you are in.
The keyspace parameter is the keyspace name you chose when you created your database. You can find that in your astra console when you click on your database.

***For this code, the keyspace name and Open AI key were kept in a separate config file and imported into the main codebase.***  

Below that we have an instance of the conversation buffer memory. You can find the documentation regarding this class [HERE](https://python.langchain.com/docs/modules/memory/types/buffer).

This will allow us store messages and extract them in a variable.
The first parameter memory_key identifies the buffer, while chat_memory passes the message_history instance we created earlier in the code. It will help the bufffer identify what object is storing the chat history. 
The ConversationBufferMemory provides a buffer that will cache messages in memory for performance, rather than always reading or writing from the database.

##### Open AI API KEY

You will also need an open AI API key. You can sign up and get one for free at OpenAI.com. 
As this is a text-based game, OpenAI limits the free usage of the API key based on how many tokens are used.

Tokens in Natural Language Processing are broken down units of text that large language models use to understand statistical relationships between words and make predictions. OpenAI has a limit on how many tokens are processed using their free API. For larger amounts of data you will need to pay.  For example of how tokens are counted here is a link to OpenAI's tokenizer. 

[OpenAI Tokenizer](https://platform.openai.com/tokenizer)

In the code below. you'll see a template variable with "ruleset" passed. For my code, ruleset was a long string in a seperate .py file. It was kept separate to keep the main code clean and less cluttered.

a ruleset example:

""" In this game you will guide the player in a fantasy adventure. You are to ask them to describe their character and proceed to take them on a choose your own adventure or dice rolling RPG journey. Ask them what they prefer at the start of the game.

AI: {chat_history}
Human Input: {human_input}''""

This is saved in a template variable and will be used as a prompt for the OpenAI LLM we are using.

![ruleset](https://github.com/SamvsP4K/ai_adveturebot/assets/110923091/55cd9589-9ff8-4c72-9790-476b783b1c75)


Below our template we connect to OpenAI and add our API key to an llm variable. 

We then create a PromptTemplate object saved in a prompt variable.
The input variables are used in your template as shown above. 
template is our ruleset.

You can find documentation on llm_chain [HERE](https://python.langchain.com/docs/modules/chains/foundational/llm_chain)

llm_chain will bring all our pieces together for the models functionality. 
Llm will take our OpenAI API key,
prompt will take the above prompt template, and
memory will take the cassandra buffer memory we also created above this.


#### Main Game Loop
Finally,
The main game loop is created. You'll see below we have a choice variable with the word "start". 
This will be used as the initial prompt to start the game.

![gameloop](https://github.com/SamvsP4K/ai_adveturebot/assets/110923091/f4c78af2-3625-4802-acbd-5187e00b6f19)

In a while loop we have a response variable with our prediction.
The print statement will print out the models response which will be the start of the game when first run. .strip() is included to take care of any leading or trailing spaces that may be generated.

The if statement following this will end the game if "The End." is detected in the models response. ***This was indicated in the template***.
The new choice variable will input the users reply into the prediction which will allow for back and forth conversation. 


### Future updates and notes:

I'd like to update this with an actual user interface. I'm currently researching what will be the best looking option for that. 

The AI works best with an optimized prompt. I'd suggest adopting a persona, giving very clear instructions, and limiting the scope for best results.
