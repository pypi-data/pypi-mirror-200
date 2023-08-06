tfrecords
## simplify and transplant the tfrecord and table

### update information
```text
    2022-10-30:  Add lmdb leveldb read and writer and add record batch write
    2022-10-17:  Add shared memory for record to read mode with more accelerated Reading.
    2022-02-01:  simplify and transplant the tfrecord dataset
```

### 1. record read and write demo , with_share_memory flags will Accelerated Reading

```python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/8 15:49

import tfrecords
options = tfrecords.TFRecordOptions(compression_type=tfrecords.TFRecordCompressionType.NONE)
def test_write(filename, N=3, context='aaa'):
    with tfrecords.TFRecordWriter(filename, options=options) as file_writer:
        batch_data = []
        for i in range(N):
            d = context + '____' + str(i)
            batch_data.append(d)
            if (i + 1) % 100 == 0:
                file_writer.write_batch(batch_data)
                batch_data.clear()
        if len(batch_data):
            file_writer.write_batch(batch_data)
            batch_data.clear()

def test_record_iterator(example_paths):
    print('test_record_iterator')
    for example_path in example_paths:
        iterator = tfrecords.tf_record_iterator(example_path, options=options,skip_bytes=0,with_share_memory=True)
        offset_list = iterator.read_offsets(0)
        count = iterator.read_count(0)
        print(count)
        num = 0
        for iter in iterator:
            num += 1
            print(iter)

def test_random_reader(example_paths):
    print('test_random_reader')
    for example_path in example_paths:
        file_reader = tfrecords.tf_record_random_reader(example_path, options=options,with_share_memory=True)
        last_pos = 0
        while True:
            try:
                x,pos = file_reader.read(last_pos)
                print(x,pos)
                last_pos = pos

            except Exception as e:
                break

def test_random_reader2(example_paths):
    print('test_random_reader2')
    for example_path in example_paths:
        file_reader = tfrecords.tf_record_random_reader(example_path, options=options,with_share_memory=True)
        skip_bytes = 0
        offset_list = file_reader.read_offsets(skip_bytes)
        for offset,length in offset_list:
            x, _ = file_reader.read(offset)
            print(x)

test_write('d:/example.tfrecords0',3,'file0')

example_paths = tfrecords.glob('d:/example.tfrecords*')
print(example_paths)
test_record_iterator(example_paths)
print()
test_random_reader(example_paths)
print()
test_random_reader2(example_paths)
print()
```

### 2. leveldb read and write demo 
```python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/8 15:49

from tfrecords import LEVELDB
db_path = 'd:/example_leveldb'
def test_write(db_path):
    options = LEVELDB.LeveldbOptions(create_if_missing=True, error_if_exists=False)
    file_writer = LEVELDB.Leveldb(db_path,options)

    keys,values = [],[]
    for i in range(30):
        keys.append(b"input_" + str(i).encode())
        keys.append(b"label_" + str(i).encode())
        values.append(b"xiaoming" + str(i).encode())
        values.append(b"zzs" + str(i).encode())
        if (i + 1) % 1000 == 0:
            file_writer.put_batch(keys,values)
            keys.clear()
            values.clear()
    if len(keys):
        file_writer.put_batch(keys, values)
        keys.clear()
        values.clear()

    file_writer.close()
def test_read(db_path):
    options = LEVELDB.LeveldbOptions(create_if_missing=False, error_if_exists=False)
    reader = LEVELDB.Leveldb(db_path,options)

    def show():
        it = reader.get_iterater(reverse=False)
        i = 0
        for item in it:
            print(i,item)
            i += 1

    def test_find(key):
        value = reader.get(key)
        print('find', type(value), value)

    show()

    test_find(b'input_0')
    test_find(b'input_5')
    test_find(b'input_10')

    reader.close()

test_write(db_path)
test_read(db_path)
```


### 3. lmdb read and write demo 
```python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/8 15:49

from tfrecords import LMDB
db_path = 'd:/example_lmdb'
def test_write(db_path):
    options = LMDB.LmdbOptions(env_open_flag = 0,
                env_open_mode = 0o664, # 8进制表示
                txn_flag = 0,
                dbi_flag = 0,
                put_flag = 0)
    file_writer = LMDB.Lmdb(db_path,options,map_size=1024 * 1024 * 10)
    keys, values = [], []
    for i in range(30):
        keys.append(b"input_" + str(i).encode())
        keys.append(b"label_" + str(i).encode())
        values.append(b"xiaoming_" + str(i).encode())
        values.append(b"zzs_" + str(i).encode())
        if (i + 1) % 1000 == 0:
            file_writer.put_batch(keys, values)
            keys.clear()
            values.clear()
    if len(keys):
        file_writer.put_batch(keys, values)
    file_writer.close()
def test_read(db_path):
    options = LMDB.LmdbOptions( env_open_flag = LMDB.LmdbFlag.MDB_RDONLY,
                env_open_mode = 0o664, # 8进制表示
                txn_flag = 0,
                dbi_flag = 0,
                put_flag = 0)
    reader = LMDB.Lmdb(db_path,options,map_size=0)

    def show():
        it = reader.get_iterater(reverse=False)
        i = 0
        for item in it:
            print(i,item)
            i += 1


    def test_find(key):
        value = reader.get(key)
        print('find', type(value), value)

    show()
    test_find('input0')
    test_find('input5')
    test_find(b'input10')
    reader.close()

test_write(db_path)
test_read(db_path)

```