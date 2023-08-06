# MetariumTopicListener for a substrate chain

# standard imports
import logging
import ipaddress
import math
import os
import shutil
import time
# third party imports
from blake3 import blake3
from substrateinterface import SubstrateInterface, Keypair
from tinydb import TinyDB, Query
# local imports
from .decorators import skip_if_syncing
from .exceptions import ChainConnectionRefusedError


logging.basicConfig(format='%(process)d : %(asctime)s : %(levelname)s\n%(funcName)s():%(lineno)i\n%(message)s\n',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class SubstrateListener(object):

    RECONNECTION_WAIT_DURATION_SECONDS = 5
    MAX_RECONNECTION_ATTEMPTS = 10

    def __init__(self,
                 key_path: str = None,
                 chain_spec_path: str = None,
                 chain_url: str = None,
                 data_location_path: str = "/home/.metarium",
                 writer_location_path: str = "/home/writer",
                 reader_location_path: str = "/home/reader",
                 block_threshold_404: int = 16,
                 outbox_read_duration_seconds: int = 3600,
                 ) -> None:
        key_path = key_path or None
        chain_spec_path = chain_spec_path or None
        chain_url = chain_url or None
        assert key_path is not None
        assert chain_spec_path is not None
        assert chain_url is not None
        # check if key_path exists
        if not os.path.exists(key_path):
            logging.error(f"key_path {key_path} does not exist!")
            raise FileNotFoundError
        # check if chain_spec_path exists
        if not os.path.exists(chain_spec_path):
            logging.error(f"chain_spec_path {chain_spec_path} does not exist!")
            raise FileNotFoundError
        # check if chain_url is valid
        if not isinstance(chain_url, str):
            logging.error(f"chain_url {chain_url} is not a string!")
            raise TypeError
        # check if data_location_path is valid
        if not isinstance(data_location_path, str):
            logging.error(
                f"data_location_path {data_location_path} is not a string!")
            raise TypeError
        if not os.path.exists(data_location_path):
            logging.error(
                f"data_location_path {data_location_path} does not exist!")
            raise FileNotFoundError
        # check if writer_location_path is valid
        if not isinstance(writer_location_path, str):
            logging.error(
                f"writer_location_path {writer_location_path} is not a string!")
            raise TypeError
        if not os.path.exists(writer_location_path):
            logging.error(
                f"writer_location_path {writer_location_path} does not exist!")
            raise FileNotFoundError
        # check if reader_location_path is valid
        if not isinstance(reader_location_path, str):
            logging.error(
                f"reader_location_path {reader_location_path} is not a string!")
            raise TypeError
        if not os.path.exists(reader_location_path):
            logging.error(
                f"reader_location_path {reader_location_path} does not exist!")
            raise FileNotFoundError
        # check if block_threshold_404 is valid
        if not isinstance(block_threshold_404, int):
            logging.error(
                f"block_threshold_404 {block_threshold_404} is not an integer!")
            raise TypeError
        if block_threshold_404 < 1:
            logging.error(
                f"block_threshold_404 {block_threshold_404} is less than 1!")
            raise ValueError
        # check if outbox_read_duration_seconds is valid
        if not isinstance(outbox_read_duration_seconds, int):
            logging.error(
                f"outbox_read_duration_seconds {outbox_read_duration_seconds} is not an integer!")
            raise TypeError
        if outbox_read_duration_seconds < 1:
            logging.error(
                f"outbox_read_duration_seconds {outbox_read_duration_seconds} is less than 1!")
            raise ValueError
        # get key from key_path file
        with open(key_path, "r") as key_file:
            # create keypair from key
            self.__key = Keypair.create_from_mnemonic(key_file.read())
        # create a blake3 hash of the chain_spec_path file
        self.__chain_spec_hash = self._file_hash(chain_spec_path)
        # set data_location_path
        self.__data_location_path = data_location_path
        # set writer_location_path
        self.__writer_location_path = writer_location_path
        # set reader_location_path
        self.__reader_location_path = reader_location_path
        self.__block_threshold_404 = block_threshold_404
        self.__outbox_read_duration_seconds = outbox_read_duration_seconds
        reconnection_attempts = 1
        while True:
            try:
                self.__chain = SubstrateInterface(url=chain_url)
            except ConnectionRefusedError:
                if reconnection_attempts == self.__class__.MAX_RECONNECTION_ATTEMPTS:
                    logging.error(
                        f"Chain connection terminated after {reconnection_attempts} attempts.")
                    logging.exception(ChainConnectionRefusedError)
                logging.warning(
                    f"Chain connection refused. Retrying in {self.__class__.RECONNECTION_WAIT_DURATION_SECONDS} seconds ...")
                reconnection_attempts += 1
                time.sleep(self.__class__.RECONNECTION_WAIT_DURATION_SECONDS)
                continue
            break
        logging.info(
            f"connected to {self.__chain.name} {self.__chain_spec_hash} as listener {self.__key.ss58_address}")
        self._is_syncing = False
        # setup folders
        self.__initialize_folders()
        # setup database
        self.__initialize_database()
        # sync all items
        self.__sync_all()
        # start listening for new blocks
        self.listen()

    ############################## INITIALIZATION LOGIC ##############################

    def __initialize_database(self):
        # check if the database path exists. if not, raise an error
        if not os.path.exists(self.__database_path):
            logging.error(
                f"database path {self.__database_path} does not exist!")
            raise FileNotFoundError
        # get the database from the database path. if it does not exist, create it
        self.__db = TinyDB(f"{self.__database_path}/yettagam.db", indent=4, separators=(
            ',', ': '), sort_keys=True)
        # get the metariums table. if it does not exist, create it
        self.__table_metariums = self.__db.table("metariums")
        # get the chain_spec_hash record. if it does not exist, create it with the chain name as the value
        self.__table_metariums.upsert(
            {"chain_spec_hash": self.__chain_spec_hash, "name": self.__chain.name}, Query().chain_spec_hash == self.__chain_spec_hash)
        # get the topics table. if it does not exist, create it
        self.__table_topics = self.__db.table("topics")
        # get the writers table. if it does not exist, create it
        self.__table_writers = self.__db.table("writers")
        # get the arikuris_state table. if it does not exist, create it
        self.__table_arikuris_state = self.__db.table("arikuris_state")
        # get the arikuris_404 table. if it does not exist, create it
        self.__table_arikuris_404 = self.__db.table("arikuris_404")

    def __initialize_folders(self):
        # create the data location directory if it does not exist
        if not os.path.exists(self.__data_location_path):
            os.makedirs(self.__data_location_path)
        ####### generic folders #######
        # create the database directory if it does not exist
        self.__database_path = os.path.join(
            self.__data_location_path, "data/db")
        self._create_folder_if_not_exists(self.__database_path)
        # create the outbox directory if it does not exist
        self.__outbox_path = os.path.join(
            self.__data_location_path, "outbox")
        self._create_folder_if_not_exists(self.__outbox_path)
        ####### chain-specific folders #######
        # create the data files directory for the chain if it does not exist
        self.__data_files_path = os.path.join(
            self.__data_location_path, "data/files", self.__chain_spec_hash)
        self._create_folder_if_not_exists(self.__data_files_path)
        # create the inbox directory for the chain if it does not exist
        self.__inbox_path = os.path.join(
            self.__data_location_path, "inbox", self.__chain_spec_hash)
        self._create_folder_if_not_exists(self.__inbox_path)
        # create the spam directory for the chain if it does not exist
        self.__spam_path = os.path.join(
            self.__data_location_path, "spam", self.__chain_spec_hash)
        self._create_folder_if_not_exists(self.__spam_path)
        # create the trash directory for the chain if it does not exist
        self.__trash_path = os.path.join(
            self.__data_location_path, "trash", self.__chain_spec_hash)
        self._create_folder_if_not_exists(self.__trash_path)

    ############################## SYNC LOGIC ##############################

    def __start_syncing(self):
        self._is_syncing = True

    def __stop_syncing(self):
        self._is_syncing = False

    def __sync_all(self):
        self.__start_syncing()
        # sync database with chain
        self.__sync_database()
        # sync folders with database
        self.__sync_folders()
        # sync writer SSH Public Keys
        self.__sync_writer_ssh_pub_keys()
        self.__stop_syncing()

    ### DATABASE SYNC ###
    def __sync_database(self) -> None:
        # sync topics
        (topics_to_add, topics_to_remove) = self.__sync_topics_table()
        # sync writers
        (writers_to_add, writers_to_remove) = self.__sync_writers_table(
            topics_to_add, topics_to_remove)

        logging.info(
            f"topics_to_add: {topics_to_add}, topics_to_remove: {topics_to_remove}, writers_to_add: {writers_to_add}, writers_to_remove: {writers_to_remove}")

        # update writers
        self.__update_writers_table()

    def __sync_topics_table(self) -> tuple:
        # get the topics from the chain
        topics_from_chain = self.__topics_from_chain()
        # get the topics from the database
        topics_from_db = self.__topics_from_db()
        # get the topics that are in the chain but not in the database
        topics_to_add = list(set(topics_from_chain) - set(topics_from_db))
        # get the topics that are in the database but not in the chain
        topics_to_remove = list(set(topics_from_db) - set(topics_from_chain))

        return topics_to_add, topics_to_remove

    def __sync_writers_table(self, topics_to_add, topics_to_remove) -> tuple:

        writer_nodes_from_chain_to_add = []
        writer_nodes_from_chain_to_remove = []

        # add the topics to the database
        for topic in topics_to_add:
            topic_from_chain = self.__topic_from_chain(topic)
            # get committer_nodes from topic_from_chain
            committer_nodes_from_chain = topic_from_chain["committer_nodes"]
            # add committer_nodes_from_chain to writer_nodes_from_topics_to_add
            writer_nodes_from_chain_to_add.extend(committer_nodes_from_chain)
            # get configuration_node from topic_from_chain
            configuration_node_from_chain = topic_from_chain["topic_configuration_node"]
            # add configuration_node_from_chain to writer_nodes_from_topics_to_add
            writer_nodes_from_chain_to_add.append(
                configuration_node_from_chain)
            self.__table_topics.insert({"topic": topic})
            logging.info(f"topic {topic} added to database")
        # remove the topics from the database
        for topic in topics_to_remove:
            topic_from_chain = self.__topic_from_chain(topic)
            # get committer_nodes from topic_from_chain
            committer_nodes_from_chain = topic_from_chain["committer_nodes"]
            # add committer_nodes_from_chain to writer_nodes_from_topics_to_remove
            writer_nodes_from_chain_to_remove.extend(
                committer_nodes_from_chain)
            # get configuration_node from topic_from_chain
            configuration_node_from_chain = topic_from_chain["topic_configuration_node"]
            # add topic_configuration_node to writer_nodes_from_topics_to_remove
            writer_nodes_from_chain_to_remove.append(
                configuration_node_from_chain)
            self.__table_topics.remove(Query().topic == topic)
            logging.info(f"topic {topic} removed from database")

        # get the writers from the database
        writers_from_db = self.__writers_from_db()
        # get the writers that are in the chain but not in the database
        writers_to_add = list(
            set(writer_nodes_from_chain_to_add) - set(writers_from_db))
        # get the writers that are in the database but not in the chain
        writers_to_remove = list(
            set(writer_nodes_from_chain_to_remove) - set(writers_from_db))

        # add the writers to the database
        for writer in writers_to_add:
            writer_from_chain = self.__writer_from_chain(writer)
            if len(writer_from_chain) == 0:
                continue
            self.__table_writers.insert({"writer": writer})
            logging.info(f"writer {writer} added to database")
        # remove the writers from the database
        for writer in writers_to_remove:
            self.__table_writers.remove(Query().writer == writer)
            logging.info(f"writer {writer} removed from database")

        return writers_to_add, writers_to_remove

    def __update_writers_table(self) -> None:
        # get the topics from the database
        topics_from_db = self.__topics_from_db()
        writers_to_update = []
        for topic in topics_from_db:
            # get the topic from the chain
            topic_from_chain = self.__topic_from_chain(topic)
            # get the committer_nodes from the chain
            committer_nodes_from_chain = topic_from_chain["committer_nodes"]
            # add the committer_nodes to the writers_to_update
            writers_to_update.extend(committer_nodes_from_chain)
            # get the configuration_node from the chain
            configuration_node_from_chain = topic_from_chain["topic_configuration_node"]
            # add the configuration_node to the writers_to_update
            writers_to_update.append(configuration_node_from_chain)
        logging.info(f"writers_to_update: {writers_to_update}")
        for writer in writers_to_update:
            writer_from_chain = self.__writer_from_chain(writer)
            logging.info(f"writer_from_chain: {writer_from_chain}")
            if len(writer_from_chain) == 0:
                continue
            self.__table_writers.upsert(
                {"writer": writer, "ip_address": writer_from_chain.get("ip_address", ""), "ssh_pub_key": writer_from_chain.get("ssh_pub_key", "")}, Query().writer == writer)
            logging.info(f"writer {writer} updated in database")

    ### FOLDER SYNC ###
    def __sync_folders(self):
        # sync topic folders
        self.__sync_topic_folders()

    def __sync_topic_folders(self):
        # get existing topic folders from the file system
        existing_topic_folders = self.__get_existing_topic_folders()
        logging.info(f"existing_topic_folders: {existing_topic_folders}")

        # get the topics from the existing topic folders, where the topic is an integer and is the last element is the folder path
        existing_topics_in_folders = list(
            map(lambda x: int(x.split("/")[-1]), existing_topic_folders))
        # logging.info(
        #     f"existing_topics_in_folders: {existing_topics_in_folders}")
        # get the topics from the database
        topics_from_db = self.__topics_from_db()
        # get the topics that are in the database but not in the file system
        topics_to_add = list(set(topics_from_db) -
                             set(existing_topics_in_folders))
        logging.info(f"topic_folders_to_add: {topics_to_add}")
        # get the topics that are in the file system but not in the database
        topics_to_remove = list(set(existing_topics_in_folders) -
                                set(topics_from_db))
        logging.info(f"topic_folders_to_remove: {topics_to_remove}")
        # add the topics to the file system
        for topic in topics_to_add:
            topic_folder = os.path.join(
                self.__data_files_path, str(topic))
            # create the topic folder
            self._create_folder_if_not_exists(topic_folder)
            logging.info(f"topic {topic} added to file system")
        # remove the topics from the file system
        for topic in topics_to_remove:
            topic_folder = os.path.join(
                self.__data_files_path, str(topic))
            # move files from the topic folder to the trash folder
            self._move_topic_files_to_topic_trash(topic_folder=topic_folder)
            # delete the topic folder
            self._delete_folder_if_exists(topic_folder)
            logging.info(f"topic {topic} removed from file system")

    def __get_existing_topic_folders(self):
        # get existing topic folders
        existing_topic_folders = []
        for root, dirs, files in os.walk(self.__data_files_path):
            for dir in dirs:
                existing_topic_folders.append(dir)
        return existing_topic_folders

    ### SYNC WRITER SSH PUBLIC KEYS ###
    def __sync_writer_ssh_pub_keys(self):
        # get the writers from the database
        writers_from_db = []
        for writer in self.__writers_from_db():
            # get the writer from the database
            writer_from_db = self.__table_writers.get(Query().writer == writer)
            writers_from_db.append(writer_from_db)
        logging.info(f"writers_from_db: {writers_from_db}")
        # get the writers from the file system
        writers_from_file_system = self.__writers_from_file_system()
        logging.info(f"writers_from_file_system: {writers_from_file_system}")
        writer_ip_addresses_from_db = []
        for writer in writers_from_db:
            logging.info(f"writer: {writer}")
            writer_ip_addresses_from_db.append(writer["ip_address"])
        # logging.info(
        #     f"writer_ip_addresses_from_db: {writer_ip_addresses_from_db}")
        writer_ip_addresses_from_file_system = []
        for writer in writers_from_file_system:
            writer_ip_addresses_from_file_system.append(writer["ip_address"])
        # logging.info(
        #     f"writer_ip_addresses_from_file_system: {writer_ip_addresses_from_file_system}")
        # get the writer ip addresses that are in the database but not in the file system
        writer_ip_addresses_to_add = list(
            set(writer_ip_addresses_from_db) - set(writer_ip_addresses_from_file_system))
        # logging.info(
        #     f"writer_ip_addresses_to_add: {writer_ip_addresses_to_add}")
        # get the writer ip addresses that are in the file system but not in the database
        writer_ip_addresses_to_remove = list(
            set(writer_ip_addresses_from_file_system) - set(writer_ip_addresses_from_db))
        # logging.info(
        #     f"writer_ip_addresses_to_remove: {writer_ip_addresses_to_remove}")
        # get the known_hosts file from reader_path/.ssh/known_hosts
        known_hosts_file = os.path.join(
            self.__writer_location_path, ".ssh", "known_hosts")
        # get the writers to add
        writers_to_add = []
        for writer in writers_from_db:
            if writer["ip_address"] in writer_ip_addresses_to_add:
                writers_to_add.append(writer)
        for writer in writers_from_file_system:
            if writer["ip_address"] in writer_ip_addresses_to_add:
                writers_to_add.append(writer)
        logging.info(f"writers_to_add: {writers_to_add}")
        # get the writers to remove
        writers_to_remove = []
        for writer in writers_from_db:
            if writer["ip_address"] in writer_ip_addresses_to_remove:
                writers_to_remove.append(writer)
        for writer in writers_from_file_system:
            if writer["ip_address"] in writer_ip_addresses_to_remove:
                writers_to_remove.append(writer)
        logging.info(f"writers_to_remove: {writers_to_remove}")
        # remove the writers from the file system
        self.__remove_writers_from_file_system(writers_to_remove)
        # add the writers to the file system
        self.__add_writers_to_file_system(writers_to_add)

    def __add_writers_to_file_system(self, writers):
        # get the known_hosts file from reader_path/.ssh/known_hosts
        known_hosts_file = os.path.join(
            self.__writer_location_path, ".ssh", "known_hosts")
        with open(known_hosts_file, "a") as f:
            for writer in writers:
                # get the writer ip address
                ip_address = writer["ip_address"]
                # get the writer ssh public key
                ssh_pub_key = writer["ssh_pub_key"]
                # add the writer to the known_hosts file
                f.write(f"{ip_address} {ssh_pub_key}")
                logging.info(f"writer {ip_address} added to file system")

    def __remove_writers_from_file_system(self, writers):
        # get the known_hosts file from reader_path/.ssh/known_hosts
        known_hosts_file = os.path.join(
            self.__writer_location_path, ".ssh", "known_hosts")
        # get the ssh public keys from the known_hosts file
        with open(known_hosts_file, "r") as f:
            known_hosts = f.readlines()
        # remove the writers from the known_hosts file
        with open(known_hosts_file, "w") as f:
            for known_host in known_hosts:
                # trim known_host
                known_host = known_host.strip()
                # ignore if known_host is empty
                if known_host == "":
                    continue
                # split the known_host by space
                known_host = known_host.split(" ")
                # get ip address from first split
                ip_address = known_host[0]
                # get ssh public key from second split
                ssh_pub_key = known_host[1]
                # check if the writer is in the writers to remove
                writer_to_remove = None
                for writer in writers:
                    if writer["ip_address"] == ip_address:
                        writer_to_remove = writer
                        break
                # if the writer is not in the writers to remove, add the writer to the known_hosts file
                if writer_to_remove is None:
                    f.write(f"{ip_address} {ssh_pub_key}")
                    logging.info(
                        f"writer {ip_address} removed from file system")

    def __writers_from_file_system(self):
        # get the writers from the file system
        writers_from_file_system = []
        # get known_hosts file from reader_path/.ssh/known_hosts
        known_hosts_file = os.path.join(
            self.__writer_location_path, ".ssh", "known_hosts")
        # get the ssh public keys from the known_hosts file
        with open(known_hosts_file, "r") as f:
            known_hosts = f.readlines()
        # get the writers from the known_hosts file
        for known_host in known_hosts:
            # trim known_host
            known_host = known_host.strip()
            # ignore if known_host is empty
            if known_host == "":
                continue
            # split the known_host by space
            known_host = known_host.split(" ")
            # get ip address from first split
            ip_address = known_host[0]
            # check if ip address is valid
            if not self._is_valid_ip_address(ip_address):
                continue
            # get public key from second and third splits
            public_key = f"{known_host[1]} {known_host[2]}" if len(
                known_host) > 2 else known_host[1]
            # append ip_address and public_key to writers_from_file_system
            writers_from_file_system.append(
                {"ip_address": ip_address, "ssh_pub_key": public_key})

        return writers_from_file_system

    ### SYNC ARIKURIS ###

    def __process_arikuri_added(self, block_number: int = None, call: any = None):
        block_number = block_number or None
        call = call or None
        assert block_number is not None
        assert call is not None
        topic_id = None
        kuri = None
        # parse the call args
        for arg in call["call_args"]:
            # get the topic id
            if arg["name"] == "topic_id":
                topic_id = arg["value"]
                # check if the topic id exists in the database
                if self.__table_topics.get(Query().topic == topic_id) is None:
                    topic_id = None
            # get the kuri
            if arg["name"] == "kuri":
                kuri = arg["value"]
        # check if the topic id and kuri are valid
        if topic_id is None or kuri is None:
            return
        # get the airikuri from the database
        kuri_from_db = self.__table_arikuris_state.get(
            Query().kuri == kuri)
        logging.info(f"kuri_from_db: {kuri_from_db}")
        topic_id = f"{topic_id}"
        # check if the arikuri exists in the database
        if kuri_from_db is None:
            # create the new kuri in the database
            self.__table_arikuris_state.insert(
                {"kuri": kuri, topic_id: ""})
        else:
            if topic_id not in kuri_from_db:
                # update the kuri in the database
                self.__table_arikuris_state.upsert(
                    {topic_id: ""}, Query().kuri == kuri)
        # update the last block synced
        self.__table_arikuris_state.upsert(
            {"last_block_synced": block_number}, Query().last_block_synced.exists())

    def __process_arikuri_deleted(self, block_number: int = None, call: any = None):
        block_number = block_number or None
        call = call or None
        assert block_number is not None
        assert call is not None
        topic_id = None
        kuri = None
        # parse the call args
        for arg in call["call_args"]:
            # get the topic id
            if arg["name"] == "topic_id":
                topic_id = arg["value"]
                # check if the topic id exists in the database
                if self.__table_topics.get(Query().topic == topic_id) is None:
                    topic_id = None
            # get the kuri
            if arg["name"] == "kuri":
                kuri = arg["value"]
        # check if the topic id and kuri are valid
        if kuri is None:
            return
        # get the airikuri from the database
        kuri_from_db = self.__table_arikuris_state.get(
            Query().kuri == kuri)
        logging.info(f"kuri_from_db: {kuri_from_db}")
        topic_id = f"{topic_id}"
        # check if the arikuri exists in the database
        if kuri_from_db is not None:
            filename = kuri_from_db.get(topic_id, None)
            if filename is not None:
                # remove the topic id from the kuri
                self.__table_arikuris_state.remove(
                    {topic_id: filename}, Query().kuri == kuri)
                # update the last block synced
                self.__table_arikuris_state.upsert(
                    {"last_block_synced": block_number}, Query().last_block_synced.exists())
                if filename != "":
                    # move the file from the topic folder to the inbox
                    topic_folder = os.path.join(
                        self.__data_files_path, str(topic_id))
                    # move the  file from the topic folder to the trash
                    self._move_topic_files_to_topic_trash(
                        topic_folder=topic_folder, filenames=[filename])

        # update the new_state in the database
        self.__table_arikuris_state.update(new_state)

    def __process_arikuris_transferred(self, block_number: int = None, call: any = None):
        block_number = block_number or None
        call = call or None
        assert block_number is not None
        assert call is not None
        from_topic_id = None
        to_topic_id = None
        kuris = []
        # parse the call args
        for arg in call["call_args"]:
            # get the from topic id
            if arg["name"] == "from_topic_id":
                from_topic_id = arg["value"]
                # check if the from topic id exists in the database
                if self.__table_topics.get(Query().topic == from_topic_id) is None:
                    from_topic_id = None
            # get the to topic id
            if arg["name"] == "to_topic_id":
                to_topic_id = arg["value"]
                # check if the to topic id exists in the database
                if self.__table_topics.get(Query().topic == to_topic_id) is None:
                    to_topic_id = None
            # get the kuris
            if arg["name"] == "kuris":
                kuris = arg["value"]
        from_topic_id = f"{from_topic_id}"
        to_topic_id = f"{to_topic_id}"
        # create the new state
        from_topic_filenames = []
        to_update = False
        for kuri in kuris:
            # get the airikuri from the database
            kuri_from_db = self.__table_arikuris_state.get(
                Query().kuri == kuri)
            # check if the arikuri exists in the database
            if kuri_from_db is not None:
                filename = kuri_from_db.get(to_topic_id, None)
                if filename is not None:
                    if from_topic_id is not None:
                        # remove the from topic id from the arikuri
                        self.__table_arikuris_state.remove(
                            {from_topic_id: filename}, Query().kuri == kuri)
                        to_update = True
                        from_topic_filenames.append(filename)
                    if to_topic_id is not None:
                        # add the to topic id to the arikuri
                        self.__table_arikuris_state.upsert(
                            {to_topic_id: ""}, Query().kuri == kuri)
                        to_update = True

        if len(from_topic_filenames) > 0:
            # move the from topic files to the inbox
            from_topic_folder = os.path.join(
                self.__data_files_path, str(from_topic_id))
            # move files from the topic folder to the inbox
            self._move_topic_files_to_inbox(
                topic_folder=from_topic_folder, filenames=from_topic_filenames)

        if to_update:
            # update the last block synced
            self.__table_arikuris_state.upsert(
                {"last_block_synced": block_number}, Query().last_block_synced.exists())

    def __process_metarium_calls(self, block_number: int = None, calls: list = []):
        block_number = block_number or None
        calls = calls or []
        assert block_number is not None
        assert len(calls) > 0
        # order the calls by the "call_index" key
        calls = sorted(calls, key=lambda call: call["call_index"])
        # process the calls
        for call in calls:
            logging.info(f"call: {call}")
            if call["call_function"] == "arikuri_added":
                self.__process_arikuri_added(
                    block_number=block_number, call=call)
            if call["call_function"] == "arikuris_transferred":
                self.__process_arikuris_transferred(
                    block_number=block_number, call=call)
            if call["call_function"] == "arikuri_deleted":
                self.__process_arikuri_deleted(
                    block_number=block_number, call=call)

    @ skip_if_syncing
    def __sync_arikuris(self, block_number: int = None):
        # get the block number
        if block_number is None:
            block_hash = self.__chain.get_block_hash(block_id=None)
            block_number = self.__chain.get_block_number(block_hash)
        else:
            block_hash = self.__chain.get_block_hash(block_id=block_number)
        # logging.info(f"block_number: {block_number}")
        # logging.info(f"block_hash: {block_hash}")
        # get the block
        block = self.__chain.get_block(block_hash)
        # logging.info(f"block: {block}")
        # get the extrinsics
        extrinsics = block["extrinsics"]
        extrinsics = list(
            map(lambda extrinsic: extrinsic.serialize(), extrinsics))
        # logging.info(f"extrinsics: {extrinsics}")
        metarium_extrinsics = []
        for extrinsic in extrinsics:
            if extrinsic["call"]["call_module"] == "Metarium":
                metarium_extrinsics.append(extrinsic)
        # logging.info(f"\n\nmetarium_extrinsics: {metarium_extrinsics}")

        metarium_calls = []

        for extrinsic in metarium_extrinsics:
            # get extrinsic receipt
            receipt = self.__chain.retrieve_extrinsic_by_hash(
                block_hash=block_hash,
                extrinsic_hash=extrinsic["extrinsic_hash"])
            if receipt.is_success == True:
                metarium_calls.append(extrinsic["call"])

        if len(metarium_calls) > 0:
            self.__process_metarium_calls(
                block_number=block_number, calls=metarium_calls)

    ############################## INBOX PROCESSING ##############################

    def __get_inbox_files(self):
        # get the inbox files
        inbox_files = os.listdir(self.__inbox_path)
        # remove the .gitkeep file
        inbox_files = list(
            filter(lambda file: file != ".gitkeep", inbox_files))
        return inbox_files

    @ skip_if_syncing
    def __process_inbox(self):
        # get the inbox files
        inbox_files = self.__get_inbox_files()
        logging.info(f"inbox_files: {inbox_files}")
        # process the inbox files
        for inbox_filename in inbox_files:
            is_file_useless = False
            # get the inbox file path
            inbox_file_path = os.path.join(self.__inbox_path, inbox_filename)
            # compute the arikuri
            kuri = self._arikuri_hash(
                file_path=inbox_file_path)
            # check if the arikuri exists in the database
            kuri_from_db = self.__table_arikuris_state.get(
                Query().kuri == kuri)
            logging.info(f"kuri_from_db: {kuri_from_db}")
            # check if the arikuri exists in the database
            if kuri_from_db is None:
                is_file_useless = True
            else:
                # if it exists, get the topics to which the arikuri belongs
                # parse the arikuri_from_db as a dictionary to get the topic_id from its key
                topic_ids_from_db = [
                    topic_id for topic_id in kuri_from_db.keys() if topic_id != "kuri"]
                logging.info(f"topic_ids_from_db: {topic_ids_from_db}")
                topic_ids_to_update = []
                for topic_id in topic_ids_from_db:
                    # check if the topic_id has an associated filename
                    filename_from_file_system = kuri_from_db[topic_id]
                    # if the filename_from_db is an empty string, move the inbox_file to the topic folder
                    if filename_from_file_system == "":
                        topic_ids_to_update.append(topic_id)
                logging.info(f"topic_ids_to_update: {topic_ids_to_update}")
                if len(topic_ids_to_update) == 0:
                    is_file_useless = True
                else:
                    # rename the inbox_file by prepending the _file_hash to the inbox_file
                    new_inbox_filename = f"{self._file_hash(inbox_file_path)}_{inbox_filename}"
                    self._rename_inbox_file(
                        filename=inbox_filename, new_filename=new_inbox_filename)
                    # copy the renamed inbox file to the folder of topics until last topic_id
                    for topic_id in topic_ids_to_update[:-1]:
                        logging.info(f"topic_id: {topic_id}")
                        # update the arikuri_from_db with the new filename
                        self.__table_arikuris_state.upsert(
                            {topic_id: new_inbox_filename}, Query().kuri == kuri)
                        # copy the new_inbox_file from the inbox to the topic folder
                        self._copy_inbox_file_to_topic_folder(
                            filename=new_inbox_filename, topic_id=topic_id)
                    # move the renamed inbox_file to the folder of last topic_id
                    topic_id = topic_ids_to_update[-1]
                    # update the arikuri_from_db with the new filename
                    kuri_from_db[topic_id] = new_inbox_filename
                    # move the new_inbox_file from the inbox to the topic folder
                    self._move_inbox_file_to_topic_folder(
                        filename=new_inbox_filename, topic_id=topic_id)
                    # update the arikuri_from_db with the new filename
                    self.__table_arikuris_state.upsert(
                        {topic_id: new_inbox_filename}, Query().kuri == kuri)
            if is_file_useless == True:
                # if it does not exist, move it to the trash/unknown folder
                self._move_inbox_file_to_unknown_trash(filename=inbox_filename)

    ############################## CHAIN QUERYING ##############################

    def __topics_from_chain(self):
        # query the chain for the topics_per_listener_node
        topics = self.__chain.query(
            module="Metarium", storage_function="ListenerTopicsMap", params=[self.__key.ss58_address])

        return list(map(int, list(map(str, topics.serialize()))))

    def __topic_from_chain(self, topic: int):
        # query the chain for the topic
        topic = self.__chain.query(
            module="Metarium", storage_function="Topics", params=[topic])

        topic = topic.serialize()

        if topic == None:
            topic = {}

        return topic

    def __writer_from_chain(self, writer: str):
        # query the chain for the writer
        writer = self.__chain.query(
            module="Metarium", storage_function="NodeInfoMap", params=[writer])

        writer = writer.serialize()
        if writer == None:
            writer = {}

        return writer

    ############################## DATABASE QUERYING ##############################
    def __topics_from_db(self):
        topics = []
        for topic in self.__table_topics.all():
            topics.append(topic["topic"])
        return topics

    def __writers_from_db(self):
        writers = []
        for writer in self.__table_writers.all():
            writers.append(writer["writer"])
        return writers

    ############################## MAIN FUNCTONS ##############################
    def __subscription_handler(self, obj, update_nr, subscription_id):
        logging.info(
            f"New block #{obj['header']['number']} produced by {obj['author']}")

        # sync all
        self.__sync_all()
        # sync arikuris
        self.__sync_arikuris(block_number=obj['header']['number'])
        # process inbox
        self.__process_inbox()

        if update_nr > math.inf:
            return {'message': 'Subscription will cancel when a value is returned', 'updates_processed': update_nr}

    def listen(self):
        result = self.__chain.subscribe_block_headers(
            self.__subscription_handler, include_author=True)

    ############################## UTILITY FUNCTONS ##############################

    def _file_hash(self, file_path: any = None) -> str:
        # check if file_path is valid
        if not isinstance(file_path, str):
            logging.error(f"file_path {file_path} is not a string!")
            raise TypeError
        if not os.path.exists(file_path):
            logging.error(f"file_path {file_path} does not exist!")
            raise FileNotFoundError
        # create a blake3 hash of the content
        hasher = blake3(max_threads=blake3.AUTO)
        with open(file_path, "rb") as f:
            counter = 0
            while True:
                counter += 1
                content = f.read(1024)
                if not content:
                    break
                hasher.update(content)

        return hasher.hexdigest()

    def _arikuri_hash(self, file_path: any = None) -> str:
        return f"|>blake3|{self._file_hash(file_path=file_path)}"

    def _create_folder_if_not_exists(self, folder_path: str = None) -> None:
        # check if folder_path is valid
        if not isinstance(folder_path, str):
            logging.error(f"folder_path {folder_path} is not a string!")
            raise TypeError
        # create the folder if it does not exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def _delete_folder_if_exists(self, folder_path: str = None) -> None:
        # check if folder_path is valid
        if not isinstance(folder_path, str):
            logging.error(f"folder_path {folder_path} is not a string!")
            raise TypeError
        # delete the folder if it exists. Oherwise return an error
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        else:
            logging.error(f"folder_path {folder_path} does not exist!")
            raise FileNotFoundError

    def _move_files(self, source_folder: str = None, destination_folder: str = None, filenames: list = None) -> None:
        # check if source_folder is valid
        if not isinstance(source_folder, str):
            logging.error(f"source_folder {source_folder} is not a string!")
            raise TypeError
        if not os.path.exists(source_folder):
            logging.error(f"source_folder {source_folder} does not exist!")
            raise FileNotFoundError
        # check if destination_folder is valid
        if not isinstance(destination_folder, str):
            logging.error(
                f"destination_folder {destination_folder} is not a string!")
            raise TypeError
        if not os.path.exists(destination_folder):
            logging.error(
                f"destination_folder {destination_folder} does not exist!")
            raise FileNotFoundError
        filenames = filenames or []
        if len(filenames) == 0:
            filenames = os.listdir(source_folder)
        # check if files is valid
        if not isinstance(filenames, list):
            logging.error(f"filenames {filenames} is not a list!")
            raise TypeError
        # move the files
        logging.info(
            f"Moving the following {len(filenames)} files from {source_folder} to {destination_folder}\n\n{filenames}\n\n")
        for filename in filenames:
            # if the file already exists in the destination folder, replace it
            if os.path.exists(os.path.join(destination_folder, filename)):
                os.remove(os.path.join(destination_folder, filename))
            shutil.move(os.path.join(source_folder, filename),
                        destination_folder)

    def _move_topic_files_to_inbox(self, topic_folder: str = None, filenames: list = None) -> None:
        # check if source_folder is valid
        if not isinstance(topic_folder, str):
            logging.error(f"source_folder {topic_folder} is not a string!")
            raise TypeError
        if not os.path.exists(topic_folder):
            logging.error(f"source_folder {topic_folder} does not exist!")
            raise FileNotFoundError
        # check if filenames is valid
        filenames = filenames or []
        if not isinstance(filenames, list):
            logging.error(f"topic_files {filenames} is not a list!")
            raise TypeError
        # move the files to the inbox
        self._move_files(source_folder=topic_folder,
                         destination_folder=self.__inbox_path, filenames=filenames)

    def _move_topic_files_to_topic_trash(self, topic_folder: str = None, filenames: list = None) -> None:
        # check if source_folder is valid
        if not isinstance(topic_folder, str):
            logging.error(f"source_folder {topic_folder} is not a string!")
            raise TypeError
        if not os.path.exists(topic_folder):
            logging.error(f"source_folder {topic_folder} does not exist!")
            raise FileNotFoundError
        filenames = filenames or []
        # check if files is valid
        if not isinstance(filenames, list):
            logging.error(f"filenames {filenames} is not a list!")
            raise TypeError
        # get the topic id from the topic folder
        topic_id = os.path.basename(topic_folder)
        # create the trash folder for the topic
        trash_folder = os.path.join(self.__trash_path, topic_id)
        self._create_folder_if_not_exists(trash_folder)
        # move the files to the trash folder
        self._move_files(source_folder=topic_folder,
                         destination_folder=trash_folder,
                         filenames=filenames)

    def _move_inbox_file_to_unknown_trash(self, filename: str = None) -> None:
        # check if filename is valid
        if not isinstance(filename, str):
            logging.error(f"filename {filename} is not a string!")
            raise TypeError
        # create the trash/unknown folder for the topic
        trash_folder = os.path.join(self.__trash_path, "unknown")
        self._create_folder_if_not_exists(trash_folder)
        # move the file to the unknown trash
        self._move_files(source_folder=self.__inbox_path,
                         destination_folder=trash_folder,
                         filenames=[filename])

    def _rename_inbox_file(self, filename: str = None, new_filename: str = None) -> None:
        # check if filename is valid
        if not isinstance(filename, str):
            logging.error(f"filename {filename} is not a string!")
            raise TypeError
        # check if new_filename is valid
        if not isinstance(new_filename, str):
            logging.error(f"new_filename {new_filename} is not a string!")
            raise TypeError
        # rename the file
        os.rename(os.path.join(self.__inbox_path, filename),
                  os.path.join(self.__inbox_path, new_filename))

    def _copy_inbox_file_to_topic_folder(self, filename: str = None, topic_id: str = None) -> None:
        # check if filename is valid
        if not isinstance(filename, str):
            logging.error(f"filename {filename} is not a string!")
            raise TypeError
        # check if topic_id is valid
        if not isinstance(topic_id, str):
            logging.error(f"topic_id {topic_id} is not a string!")
            raise TypeError
        # create the topic folder if it does not exist
        topic_folder = os.path.join(self.__data_files_path, topic_id)
        self._create_folder_if_not_exists(topic_folder)
        # copy the file to the topic folder
        shutil.copy(os.path.join(self.__inbox_path, filename),
                    topic_folder)

    def _move_inbox_file_to_topic_folder(self, filename: str = None, topic_id: str = None) -> None:
        # check if filename is valid
        if not isinstance(filename, str):
            logging.error(f"filename {filename} is not a string!")
            raise TypeError
        # check if topic_id is valid
        if not isinstance(topic_id, str):
            logging.error(f"topic_id {topic_id} is not a string!")
            raise TypeError
        # create the topic folder if it does not exist
        topic_folder = os.path.join(self.__data_files_path, topic_id)
        self._create_folder_if_not_exists(topic_folder)
        # move the file to the topic folder
        self._move_files(source_folder=self.__inbox_path,
                         destination_folder=topic_folder,
                         filenames=[filename])

    def _is_valid_ip_address(self, ip_address: str = None) -> bool:
        # check if ip_address is valid
        if not isinstance(ip_address, str):
            logging.error(f"ip_address {ip_address} is not a string!")
            raise TypeError
        # check if ip_address is valid
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            return False
