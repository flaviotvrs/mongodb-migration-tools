import subprocess
import util
from urllib.parse import urlparse
import json

class Migration:

    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

    def dump_restore(self, override):
        return self.dump_restore_collection(override, None)

    def dump_restore_collection(self, override, collection):

        if self.destination.exists() and not override:
            raise Exception("Destination database already exists!")
        
        cmd_dump = ["mongodump", "--uri", self.origin.connection_string, "--numParallelCollections", "16", "--archive"]

        cmd_restore = ["mongorestore", "--uri", self.destination.connection_string, "--archive", "--numParallelCollections", "16", "--numInsertionWorkersPerCollection", "8"]
        
        if collection:
            cmd_dump.append(f"--collection={collection}")
            cmd_restore.append("2> /dev/null") # not working
        
        dump = subprocess.Popen(cmd_dump, stdout = subprocess.PIPE, universal_newlines = True)
        restore = subprocess.Popen(cmd_restore, stdin = dump.stdout, stdout = subprocess.PIPE, universal_newlines = True)
        
        dump.stdout.close()

        return_code = None
        while True:
            output = restore.stdout.readline()
            print(output.strip())
            return_code = restore.poll()
            if return_code is not None:
                for output in restore.stdout.readlines():
                    print(output.strip())
                break
        return return_code


class MongoDb:

    def __init__(self, connection_string):
        parsed_url = urlparse(connection_string)
        self.connection_string = connection_string
        self.database = parsed_url.path.replace("/","")

    def get_balancer_state(self):
        stdout = self.run_command("sh.getBalancerState()")
        return util.str2bool(stdout)
    
    def stop_balancer(self):
        result = None
        if self.get_balancer_state():
            stdout = self.run_command("sh.stopBalancer()")
            result = True
        else:
            result = False
        return result

    def start_balancer(self):
        result = None
        if not self.get_balancer_state():
            stdout = self.run_command("sh.startBalancer()")
            result = True
        else:
            result = False
        return result

    def exists(self):
        find_base = "db.adminCommand( { listDatabases: 1, nameOnly: true, filter: { \"name\": /^<database>$/ } } )"
        find_command = find_base.replace("<database>", self.database)
        stdout = self.run_command(find_command)
        return (self.database in stdout)

    def count_documents(self, collection):
        count_base = "var database = '<database>'; var collection = '<collection>'; var dict = {}; db.getMongo().getDB(database).getCollectionNames().forEach(function (col) { if (collection == '' || collection == col){ dict[col] = db.getMongo().getDB(database).getCollection(col).countDocuments({}); }}); print(JSON.stringify(dict));"
        count_command = count_base.replace("<database>", self.database).replace("<collection>", collection)
        stdout = self.run_command(count_command)
        return json.loads(stdout)

    def run_command(self, command):
        cmd = ["mongosh", self.connection_string, "--quiet", "--eval", command]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        if stderr:
            raise Exception(stderr)
        return stdout
