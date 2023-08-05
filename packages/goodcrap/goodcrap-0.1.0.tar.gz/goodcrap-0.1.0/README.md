# goodcrap
 
This software enables data engineers to replicate the database schemas at their organisations, and then generate fake data that resemble a random sample of the actual data in their organisation.

Using JSON/yaml configuration file, you define the players of your systems, the nodes they will be using and the frequency of usage.

Generating random data is increasingly a requirement for data teams. [It is a better alternative to using public datasets that require cleaning]{https://motherduck.com/blog/python-faker-duckdb-exploration/}.

Features of data emulator:

1- Choose whether fake data is dynamic or static. For dynamic data, a data stream is established that schedules the generation of data from the cloud, or from a PC.
2- Seamlessly host the data at the platform of choice.
3- Insert the data into the storage platform of choice.
4- Control the randomness of the data: data can be made to fit a specific distribution.
5- The data can be generated based on a data sample: the user provides values for a column, and the random generator is trained on the values to generate infinite data values.
6- The user can control the cleanliness of the data: you can add `HTML tags` to text data where tags such as <b></b> enclose randomly chosen parts of the text, or you can add `null` values, and outliers.
7- Service is accessible via a python library or a web API. *The web API lets you generate new data sources in mage_io*. The software lets the user run a local server that generates data, and can be accessed as a data sources.
8- Choose from template schemas. The entire schema along with data are generated.
9- Generate data also for games: chess moves, Go moves, connect4 moves.
10- Generate image data! Different svg images are assembled together.

