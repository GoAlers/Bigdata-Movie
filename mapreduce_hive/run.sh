
HADOOP_CMD="/usr/local/src/hadoop2.6.5/bin/hadoop"
STREAM_JAR_PATH="/usr/local/src/hadoop2.6.5/contrib/streaming/hadoop-streaming-2.6.5.jar"

INPUT_FILE_PATH_1="/The_Man_of_Property.txt"
OUTPUT_PATH="/output"

$HADOOP_CMD fs -rmr -skipTrash $OUTPUT_PATH

# Step 1.
$HADOOP_CMD jar $STREAM_JAR_PATH \
    -input $INPUT_FILE_PATH_1 \
    -output $OUTPUT_PATH \
    -mapper "python map_new.py" \
    -reducer "python red_new.py" \
    -file ./map_new.py \
    -file ./red_new.py
