if [ ! -d 'data_train_omit' ]; then
    mkdir data_train_omit
fi

for test_file in ./data_test/*; do
    file_name="$(basename ${test_file%.*})"
    mv "data_train/$file_name.xml" data_train_omit

    if ! ./run.sh $file_name; then
        echo "Failed to process file $test_file"
        exit 2
    fi

    mv "data_train_omit/$file_name.xml" data_train
done