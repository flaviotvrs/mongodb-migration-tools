import mongo
from util import (print_info, print_success, print_fail, print_warning)

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
    else:
        print_fail("migration finished with errors")

    if compare_documents:
        print_info("origin document count")
        print(origin.count_documents())
        print_info("destination document count")
        print(destination.count_documents())