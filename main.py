from api import app
from mangum import Mangum

handler = Mangum(app)