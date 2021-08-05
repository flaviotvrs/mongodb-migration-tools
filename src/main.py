import argparse
from migration_manager import migrate

parser = argparse.ArgumentParser(description='Copy a MongoDB from one cluster to another')

parser.add_argument("--origin", dest = "origin", required = True, help = "Connection string of the original cluster containing credentials and database")
parser.add_argument("--destination", dest = "destination", required = True, help = "Connection string of the destination cluster containing credentials and database.")
parser.add_argument("--collection", dest = "collection", required = False, help = "Specifies a collection to backup. If you do not specify a collection, this option copies all collections in the specified database or instance to the dump files.")
parser.add_argument("--compare-documents", dest = "compare_documents", action = "store_true", required = False, help = "If specified there will be a document count comparison at the end of the migration.")
parser.add_argument("--handle-balancer", dest = "handle_balancer", action = "store_true", required = False, help = "If specified origin cluster balancer will be stopped before migration and re started after migration.")
parser.add_argument("--override-database", dest = "override", action = "store_true", required = False, help = "If specified the migration will occur on top of an existing database on destination.")

args = parser.parse_args()

migrate(args.origin, args.destination, args.collection, args.handle_balancer, args.compare_documents, args.override)