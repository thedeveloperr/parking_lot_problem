### Req.
1. python 3+
2. git
3. black , for linting

### Setup
#### Note: if you have python3 virtual env setup or your `python` command is matched to python 3 Instead of using `python3` in below commands use `python`
1. Clone the repo. `git clone git@github.com:thedeveloperr/parking_lot_problem.git`
2. cd into the repo using: `cd parking_lot_problem`.
3. Run the program using `python3 main.py ./tests/data/test1.txt` . You can give your own file path too by replacing last command line arg.
4. To run tests run this command: `python3 -m unittest discover` .
5. Linting is done using black. See https://github.com/psf/black .

### Folder and files brief:
1. `tests/`: Contains mix of unit tests and integration tests
  1. `tests/data` contains test files input
2. `errors.py` Contains error objects for app.
3. `models.py` Contains data models
4. `data_access_objects/` a DAO pattern hides implementation details of the the data store and if later we want to change the datastore we just need to make changes to implementations of the existing class methods interface. without touching code in services folder. Right now an in memory datastore is implemented.
5. `services/` takes request and call appropriate DAO methods or other services to produce output which will be used to produce final response view.
6. `command_processor.py` process text command and call relevant services.
7. `input_consumer/` for storing code of user input consumer. different type of input like http req, cli or file based input can be there. This layer ensures mode of input is decoupled from rest of logic. As of now it have file based input reading capability.
8. `main.py` The first file that is executed from cli to start and run the whole program.
