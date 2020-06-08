import io
import pandas as pd
import pdb; pdb.set_trace()

def iowrite():
    df = pd.DataFrame({"foo_id": [1, 2, 3, 4, 5]})
    stream = io.StringIO()
    df.to_csv(stream, sep=",")

    print(stream.getvalue())

if __name__ == "__main__":
    iowrite()
