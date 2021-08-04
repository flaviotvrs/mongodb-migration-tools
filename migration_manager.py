import mongo
from util import (print_info, print_success, print_fail, print_warning)
import json
import jsondiff

def migrate(origin_connection_string, destination_connection_string, collection, handle_balancer, compare_documents, override):

    origin = mongo.MongoDb(origin_connection_string)
    destination = mongo.MongoDb(destination_connection_string)

    print_info("starting migration")
    
    balancer_state = None

    if handle_balancer:
        balancer_state = origin.get_balancer_state()
        
        if balancer_state:
            print_info("origin stop balancer " + str(origin.stop_balancer()))
        else:
            print_warning("balancer is already not started")
    
    print_info("dump and restore")
    migration = mongo.Migration(origin, destination)
    
    migration_result = None

    try:
        if collection:
            migration_result = migration.dump_restore_collection(override, collection)
        else:
            migration_result = migration.dump_restore(override)
    finally:
        if handle_balancer and balancer_state:
            print_info("origin start balancer " + str(origin.start_balancer()))

    if migration_result == 0:

        print_success("migration finished successfuly")

        if compare_documents:
            print_info("document count compare")
            origin_count = origin.count_documents(collection if collection else "")
            dest_count = destination.count_documents(collection if collection else "")

            diff = jsondiff.diff(origin_count, dest_count)

            if diff :
                print("Different")
                print_fail("document count between clusters is different")
                print(diff)
                migration_result = 1
            else :
                print_success("document count match")
                print(json.dumps(dest_count))

    else:
        print_fail("migration finished with errors")

    if migration_result and migration_result > 0:
        exit(1)
