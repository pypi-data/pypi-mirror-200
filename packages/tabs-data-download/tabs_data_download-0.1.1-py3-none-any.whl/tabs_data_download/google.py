import os

from tabs_type.home import Home
from tabs_type.io.reader import Reader

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "/Users/alexis/tabs/tabs-366719-75f551fe5427.json"

CONDA_USERNAME = os.environ["CONDA_USERNAME"]
CONDA_PASSWORD = os.environ["CONDA_PASSWORD"]


KRAKEN_FUTURE_API_KEY = os.environ["KRAKEN_FUTURE_API_KEY"]
KRAKEN_FUTURE_SECRET_KEY = os.environ["KRAKEN_FUTURE_SECRET_KEY"]

KRAKEN_SPOT_API_KEY = os.environ["KRAKEN_SPOT_API_KEY"]
KRAKEN_SPOT_SECRET_KEY = os.environ["KRAKEN_SPOT_SECRET_KEY"]


if __name__ == "__main__":
    script = f"""
        sudo su
        export HOME=/home/rosuelalexis1
        export PATH=/home/rosuelalexis1/mamba/bin:$PATH
        mkdir -p /home/rosuelalexis1
        sudo apt-get update
        sudo apt-get install wget
        export PATH=/home/rosuelalexis1/mamba/bin:$PATH
        wget --quiet https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh -O /home/rosuelalexis1/mambaforge.sh
        rm -rf /home/rosuelalexis1/mamba
        sh /home/rosuelalexis1/mambaforge.sh -b -p /home/rosuelalexis1/mamba
        sudo mkdir -p /root/.mamba
        chmod 777 /home/rosuelalexis1/mamba
        sudo chmod 777 /root/.mamba
        mamba install -c conda-forge anaconda-client -y
        anaconda -q login --username alexisrosuel --password byvras-kofbyp-8neXju
        mamba install -c alexisrosuel -c conda-forge tabs-data-download -y
        mamba update --all -c alexisrosuel -c conda-forge -y
        export KRAKEN_FUTURE_API_KEY={KRAKEN_FUTURE_API_KEY}
        export KRAKEN_FUTURE_SECRET_KEY={KRAKEN_FUTURE_SECRET_KEY}
        export KRAKEN_SPOT_API_KEY={KRAKEN_SPOT_API_KEY}
        export KRAKEN_SPOT_SECRET_KEY={KRAKEN_SPOT_SECRET_KEY}
        sudo apt-get install lftp
        export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
        echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
        sudo curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
        sudo apt-get update -y
        sudo apt-get install gcsfuse -y
        sudo mkdir -p /mnt/disks/tabs
        sudo gcsfuse -o allow_other tabs-1 /mnt/disks/tabs
        echo "user_allow_other" >> /etc/fuse.conf
        echo "export PATH=/home/rosuelalexis1/mamba/bin:$PATH" >> /home/rosuelalexis1/.bashrc
        """

    symbols = Reader.load_settings_file(
        "/Users/alexis/tabs/code/tabs-settings/src/tabs_settings/configs/symbols.yml"
    )
    symbols_futures = symbols["kraken"]["futures"]
    symbols_spot = symbols["kraken"]["spot"]

    symbols_futures = " ".join(symbols_futures).upper()
    symbols_spot = " ".join(symbols_spot).upper()

    commands = """
    tabs-data-download-kraken-futures-book --output_dir /Users/alexis/tabs/data/market/raw/books/{version} --log_dir /Users/alexis/tabs/logs --basket {symbols_futures}  &
    tabs-data-download-kraken-spot-book --output_dir /Users/alexis/tabs/data/market/raw/books/{version} --log_dir /Users/alexis/tabs/logs  --basket {symbols_spot} &
    """.format(
        symbols_futures=symbols_futures, symbols_spot=symbols_spot, version="{version}"
    )

    # package_used = "tabs-data-download"
    # home = "/home/rosuelalexis1"
    # mambaforge_url = (
    #     "https://github.com/conda-forge/miniforge/releases/"
    #     "latest/download/Mambaforge-Linux-x86_64.sh"
    # )
    # set_mamba_path = f"""
    # export HOME={home}
    # export PATH={home}/mamba/bin:$PATH
    # """
    # pre = "DEBIAN_FRONTEND=noninteractive"
    # post = "> /dev/null"
    # pre, post = ' ', ''
    # mamba_install = f"""
    #     {pre} mkdir -p {home}
    #     {pre} sudo apt-get update {post}
    #     {pre} sudo apt-get install wget {post}
    #     export PATH={home}/mamba/bin:$PATH
    #     {pre} wget --quiet {mambaforge_url} -O {home}/mambaforge.sh
    #     {pre} rm -rf {home}/mamba
    #     {pre} sh {home}/mambaforge.sh -b -p {home}/mamba
    #     {pre} sudo mkdir -p /root/.mamba
    #     {pre} chmod 777 {home}/mamba
    #     {pre} sudo chmod 777 /root/.mamba
    # """
    # # tabs_settings = f"""
    # #     {pre} mkdir -p {home}/tabs/code
    # #     {pre} cp -r /mnt/disks/tabs/code/tabs-settings {home}/tabs/code
    # # """
    # conda_login = f"""
    #     {pre} mamba install -c conda-forge anaconda-client -y {post}
    #     {pre} anaconda -q login --username {CONDA_USERNAME} --password {CONDA_PASSWORD} {post}
    # """
    # packages_install = f"""
    #     {pre} mamba install -c alexisrosuel -c conda-forge {package_used} -y {post}
    #     {pre} mamba update --all -c alexisrosuel -c conda-forge -y {post}
    # """
    # env_variables = f"""
    # export KRAKEN_FUTURE_API_KEY={KRAKEN_FUTURE_API_KEY}
    # export KRAKEN_FUTURE_SECRET_KEY={KRAKEN_FUTURE_SECRET_KEY}
    # export KRAKEN_SPOT_API_KEY={KRAKEN_SPOT_API_KEY}
    # export KRAKEN_SPOT_SECRET_KEY={KRAKEN_SPOT_SECRET_KEY}
    # """
    # home_storage = Home.from_settings("google")
    # gcsfuse = f"""sudo apt-get install lftp
    # export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
    # echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
    # sudo curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    # sudo apt-get update -y
    # sudo apt-get install gcsfuse -y
    # sudo mkdir -p {home_storage.home_path}
    # sudo gcsfuse -o allow_other tabs-1 {home_storage.home_path}
    # echo "user_allow_other" >> /etc/fuse.conf
    # """
    # basket = ("LTC/USD", "PF_ADAUSD")
    # output_dir = home_storage.home_path / "data" / "market" / "raw" / "books" / "{version}"
    # to_run = f"""
    #     sudo tabs-data-download-kraken-futures-book --output_dir {output_dir} --basket {' '.join(basket)} &
    #     sudo tabs-data-download-kraken-spot-book --output_dir {output_dir} --basket {' '.join(basket)} &
    # """
    #
    # script = (
    #     # "sudo su"
    #     set_mamba_path
    #     # + f"""
    #     #     if [ ! -f {home}/mambaforge.sh ]; then
    #     #     """
    #     + mamba_install
    #     + conda_login
    #     # + tabs_settings
    #     + packages_install
    #     + env_variables
    #     + gcsfuse
    # )
    #
    # script += (
    #     # """
    #     #     fi
    #     #     """
    #     f"""
    #     echo "export PATH={home}/mamba/bin:$PATH" >> {home}/.bashrc
    #     . {home}/.bashrc
    #     """
    #     + to_run
    # )

    final_text = script + commands
    print(final_text)

    final_text = ""
    with open("startup.txt", "w") as f:
        f.write(final_text)

    import pdb

    pdb.set_trace()

    google_command = (
        f"gcloud compute instances create instance-2 --project=tabs-366719"
        f" --zone=europe-west2-a --machine-type=e2-small"
        f" --network-interface=network-tier=PREMIUM,subnet=default"
        # f" --no-restart-on-failure --maintenance-policy=TERMINATE"
        # f" --provisioning-model=SPOT --instance-termination-action=STOP"
        f" --service-account=277085644812-compute@developer.gserviceaccount.com"
        f" --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append,https://www.googleapis.com/auth/devstorage.full_control"
        f" --create-disk=auto-delete=yes,boot=yes,device-name=instance-1,image=projects/debian-cloud/global/images/debian-11-bullseye-v20230206,mode=rw,size=10,type=projects/tabs-366719/zones/europe-west2-a/diskTypes/pd-balanced"
        f" --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring"
        f" --reservation-affinity=any --metadata-from-file startup-script=startup.txt"
        f" --scopes=https://www.googleapis.com/auth/devstorage.read_write --metadata"
        f" bucket=tabs-1"
    )

    os.system(google_command)
