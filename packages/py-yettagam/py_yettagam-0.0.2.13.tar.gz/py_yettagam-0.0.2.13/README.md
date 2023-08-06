# py-yettagam

Python client for Yettagam - Metarium's storage layer

# Usage

## 1. Virtual environment

### 1.1. Install virtual environment

```
pip3 install virtualenv
```

### 1.2. Create virtual environment for metarium

```
python3 -m venv virtualenv ~/venv-yettagam
```

### 1.3. Activate metarium virtual environment

```
source ~/venv-yettagam/bin/activate
```

## 2. Dependencies

```
pip install py-yettagam==0.0.2.13
```

## 3. Example usage - Create a simple Yettagam Storage Sync

### 3.1. `Topic Listener`

Create a script called `listener-cli.py` with the following code block

```
import os
from argparse import ArgumentParser

from py_yettagam import (
    SubstrateListener,
)

parser = ArgumentParser()
# add key-path
parser.add_argument(
    "--key-path",
    type=str,
    help="Path to the key file of the Listener Node."
)
# add chain-spec-path
parser.add_argument(
    "--chain-spec-path",
    type=str,
    help="Path to the spec file the Listener Node's corresponding chain."
)
# add chain-url
parser.add_argument(
    "--chain-url",
    type=str,
    help="URL of the Listener Node's corresponding chain."
)
# add data-location-path, default to "/home/.metarium"
parser.add_argument(
    "--data-location-path",
    type=str,
    default="/home/.metarium",
    help="Path to the data location of the Listener Node. Default is '/home/.metarium'."
)
# add writer-location-path, default to "/home/writer"
parser.add_argument(
    "--writer-location-path",
    type=str,
    default="/home/writer",
    help="Path to the location of the user with write-only access to the 'inbox' folder. Default is '/home/writer'."
)
# add reader-location-path, default to "/home/reader"
parser.add_argument(
    "--reader-location-path",
    type=str,
    default="/home/reader",
    help="Path to the location of the user with read-only access to the 'outbox' folder. Default is '/home/reader'."
)
# add block-threshold-404, default to 16
parser.add_argument(
    "--block-threshold-404",
    type=int,
    default=16,
    help="Number of blocks to wait before retrying a block retrieval. Default is 16."
)
# add outbox-read-duration-seconds, default to 3600
parser.add_argument(
    "--outbox-read-duration-seconds",
    type=int,
    default=3600,
    help="Number of seconds for which the 'outbox' folder is open for a remote Node to read files from. Default is 3600."
)
# add force-historic-sync as a flag, default to False
parser.add_argument(
    "--force-historic-sync",
    action="store_true",
    help="Flag to force historic sync of the Listener Node from the corresponding earliest topic in the chain. Default is False."
)


if __name__ == "__main__":
    # parse arguments
    args = parser.parse_args()
    # verify key-path exists
    assert os.path.exists(args.key_path)
    # verify chain-spec-path exists
    assert os.path.exists(args.chain_spec_path)
    # verify chain-url is valid
    assert args.chain_url.startswith(
        "ws://") or args.chain_url.startswith("wss://")
    # check if data-location-path exists. If not, create it. Inform user.
    if not os.path.exists(args.data_location_path):
        os.mkdir(args.data_location_path)
        print(
            f"Created data location path: {args.data_location_path}")
    # check if writer-location-path exists. If not, inform user.
    if not os.path.exists(args.writer_location_path):
        print(
            f"Writer location path does not exist: {args.writer_location_path}")
    # check if reader-location-path exists. If not, inform user.
    if not os.path.exists(args.reader_location_path):
        print(
            f"Reader location path does not exist: {args.reader_location_path}")
    # create listener
    listener = SubstrateListener(
        key_path=args.key_path,
        chain_spec_path=args.chain_spec_path,
        chain_url=args.chain_url,
        force_historic_sync=args.force_historic_sync,
        data_location_path=args.data_location_path,
        writer_location_path=args.writer_location_path,
        reader_location_path=args.reader_location_path,
        block_threshold_404=args.block_threshold_404,
        outbox_read_duration_seconds=args.outbox_read_duration_seconds,
    )
```

Run the cli script

```
python listener-cli.py -h
```

### 3.2. `Topic Committer`

Create a script called `committer-cli.py` with the following code block

```
import os
from argparse import ArgumentParser

from py_yettagam import (
    SubstrateCommitter,
)

parser = ArgumentParser()
# add key-path
parser.add_argument(
    "--key-path",
    type=str,
    help="Path to the key file of the Committer Node."
)
# add chain-spec-path
parser.add_argument(
    "--chain-spec-path",
    type=str,
    help="Path to the spec file the Committer Node's corresponding chain."
)
# add chain-url
parser.add_argument(
    "--chain-url",
    type=str,
    help="URL of the Committer Node's corresponding chain."
)
# add topic-id
parser.add_argument(
    "--topic-id",
    type=int,
    help="Topic ID which the Committer Node's is configured to commite to."
)
# add file-location-path
parser.add_argument(
    "--file-location-path",
    type=str,
    help="Path to the file to be uploaded."
)
# add ssh-private-key-path
parser.add_argument(
    "--ssh-private-key-path",
    type=str,
    help="Path to the SSH private key file of the Committer Node."
)
# add ssh-private-key-passphrase
parser.add_argument(
    "--ssh-private-key-passphrase",
    type=str,
    help="Passphrase of the SSH private key file of the Committer Node."
)
# add listener-threshold, default=3
parser.add_argument(
    "--listener-threshold",
    type=int,
    default=3,
    help="Maximum number of corresponding Listeners to which the committed file will be uploaded. Default is 3."
)


if __name__ == "__main__":
    # parse arguments
    args = parser.parse_args()
    # verify key-path exists
    assert os.path.exists(args.key_path)
    # verify chain-spec-path exists
    assert os.path.exists(args.chain_spec_path)
    # verify chain-url is valid
    assert args.chain_url.startswith(
        "ws://") or args.chain_url.startswith("wss://")
    # verify topic-id is valid
    assert args.topic_id > 0
    # verify file-location-path exists
    assert os.path.exists(args.file_location_path)
    # verify ssh-private-key-path exists
    assert os.path.exists(args.ssh_private_key_path)
    # verify ssh-private-key-passphrase is valid
    assert args.ssh_private_key_passphrase is not None
    # verify listener-threshold is valid
    assert args.listener_threshold > 0
    # create committer
    committer = SubstrateCommitter(
        key_path=args.key_path,
        chain_spec_path=args.chain_spec_path,
        chain_url=args.chain_url,
        topic_id=args.topic_id,
        file_location_path=args.file_location_path,
        ssh_private_key_path=args.ssh_private_key_path,
        ssh_private_key_passphrase=args.ssh_private_key_passphrase,
        listener_threshold=args.listener_threshold,
    )
```

Run the cli script

```
python committer-cli.py -h
```

## 4. Teardown

Please remember to deactivate the virtual environment after usage

```
deactivate
```
