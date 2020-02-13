from app.data_base.DB import DB
from app.data_base import bilibilier

bilibilier.write(2)

x = bilibilier.read(2)
print(x)

