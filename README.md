[![CLA assistant](https://cla-assistant.io/readme/badge/assetninja/assetexchange)](https://cla-assistant.io/assetninja/assetexchange)

# assetexchange

An asset exchange protocol implementation used by Asset Ninja.

## Python

### Pack Extensions

```sh
# prerequisites
# npm and npx
brew install node

# pack extensions
cd ./python
./dist_extensions.sh

# list pack result
ls -l ./dist
```

### Pack Library for Embedding

```sh
# prerequisites
# npm and npx
brew install node

# pack library for embedding (example commands for Maya)
cd ./python
./dist_library.sh maya myproduct_assetexchange $HOME/dev/myproduct/assetexchange.py
```

This is how you can use the packed library:

```py
# Step 1: import the packed assetexchange.py
from . import assetexchange

# Step 2: now you can import the modules contained in the packed library
import myproduct_assetexchange.assetexchange_maya as assetexchange_maya

# ...
```
