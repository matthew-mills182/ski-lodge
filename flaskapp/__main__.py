# Copyright © 2023-2025, Indiana University
# BSD 3-Clause License

from flaskapp.app import app
from os.path import abspath


# Flask's default port is 5000, but this can conflict with macOS users since
# AirPlay also uses 5000. Students frequently try to run their lecture and
# project repos at the same time, so we've opted into using two different
# numbers, e.g. if running from `/path/to/lecture` or somewhere else.
port_number = 5001 if "lecture" in abspath(__file__) else 5002


app.run(debug=True, port=port_number)
