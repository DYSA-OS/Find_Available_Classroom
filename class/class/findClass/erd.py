import pandas as pd
from matplotlib import pyplot as plt
import pydotplus
from IPython.display import Image
from graphviz import Source

# Define the models in a DataFrame
data = {
    'Table': ['Building', 'Room', 'Lecture', 'LectureSchedule'],
    'Columns': [
        'id (PK), name, latitude, longitude',
        'id (PK), building_id (FK), room_number',
        'id (PK), subject, professor, lecture_type, room_id (FK)',
        'id (PK), lecture_id (FK), day, start_time, end_time'
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a Graphviz ERD diagram
erd = """
digraph G {
    node [shape=record, fontsize=12, fontname="Arial"];

    Building [label="{ Building | id (PK) | name | latitude | longitude }"];
    Room [label="{ Room | id (PK) | building_id (FK) | room_number }"];
    Lecture [label="{ Lecture | id (PK) | subject | professor | lecture_type | room_id (FK) }"];
    LectureSchedule [label="{ LectureSchedule | id (PK) | lecture_id (FK) | day | start_time | end_time }"];

    Building -> Room [label="1:N"];
    Room -> Lecture [label="1:N"];
    Lecture -> LectureSchedule [label="1:N"];
}
"""

# Generate the ERD diagram
graph = Source(erd)
graph.render("erd_diagram", format='png', cleanup=False)
graph_path = "erd_diagram.png"

graph_path
