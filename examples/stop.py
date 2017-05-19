import sys
sys.path.append("..")

from allegro import Allegro

app = Allegro("test_project")
app.initialize("test.ini")
app.stop()




