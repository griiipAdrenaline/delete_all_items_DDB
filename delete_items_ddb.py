import boto3
import sys

ddb = boto3.resource('dynamodb')


def main(table_name):
    count_del = 0
    table = ddb.Table(table_name)
    key = table.key_schema[0]['AttributeName']  # Get primary key name
    key2 = table.key_schema[1]['AttributeName']
    scan = table.scan()
    data = scan['Items']
    while 'LastEvaluatedKey' in scan:
        scan = table.scan(ExclusiveStartKey=scan['LastEvaluatedKey'])
        data.extend(scan['Items'])

    with table.batch_writer() as batch:
        for each in data:  # Iterate over all the table rows by keys.
            # print each
            batch.delete_item(Key={key: each[key], key2: each[key2]})
            count_del += 1
            print("Delete items count: %d" % count_del)

    print "%s ITEMS HAS BEEN DELETED FROM DYNAMODB TABLE: %s" % (count_del, table_name)


if __name__ == '__main__':
    table_name_arg = str(sys.argv[1])
    print("Table to delete %s" % table_name_arg)
    main(table_name_arg)